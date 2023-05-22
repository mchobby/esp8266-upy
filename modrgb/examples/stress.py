"""
Stress test the Olimex MOD-RGB board under MicroPython. 

MOD-RGB board : http://shop.mchobby.be/product.php?id_product=1410 
MOD-RGB board : https://www.olimex.com/Products/Modules/LED/MOD-RGB/open-source-hardware 
User's guide : https://www.olimex.com/Products/Modules/LED/MOD-RGB/resources/MOD-RGB_fw_rev_3.pdf f 

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

from machine import I2C, Pin
from time import sleep_ms
from modrgb import MODRGB
from rgbfx import randrange

i2c = I2C( sda=Pin(2), scl=Pin(4) )
rgb = MODRGB( i2c ) # default address=0x20
rgb.pwm( True )

iter = 0
print( 'MOD-RGB start I2C stress test' )
while True:
    color = (randrange( 255 ), randrange( 255 ), randrange( 255 ) )
    iter += 1
    print( 'Iteration %s with color %s' % (iter, color))
    rgb.set_rgb( color )

print( "That's the end folks")