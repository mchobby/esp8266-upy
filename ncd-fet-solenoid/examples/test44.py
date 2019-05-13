"""
Test the NCD 4-Channel FET Solenoid + 4 GPIO also named

* MCP23008 4-Channel 8W 12V FET + 4 GPIO Solenoid Driver Valve Controller with I2C Interface.

NCD-4Channel-FET-Solenoid-4Gpio : https://store.ncd.io/product/mcp23008-4-channel-8w-12v-fet-solenoid-driver-valve-controller-4-channel-gpio-with-i2c-interface/
See also NCD Products at http://shop.mchobby.be/

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
from fetsol import FetSolenoid4
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

# Add "address" parameter as needed
board = FetSolenoid4( i2c )

# Activating Fet Outputs
for i in range(4):
	board.output( i, True )
	time.sleep( 1 )

# deactivate the 4 outputs in 2 steps
board.output_pins( {0: False, 2: False } )
time.sleep( 1 )
board.output_pins( {1: False, 3: False } )
time.sleep( 1 )

dic = {}
dic[2] = True
dic[3] = True
board.output_pins( dic )
time.sleep( 1 )

# Reset all FETs
board.reset()

# --------------------------------------------
#   Manipulate GPIOs
# --------------------------------------------
# Setting GPIO 6 as output
board.setup( 6, Pin.OUT )
board.output( 6, True )

# Setting GPIO 4 as input + activate pull-up
board.setup( 4, Pin.IN )
board.pullup( 4, True )
# Perform 10 reading
for i in range( 10 ):
	print( "GPIO 4 = %s" % board.input(4) )
	time.sleep( 1 )

# turn off GPIO 6
board.output( 6, False )

print( "That's all Folks!" )
