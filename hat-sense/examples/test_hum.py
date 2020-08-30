# Read the data from Humidity sensor (Relative Humidity, temperature ) and
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
i2c = I2C( 1 )
hat = SenseHat( i2c )

while True:
	# Read Humidity and Temperature
	print( "%3.1f %%RH, %3.1f Celcius" % hat.humidity )
	time.sleep( 1 )
