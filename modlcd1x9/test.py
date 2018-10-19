'''
Test yje Olimex MOD-LCD1x9 board. 

It allows the user to control one or more MOD-IO board.
MOD-LCD1x9 board : http://shop.mchobby.be/product.php?id_product=1414
MOD-LCD1x9 : https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/open-source-hardware    
User Guide : https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/LCD1X9.pdf 

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
'''

from machine import I2C, Pin
from time import sleep_ms
from modlcd19 import MODLCD1x9

i2c = I2C( sda=Pin(2), scl=Pin(4) )
lcd = MODLCD1x9( i2c ) # Will light all segments
lcd.write( '123456789' )
lcd.point( 5, True )
lcd.selection( 2, True )
lcd._update()