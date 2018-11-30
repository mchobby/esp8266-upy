"""
LTR_501ALS light sensor reading.

LTR-501ALS is a sensor can measure visible light from 0.01 Lux to 64000 Lux with linear response.
It can also be used ad proximty sensor (up 10 cm).

MOD-LTR-501ALS board : http://shop.mchobby.be/product.php?id_product=1415
MOD-LTR-501ALS board : https://www.olimex.com/Products/Modules/Sensors/MOD-LTR-501ALS/open-source-hardware  
Arduino code sample  : https://github.com/OLIMEX/UEXT-MODULES/tree/master/MOD-LTR-501ALS/ARDUINO%20EXAMPLE

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
from time import sleep
from ltr501 import * 

i2c = I2C( sda=Pin(2), scl=Pin(4) ) # 400000 = 400 KHz, 100000 = 100 KHz (standard)
ltr = LTR_501ALS( i2c ) # 2 Lux to 64000 Lux

# or use the following for alternate 0.01 to 320 Lux range
#
# ltr = LTR_501ALS( i2c, lux_range = LUX_RANGE_320 ) 

while True:
    dr = ltr.data_ready
    if DR_LUX in dr:
    	l = ltr.lux # read ALS_0 & ALS_1
    	print( "Lux ALS_0, ALS_1 = ", l )

    if DR_PROXIMITY in dr:
    	p = ltr.proximity # read (value, cm)
    	print( "Proximity value, cm =" , p )

    print( '-'*40 )
    sleep( 1 )


print( "That's the end folks")
