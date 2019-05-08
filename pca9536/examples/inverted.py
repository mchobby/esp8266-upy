"""
PCA9536 GPIO extender - Testing INPUT Polarity inverter

When not inverted:
	Input with HIGH level (not connected to Ground) returns True
	Input with LOW  level (    connected to Ground) returns False

When INVERTED:
	Input with High level (not connected to Ground) returns False
	Input with LOW  level (    connected to Ground) returns True

INVERTED mode is useful to get a True value for the input WHEN a pressed
	push button shorts the input pin to the ground.

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

# reset the PCA configuration
pca.reset()

# Set IO1 as Input
pca.setup ( 1, Pin.IN )

invert_it = False
while True:
	# Tip: see input_pins() for multiple pin reads
	for i in range( 5 ):
		print( "IO1 = %s" % ( pca.input(1)) )
		sleep( 1 )
	invert_it = not( invert_it )
	print( 'Set polarity to %s' % ('INVERTED' if invert_it else 'normal (retain)') )
	pca.polarity( 1, inverted=invert_it )

print( "That's all folks")
