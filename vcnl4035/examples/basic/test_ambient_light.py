""" Vishay VCNL4035 sensor for MicroPython

    Test the Ambient Light reading
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

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.AMBIENT_LIGHT )

# The default 100ms integration time can measure from 0 to 2096 lux.
# Reducing integration time down to 50ms can measure up to 4192 lux.
# Increasing integration time to 200,400,500,600,700,800 ms can be used 
#    to measure lower luminosity environment.
# Note than higher integration time will reduce the m&ximum detection range.
#
# sensor.set_als_integration( VCNL4035_ALS_IT.ALS_IT_400ms )

# double the sensitivity (this double the Lux-Range)
#
# sensor.set_als_sensitivity( VCNL4035_ALS_NS.ALS_NS_X2 )

# double the dynamic range (this double, once again, the Lux-Range)
#
# sensor.set_als_dynamic_range( VCNL4035_ALS_HD.ALS_HD_X2 )



print( "VCLN4035 version", sensor.version )
print( "Range = 0..%i lux" % sensor.lux_range )


while True:
	print("-"*20)
	# Raw reading 
	data = sensor.read_data() 
	print( "Raw:", data )
	# Lux reading
	print( "Lux:", sensor.lux )
	time.sleep_ms(500)
