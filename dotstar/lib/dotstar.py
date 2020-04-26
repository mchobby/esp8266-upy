START_HEADER_SIZE = 4
LED_START = 0b11100000  # Three "1" bits, followed by 5 brightness bits

RGB = (0, 1, 2) # Pixel color order constants
RBG = (0, 2, 1)
GRB = (1, 0, 2)
GBR = (1, 2, 0)
BRG = (2, 0, 1)
BGR = (2, 1, 0)

class DotStar:
    def __init__(self, spi, n, *, brightness=1.0, auto_write=True,
                 pixel_order=BGR):
        self._spi = spi
        self._n = n
        # Supply one extra clock cycle for each two pixels in the strip.
        self.end_header_size = n // 16
        if n % 16 != 0:
            self.end_header_size += 1
        self._buf = bytearray(n * 4 + START_HEADER_SIZE + self.end_header_size)
        self.end_header_index = len(self._buf) - self.end_header_size
        self.pixel_order = pixel_order
        # Four empty bytes to start.
        for i in range(START_HEADER_SIZE):
            self._buf[i] = 0x00
        # Mark the beginnings of each pixel.
        for i in range(START_HEADER_SIZE, self.end_header_index, 4):
            self._buf[i] = 0xff
        # 0xff bytes at the end.
        for i in range(self.end_header_index, len(self._buf)):
            self._buf[i] = 0xff
        self._brightness = 1.0
        self.auto_write = auto_write

    def deinit(self):
        """Blank out the DotStars and release the resources."""
        self.auto_write = False
        for i in range(START_HEADER_SIZE, self.end_header_index):
            if i % 4 != 0:
                self._buf[i] = 0
        self.show()
        if self._spi:
            self._spi.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def _set_item(self, index, value):
        offset = index * 4 + START_HEADER_SIZE
        rgb = value
        if isinstance(value, int):
            rgb = (value >> 16, (value >> 8) & 0xff, value & 0xff)

        if len(rgb) == 4:
            brightness = value[3]
            # Ignore value[3] below.
        else:
            brightness = 1

        brightness_byte = 32 - int(32 - brightness * 31) & 0b00011111
        self._buf[offset] = brightness_byte | LED_START
        self._buf[offset + 1] = rgb[self.pixel_order[0]]
        self._buf[offset + 2] = rgb[self.pixel_order[1]]
        self._buf[offset + 3] = rgb[self.pixel_order[2]]

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._n)
            length = stop - start
            if step != 0:
                # same as math.ceil(length / step)
                # Idea from https://fizzbuzzer.com/implement-a-ceil-function/
                length = (length + step - 1) // step
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index, val)

        if self.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range(*index.indices(self._n)):
                out.append(
                    tuple(self._buf[in_i * 4 + (3 - i) + START_HEADER_SIZE] for i in range(3)))
            return out
        if index < 0:
            index += len(self)
        if index >= self._n or index < 0:
            raise IndexError
        offset = index * 4
        return tuple(self._buf[offset + (3 - i) + START_HEADER_SIZE]
                     for i in range(3))

    def __len__(self):
        return self._n

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = min(max(brightness, 0.0), 1.0)

    def fill(self, color):
        auto_write = self.auto_write
        self.auto_write = False
        for i in range(self._n):
            self[i] = color
        if auto_write:
            self.show()
        self.auto_write = auto_write

    def show(self):
        if self._spi:
            self._spi.write(self._buf)
