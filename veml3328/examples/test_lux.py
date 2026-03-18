""" test.py - Test of the VEML3328 light color sensor with MicroPython
		Evaluate Lux

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2026 - domeu - creation

Based on project source @ https://github.com/mchobby/esp8266-upy/veml3328
"""

from machine import I2C, Pin
from veml3328 import *
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
veml = VEML3328( i2c )

print( "Vishay VEML3328 Lux sensor" )
veml.enable()
veml.gain( 4 ) # 0.5, 1, 2, 4
veml.sensitivity( high=True )
veml.digital_gain( 4 ) # 1, 2 , 4
veml.integration( 50 ) # 50, 100, 200, 400 ms

print( "VEML3328 config: %r" % veml.config )
print( "Lux Resolution : %s lux/cnt" % veml.config.lux_res )

time.sleep( 1 )
while True:
	print( "Lux: %i" % veml.lux )
	time.sleep_ms( 200 )
