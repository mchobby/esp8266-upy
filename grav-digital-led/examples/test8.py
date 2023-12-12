"""
VK16K33 test script - 8-Digital LED Segment Display module (DFR0646)
====================================================================

For wiring, see the:
 https://github.com/mchobby/esp8266-upy/tree/master/grav-digital-led

Author(s):
* Meurisse D for MC Hobby sprl
"""
from machine import I2C
from ledseg8 import LedSegment8, VK16K33_BLINK_1HZ, VK16K33_BLINK_2HZ, VK16K33_BLINK_0HZ5
from time import sleep

# Raspberry-Pi Pico
i2c = I2C(1) # sda=GP6, scl=GP7
dis = LedSegment8( i2c ) # DFR0646 8 digit LED display

# Display integers
dis.int( 4289213 )
sleep(2)
dis.int(-4366444)
sleep(2)

# Display float
dis.float(0.101)
sleep(2)
dis.float(7890.101)
sleep(2)
dis.float(-3.14159265) # pi
# other test dis.float(-13.14159265)
sleep(2)
dis.float(6.283185307179586) # taux

# Brightness control (0..7)
for i in range( 16 ): # 0..15
	dis.brightness( i )
	dis.print( 'br  %s' % i )
	sleep(1)

d = {VK16K33_BLINK_1HZ:"1 Hz", VK16K33_BLINK_2HZ:"2 Hz", VK16K33_BLINK_0HZ5 : "0.5Hz"}
for freq in (VK16K33_BLINK_1HZ, VK16K33_BLINK_2HZ, VK16K33_BLINK_0HZ5):
		dis.print( "Bl %s" % d[freq] )
		dis.blink( freq )
		sleep( 5 )
dis.blink_off()

dis.print( "end" )
sleep(2)
# Switch display off
dis.off()
