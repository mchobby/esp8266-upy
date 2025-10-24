# -*- coding: utf-8 -*-
""" 
    Driver for WS2812 / NeoPixel RGB LEDs using Hardware SPI to emit the data.
    Uses the over-sampling method to made it compatible with MicroPython.

    Build using machine.SPI interface  

    Original at https://github.com/mchobby/esp8266-upy/tree/master/neopixel

    Written by D. Meurisse from shop.mchobby.be
"""

import gc
import machine

__version__ = '1.2.0'

class WS2812:
    """
    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
    of LEDs.

    Example of use:
		* modified lib @ https://github.com/mchobby/esp8266-upy/tree/master/neopixel
		* original lib @ https://github.com/JanBednarik/micropython-ws2812


	History:
       1.2 - based on machine.SPI hardware bus (Plateform Agnostic)
	   1.1 - small fix + compatibility with official ESP8266 NeoPixel library
	   1.0 - original version by JanBednarik. https://github.com/JanBednarik/micropython-ws2812
    """
    buf_bytes = (0x11, 0x13, 0x31, 0x33)

    def __init__(self, spi_bus=1, led_count=1, intensity=1):
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        """
        self.led_count = led_count
        self.intensity = intensity

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count * 3 * 4
        self.buf = bytearray(self.buf_length)

        # SPI init
        self.spi = machine.SPI(spi_bus, baudrate=3200000, polarity=0, phase=0)

        # turn LEDs off
        self.show([])

    def show(self, data):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def write( self ):
        # ESP8266 NeoPixel compatibility
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over SPI.
        """
        self.spi.write(self.buf)
        gc.collect()

    def __setitem__( self, index, data ):
        """ allow access like pixels[1] = (r,g,b) """
        # ESP8266 NeoPixel compatibility
        self.update_buf( data=[data], start=index )

    def fill( self, color ):
        """ fill with a (r,g,b) color """
        # ESP8266 NeoPixel compatibility
        pixel = [color]
        for i in range( self.led_count ):
            self.update_buf( data=pixel, start=i )

    @property
    def n( self ):
        """ Number of leds """
        # ESP8266 NeoPixel compatibility
        return self.led_count

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data. data is a list of rgb tuples.

        Order of colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.buf
        buf_bytes = self.buf_bytes
        intensity = self.intensity

        mask = 0x03
        index = start * 12
        for red, green, blue in data:
            red = int(red * intensity)
            green = int(green * intensity)
            blue = int(blue * intensity)

            buf[index] = buf_bytes[green >> 6 & mask]
            buf[index+1] = buf_bytes[green >> 4 & mask]
            buf[index+2] = buf_bytes[green >> 2 & mask]
            buf[index+3] = buf_bytes[green & mask]

            buf[index+4] = buf_bytes[red >> 6 & mask]
            buf[index+5] = buf_bytes[red >> 4 & mask]
            buf[index+6] = buf_bytes[red >> 2 & mask]
            buf[index+7] = buf_bytes[red & mask]

            buf[index+8] = buf_bytes[blue >> 6 & mask]
            buf[index+9] = buf_bytes[blue >> 4 & mask]
            buf[index+10] = buf_bytes[blue >> 2 & mask]
            buf[index+11] = buf_bytes[blue & mask]

            index += 12

        return index // 12

    def fill_buf(self, data):
        """
        Fill buffer with RGB data. Data is a list of (r,g,b tuples)

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 12, self.buf_length):
            buf[index] = off
            index += 1

# Class alias
NeoPixel = WS2812
