from machine import I2C
from tsl2591 import *

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Warning: manipulating gain & intergration time unappropriately
# may lead to incorrect value.
tsl = TSL2591( i2c = i2c )
# GAIN_LOW (1x gain)
# GAIN_MED (25x gain, default)
# GAIN_HIGH (428x gain)
# GAIN_MAX (9876x gain)
#tsl.gain =  GAIN_LOW # x25

# INTEGRATIONTIME_100MS (100ms, default)
# INTEGRATIONTIME_200MS
# INTEGRATIONTIME_300MS
# INTEGRATIONTIME_400MS
# INTEGRATIONTIME_500MS
# INTEGRATIONTIME_600MS
#tsl.integration_time = INTEGRATIONTIME_400MS

print( "%s lux" % tsl.lux )
print( "Infrared level (0-65535): %s" % tsl.infrared )
print( "Visible Light (0-2147483647): %s" % tsl.visible )
print( "Full spectrum (0-2147483647): %s (visible+IR)" % tsl.full_spectrum )
