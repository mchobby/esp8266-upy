# Read the data from Pressure sensor (Pressure, temperature ) and
#                display it on REPL
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
# i2c = I2C( 1 )
# Raspberry-Pi Pico, Sda=GP8, Scl=GP9
i2c = I2C( 0 )
hat = SenseHat( i2c )

while True:
	# Read Pressure and Temperature
	print( "%8.2f hPa, %3.1f Celcius" % hat.pressure )
	time.sleep( 1 )
