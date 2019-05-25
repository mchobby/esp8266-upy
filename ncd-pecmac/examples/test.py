"""
Test the NCD PECMAC 'AC Current Monitor' (I2C) board from National Control Device.

Display the Current Sensing from 2-Channel On-Board 97% Accuracy - 30A (PR29-8).

* NCD-PR29-6_10A (PECMAC) : http://shop.mchobby.be/
* NCD-PR29-6_10A (PECMAC): https://store.ncd.io/product/2-channel-on-board-97-accuracy-ac-current-monitor-with-i2c-interface/

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
from pecmac import PECMAC, PECMAC_SENSOR_TYPES
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

# Use address parameter as suited
board = PECMAC( i2c )
print( 'Sensor Type : %d (%s)' % (board.sensor_type, PECMAC_SENSOR_TYPES[board.sensor_type]) )
print( 'Max current : %d' % board.max_current )
print( 'Channels    : %d' % board.channels    )

print( '' )
print( 'Read Channels Calibration :' )
for ch in range(1, board.channels+1 ):
	print( 'Channel %s = %i' % (ch, board.read_calibration(ch)) )

# board.raw_values will return one entry per channels
# Raw values are more appropriate for computation
print( '' )
print( 'Reading Channels RAW value (floats):' )
print( board.raw_values )

print( '' )
print( 'Human Friendly values (textual):')
while True:
	# board.values will return one entry per channels
	print( board.values )
	time.sleep(1)
