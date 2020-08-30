# Test the basic drawing function on the Sense Hat.
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
hat.fill( hat.color(255,0,0) ) # Red
hat.update()
time.sleep(1)

hat.fill( hat.color(0,255,0) ) # Green
hat.update()
time.sleep(1)

hat.fill( hat.color(0,0,255) ) # Blue
hat.update()
time.sleep(1)

# Draw nested rectangle
hat.clear()
hat.rect( 0,0, 8,8, hat.color(255,0,0) ) # Outside = Red
hat.rect( 1,1, 6,6, hat.color(0,255,0) ) # Green
hat.rect( 2,2, 4,4, hat.color(0,0,255) ) # Blue
hat.rect( 3,3, 2,2, hat.color(255,255,0) ) # Yellow
hat.update()
time.sleep(2)

# from Top to Bottom
for y in range(8):
	hat.clear( update=False ) # Just clear internal memory
	hat.hline(0, y, 8, hat.color(238,130,238) ) # Violet
	hat.update()
	time.sleep(0.200)

# from Left to right
hat.clear()
for x in range(8):
	hat.clear( update=False )
	hat.vline(x, 0, 8, hat.color(91,60,17) ) # brown
	hat.update()
	time.sleep(0.200)

hat.clear()

# random pixel display
from random import randint
while True:
	hat.pixel( randint(0,7), randint(0,7), hat.color(randint(0,255),randint(0,255),randint(0,255) ) )
	hat.update()
