# Test the basic character drawing on the Sense Hat.
# As the sense-hat inherits from FramBuffer so all drawing functions and code
# around FrameBuffer can be used on the sense hat.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author: Meurisse D. for Shop.mchobby.be
#
from machine import I2C
from sensehat import SenseHat
import time

# PYBStick, Hat-Face: Sda=S3, Scl=S5
i2c = I2C( 1 )
hat = SenseHat( i2c )

# See the FrameBuffer doc @ https://docs.micropython.org/en/latest/library/framebuf.html
#
hat.clear()
# Display one charaters at the time
for ch in "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrstuvwxyz" :
	hat.clear()
	# The matrix is so small that only one char can be displayed at the time
	hat.text( ch,0,0, hat.color(125,125,125) )
	hat.update()
	time.sleep(1)
