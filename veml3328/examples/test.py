""" test.py - Test of the VEML3328 light color sensor with MicroPython

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2026 - domeu - creation

Based on project source @ https://github.com/mchobby/esp8266-upy/veml3328
"""

from machine import I2C, Pin
from veml3328 import *
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
veml = VEML3328( i2c )

print( "Vishay VEML3328 RGBCIR color sensor" )
print( "  value [0..65535]" )
veml.enable()
veml.gain( 4 ) # 0.5, 1, 2, 4
veml.sensitivity( high=True )
veml.digital_gain(4 ) # 1, 2 , 4
veml.integration( 50 ) # 50, 100, 200, 400 ms

time.sleep( 1 )
while True:
	print( "Red  : %i" % veml.red )
	print( "Green: %i" % veml.green )
	print( "Blue : %i" % veml.blue )
	print( "Clear: %i" % veml.clear ) # Clear Channel
	print( "IR   : %i" % veml.ir )    # IR Channel
	print( "-"*40 )
	time.sleep_ms( 100 )
