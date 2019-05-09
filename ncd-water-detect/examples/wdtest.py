"""
Test the Water Detect (I2C) sensor board from National Control Device.
Make the buzzer scream when it detects water.

NCD-Water-Detection : http://shop.mchobby.be/
NCD-Water-Detection : https://store.ncd.io/product/water-detection-sensor-with-buzzer/
Datasheet : https://media.ncd.io/sites/2/20170721134419/PCA9536_WDBZ_I2CS.pdf

The MIT License (MIT)
Copyright (c) 2019 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
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

from machine import Pin, I2C
from time import sleep
from wdetect import WaterDetect

# Create the I2C bus accordingly to your plateform.
# Pyboard: SDA on Y9, SCL on Y10. See NCD wiring on https://github.com/mchobby/pyboard-driver/tree/master/NCD
#         Default bus Freq 400000 = 400 Khz is to high.
#         So reduce it to 100 Khz. Do not hesitate to test with 10 KHz (10000)
i2c = I2C( 2, freq=100000 )
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )

wd = WaterDetect( i2c )
buz = False
try:
	while True:
		if wd.has_water:
			print( "WATER DETECTED!" )
			# Call the set buzzer ONLY ONCE to not load the I2C bus
			if not buz:
				buz = True
				wd.buzzer( True )
		else:
			print( '...')
			# Call the set buzzer ONLY ONCE to not load the I2C bus
			if buz:
				buz = False
				wd.buzzer( False )
		sleep( 1 )
finally:
	# be sure than buzzer is deactivated
	# ... before someone get crazy
	if buz:
		wd.buzzer( False )

print( "That's all folks!" )
