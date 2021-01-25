# Read the data from accelerometer sensor (x,y,z) and display it on REPL
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author: Meurisse D. for Shop.mchobby.be
#
from machine import I2C
from sensehat import *
import time

# PYBStick, Hat-Face: Sda=S3, Scl=S5
# Pyboard, Sda=X10, Scl=X9
i2c = I2C( 1 )
# Raspberry-Pi Pico, Sda=GP8, Scl=GP9
# i2c = I2C( 0 )
hat = SenseHat( i2c )

while True:
	# Read Accelerometer
	print( "x: %i , y: %i , z: %i" % hat.acc )
	time.sleep( 0.3 )
