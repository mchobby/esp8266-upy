# Read the device ID from MOD-TC-MK2-31855
#
from machine import I2C
from modtc_mk2 import MODTC_MK2

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk2 = MODTC_MK2( i2c )

print( "Device ID = 0x%x" % mk2.device_id )
