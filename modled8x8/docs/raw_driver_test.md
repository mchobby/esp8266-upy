# RAW Driver testing

__Warning: the RAW driver is deprecated since the FrameBuffer portage. DO NOT USE IT unless you know what you are doing!__

__The RAW driver use different axis model herited from Arduino code.__

![MOD-LED8x8RGB - FrameBuffer Axis](_static/modled8x8-axis.jpg)

## Test with RAW driver
The initial port of Arduino driver to MicroPython was done with the _video buffer_ suggested by Olimex in the orginal code ( `self.buffer = [0]*self.matrixes*24` ).

The `ModLedRGBraw` driver (examples/modledraw.py) only implement pixel drawing for testing the protocol before switching to FrameBuffer implementation.

The final FrameBuffer driver, the suited version to use, will be made available in the `modled/modled.py` file.

## RAW library & examples
The raw library was for testing only and not designed for regular usage.

Copy the library file `examples/modledraw.py` and the test file `examples/testraw.py` on your MicroPython board.

The `testraw.py` file (listed here under) can be loaded from REPL session with `import testraw`.

```
# ----------------------------------------------
#   DO NOT USE RAW driver
#   USE the FrameBuffer driver (here upper)
# ----------------------------------------------

from machine import Pin, SPI
from modledraw import ModLedRGBraw

# Initialize the SPI Bus (on ESP8266-EVB)
# Software SPI
#    spi = SPI(-1, baudrate=4000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# Hardware SPI on Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # low @ 2 MHz
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

modled = ModLedRGBraw( spi, ss ) # Just one LED brick LED-8x8RGB
modled.drawPixel( 1,1, color=1 ) # Red
modled.drawPixel( 2,2, color=2 ) # Green
modled.drawPixel( 3,3, color=4 ) # Blue
modled.drawPixel( 4,8, color=3 ) # Red + Green = Yellow
modled.drawPixel( 5,8, color=5 ) # Red + Blue  = Magenta
modled.drawPixel( 6,7, color=6 ) # Green + Blue  = Cyan
modled.drawPixel( 7,6, color=7 ) # Red + Green + Blue  = White
modled.show()
```

which produce the following result (with axis reference) :

![MOD-LED8x8RGB to RAW MicroPython driver testing](_static/modled8x8-axis.jpg)

The `examples/testraw2x3.py` test script explore the matrix chaining (2 rows, 3 columns).

![MOD-LED8x8RGB chaning for RAW MicroPython driver testing](_static/modled8x8-chaining.jpg)

Which produce a really nice result under a sheet of paper (otherwise there is too much light for the camera).

![MOD-LED8x8RGB chaning for RAW MicroPython driver testing](_static/modled8x8-testraw2x3.jpg)
