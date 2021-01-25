# Display a mini image on the sense Sense Hat.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author: Meurisse D. for Shop.mchobby.be
#
from machine import I2C
from sensehat import SenseHat
from icons import *
import time
from random import randint

# PYBStick, Hat-Face: Sda=S3, Scl=S5
# Pyboard, Sda=X10, Scl=X9
i2c = I2C( 1 )
# Raspberry-Pi Pico, Sda=GP8, Scl=GP9
#i2c = I2C( 0 )
hat = SenseHat( i2c )

# See the FrameBuffer doc @ https://docs.micropython.org/en/latest/library/framebuf.html

# Show a pulsing heart
red = hat.color(200, 0, 0)
for i in range(10):
	hat.clear()
	hat.icon( HEART, color=red )
	hat.update()
	time.sleep(1)

	hat.clear()
	hat.icon( HEART_SMALL, color=red )
	hat.update()
	time.sleep(1)

# Iterate every icons with random color
while True:
	for icon in all_icons:
		hat.clear()
		hat.icon( icon, color=hat.color(randint(0,255),randint(0,255),randint(0,255) ) )
		hat.update()
		time.sleep(1)
