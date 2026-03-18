""" test_high_luminosity.py - Test of the VEML3328 light color sensor with MicroPython

    Can measure up to 150 000 lux with appropriate configuration (Digital_Gain=1, Gain=0.5, 
      Sensitivity=False, integration=50ms).
    
    Important Remark: at low sensitivity, low luminosity measurement are fairly unprecise!

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2026 - domeu - creation

Based on project source @ https://github.com/mchobby/esp8266-upy/veml3328
"""

__version__ = "0.0.1"
__repo__ = "https://github.com/esp8266-upy/mchobby/esp8266-upy/veml3328"

from machine import I2C, Pin
from veml3328 import *
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
veml = VEML3328( i2c )

print( "Vishay VEML3328 RGBCIR color sensor" )
print( "  value [0..65535]" )

# In high luminosity environment, it is recommanded to switch the sensor
# to LOW SENSITIVITY and DIGITAL_GAIN=1 (higher value not allowed).
#
# User can act are sensor GAIN and integration time.
#
veml.enable()
veml.gain( 4 ) # Sensor Gain: 0.5, 1, 2, 4
veml.sensitivity( high=False ) # Low sensitivity
veml.integration( 400 ) # 50, 100, 200, 400 ms
print( "VEML configuration: %r " % veml.config )
print( "Lux resolution    : %r " % veml.config.lux_res )
time.sleep( 1 )
while True:
	# Enable on purpose
	#
	# print( "Red  : %i" % veml.red )
	print( "Green: %i" % veml.green )
	# print( "Blue : %i" % veml.blue )
	print( "Clear: %i" % veml.clear )
	print( "IR   : %i" % veml.ir )
	print( "Lux  : %i" % veml.lux )
	print( "-"*40 )
	time.sleep_ms( 200 )
