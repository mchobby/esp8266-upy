"""
TM1650 test script - 4-Digital LED Segment Display module (DFR0645)
==========================================================

For wiring, see the:
 https://github.com/mchobby/esp8266-upy/tree/master/grav-digital-led


Author(s):
* Meurisse D for MC Hobby sprl
"""
from machine import I2C
from ledseg4 import LedSegment4
from time import sleep

# Raspberry-Pi Pico
i2c = I2C(1, freq=100000 ) # sda=GP6, scl=GP7 , limited to 100 KHz
dis = LedSegment4( i2c ) # DFR0645 4 digit LED display

# Display integers
dis.int( 4289 )
sleep(2)
dis.int(-43)
sleep(2)

# Display float
dis.float(0.1)
sleep(2)
dis.float(-3.1415)
sleep(2)

# Brightness control (0..7)
for i in range( 8 ):
	dis.brightness( i )
	dis.print( 'br %s' % i )
	sleep(2)

# Switch display off
dis.off()
