"""
 Test the modledraw implementation organized in 2 raw of 3 slabs (RAW CODE
 PORTAGE to micropython) for the MOD-LED8x8RGB Olimex board.
 MOD-LED8x8RGB is 8x8 RGB LED Matrix (7 colors) that can be daisy chained.

 modledraw is a temporary test implementation before going to the Frambuffer implementation.

MOD-LED8x8RGB board : http://shop.mchobby.be
MOD-LED8x8RGB board : https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware
Arduino code sample : https://github.com/OLIMEX/UEXT-MODULES/tree/master/MOD-LED8x8RGB/ARDUINO%20EXAMPLE

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

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

modled = ModLedRGBraw( spi, ss, width=3, height=2 ) # 2x3 LEDs brick LED-8x8RGB

def drawBox( modled, x, y, width, height, color ):
	for i in range( width ):
		modled.drawPixel( x+i, y+height-1, color )
		modled.drawPixel( x+i, y,  color )
	for i in range( height ):
		modled.drawPixel( x, y+i, color )
		modled.drawPixel( x+width-1, y+i, color)

drawBox( modled, 1,1, 24, 16, color = 1 ) # red
drawBox( modled, 2,2, 22, 14, color = 2 ) # Green
drawBox( modled, 3,3, 20, 12, color = 4 ) # Blue
drawBox( modled, 4,4, 18, 10, color = 3 ) # Red + Green = Yellow
drawBox( modled, 5,5, 16,  8, color = 5 ) # Red + Blue  = Magenta
drawBox( modled, 6,6, 14,  6, color = 6 ) # Green + Blue  = Cyan
drawBox( modled, 7,7, 12,  4, color = 7 ) # Red + Green + Blue  = White


modled.show()
