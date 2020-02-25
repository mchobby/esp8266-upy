# Continously toggle the state of a GPIO configured as output
#
from machine import I2C, Pin
from modtc_mk2 import MODTC_MK2
from time import sleep

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk2 = MODTC_MK2( i2c )

# The GPIO to test
GPIO = 6

print( "Toggling state of GPIO %s" % GPIO )
mk2.pin_mode( GPIO, Pin.OUT )
while True:
	print( "ON" )
	mk2.digital_write( GPIO, True )
	sleep( 1 )
	print( "off" )
	mk2.digital_write( GPIO, False )
	sleep( 1 )
