"""
PCA9536 GPIO extender - PinMode, input, output & pullup testing

The API follows the MCPxxx ones (so based on Adafruit's works)

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

from pca9536 import PCA9536
from machine import Pin, I2C
from time import sleep

# Create the I2C bus accordingly to your plateform.
# Pyboard: SDA on Y9, SCL on Y10. See NCD wiring on https://github.com/mchobby/pyboard-driver/tree/master/NCD
#         Default bus Freq 400000 = 400 Khz is to high.
#         So reduce it to 100 Khz. Do not hesitate to test with 10 KHz (10000)
i2c = I2C( 2, freq=100000 )
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )

pca = PCA9536( i2c )

# Set IO0 to Input - Hardware pull-up activat on all Pin by default
pca.setup( 0, Pin.IN  )
# Set IO1 to Input - Hardware pull-up activat on all Pin by default
#	Read's result will be False when pin is HIGH (not connected to ground)
#	Read's result will be True  when pin is LOW  (connected to ground)
pca.setup ( 1, Pin.IN )

# Set IO3 to Output
pca.setup( 3, Pin.OUT )
pca.output( 3, False )  # High by default because of the pull-up for input
for i in range( 2 ):
	# Tip: see output_pins() to update multiple pins
	pca.output( 3, True )
	sleep( 1 ) # 1 Second
	pca.output( 3, False )
	sleep( 1 )

# Read value on GPIO 0 - pull-up activated by default
for i in range( 10 ):
	# Tip: see input_pins() for multiple pin reads
	print( "IO0 = %s" % (pca.input(0)) )
	sleep( 1 )

# Read value on GPIO 1 - pull-up activated by default
for i in range( 10 ):
	# Tip: see input_pins() for multiple pin reads
	print( "IO1 = %s" % (pca.input(1)) )
	sleep( 1 )


print( "That's all folks")
