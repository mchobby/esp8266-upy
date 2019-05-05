"""
Test the NCD MPL115A2 (I2C) sensor board from National Control Device.

Display the hPa Athmospherique pressure and temperature sensor from MPL115A2 is an I2C.

NCD-MPL115A2 : http://shop.mchobby.be/
NCD-MPL115A2 : https://store.ncd.io/product/mpl115a2-digital-barometer-50-to-115-kpa-i2c-mini-module/

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
from mpl115a2 import MPL115A2
import time

# Create the I2C bus accordingly to your plateform.
# Pyboard: SDA on Y9, SCL on Y10. See NCD wiring on https://github.com/mchobby/pyboard-driver/tree/master/NCD
#         Default bus Freq 400000 = 400 Khz is to high.
#         So reduce it to 100 Khz. Do not hesitate to test with 10 KHz (10000)
i2c = I2C( 2, freq=100000 )
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )

mpl = MPL115A2( i2c )
print( 'raw_values ', mpl.raw_values ) # computer Friendly pressure, temp
val = mpl.values # Human Friendly values
print( val[0] ) # pressure hPa
print( val[1] ) # temp °C

while True:
	print( '%-15s %-15s' % mpl.values )
	time.sleep(1)
