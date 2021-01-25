# Test scroll a text message on the Sense Hat.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author: Meurisse D. for Shop.mchobby.be
#
from machine import I2C
from sensehat import *
from icons import *
import time

# PYBStick, Hat-Face: Sda=S3, Scl=S5
# Pyboard, Sda=X10, Scl=X9
i2c = I2C( 1 )
# Raspberry-Pi Pico, Sda=GP8, Scl=GP9
# i2c = I2C( 0 )
hat = SenseHat( i2c )

# See the FrameBuffer doc @ https://docs.micropython.org/en/latest/library/framebuf.html
#
hat.clear()
hat.scroll( "Sense-Hat, PYBStick & MicroPython" )

# Show a pulsing heart
red = hat.color(200, 0, 0)
for i in range(5):
	hat.clear()
	hat.icon( HEART, color=red )
	hat.update()
	time.sleep(0.5)

	hat.clear()
	hat.icon( HEART_SMALL, color=red )
	hat.update()
	time.sleep(0.5)

# random pixel display
i = 0
from random import randint
while i < 500:
	hat.pixel( randint(0,7), randint(0,7), hat.color(randint(0,255),randint(0,255),randint(0,255) ) )
	hat.update()
	i+=1

# Read Pressure and Temperature
hat.scroll( "%8.2f hPa, %3.1f Celcius" % hat.pressure )

hat.clear()
# Display one charaters at the time
while True:
	hat.clear(update=False) # Just clear the FrameBuffer
	j = hat.joystick
	if j == JOY_UP:
		hat.icon(ARROW_N)
	elif j == JOY_DOWN:
		hat.icon(ARROW_S)
	elif j == JOY_RIGHT:
		hat.icon(ARROW_W)
	elif j == JOY_LEFT:
		hat.icon(ARROW_E)
	elif j == JOY_ENTER:
		hat.icon(TARGET)
	hat.update()
