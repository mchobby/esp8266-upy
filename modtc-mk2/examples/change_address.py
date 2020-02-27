# Change the I2C address of a given MOD-TC-MK2-31855
#
from machine import I2C
from modtc_mk2 import MODTC_MK2

FROM_ADDRESS = 0x23 # 0x23 is the default address of MOD-TC-MK2-31855
TO_ADDRESS   = 0x25

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)

print( "I2C scan..." )
print( ", ".join( [ "0x%x" % value for value in i2c.scan() ] ))
print( "" )

print( "Connecting to address 0x%x" % FROM_ADDRESS )
mk2 = MODTC_MK2( i2c, address=FROM_ADDRESS )

print( "Change to address 0x%x" % TO_ADDRESS )
mk2.change_address( new_address=TO_ADDRESS )

print( "Power cycle the board and make")
print( "a new I2C scan to check the address." )
