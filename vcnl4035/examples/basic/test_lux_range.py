""" Vishay VCNL4035 sensor for MicroPython

    Evaluate the Ambient Light LUX RANGE for various integration time
    Use the default setting

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   implementation by MCHobby
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_ALS_IT, VCNL4035_ALS_NS, VCNL4035_ALS_HD
import time

INTEGRATION_TIMES = [ \
	(VCNL4035_ALS_IT.ALS_IT_50ms  , '50 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_100ms , '100 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_200ms , '200 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_400ms , '400 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_500ms , '500 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_600ms , '600 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_700ms , '700 ms' ), \
	(VCNL4035_ALS_IT.ALS_IT_800ms , '800 ms' ) ]

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.AMBIENT_LIGHT )

# double the sensitivity (this double the Lux-Range)
#
# sensor.set_als_sensitivity( VCNL4035_ALS_NS.ALS_NS_X2 )

# double the dynamic range (this double, once again, the Lux-Range)
#
# sensor.set_als_dynamic_range( VCNL4035_ALS_HD.ALS_HD_X2 )



print( "VCLN4035 version", sensor.version )

mul_hd = 1 if sensor.settings.als_conf_1.als_hd==VCNL4035_ALS_HD.ALS_HD_X1 else 2
mul_ns = 1 if sensor.settings.als_conf_2.als_ns==VCNL4035_ALS_NS.ALS_NS_X1 else 2

print( "Dynamic Range setting : *%i" % mul_hd )
print( "Sensitivity setting   : *%i" % mul_ns )

# The default 100ms integration time can measure from 0 to 2096 lux.
# Reducing integration time down to 50ms can measure up to 4192 lux.
# Increasing integration time to 200,400,500,600,700,800 ms can be used 
#    to measure lower luminosity environment.
# Note than higher integration time will reduce the m&ximum detection range.
#
for als_it, label in INTEGRATION_TIMES:
	sensor.set_als_integration( als_it )
	print( "%6s => 0..%5i lux range" % (label,sensor.lux_range) )

print( "" )
print( "That's all done!" )
