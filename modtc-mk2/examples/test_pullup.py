# Read the state GPIO INPUTS on MOD-TC-MK2-31855 device
# Activate a PULL-UP on GPIO2 then read the status of the GPIO 2
#
from machine import I2C, Pin
from modtc_mk2 import MODTC_MK2
from time import sleep

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk2 = MODTC_MK2( i2c )

print( "Set GPIO 2 as input with Pull-up" )
mk2.pin_mode( 2, Pin.IN )
mk2.pullup( 2, True  )
while True:
	print( "GPIO 2 : %s" % ("3.3v" if mk2.digital_read(2) else "Gnd") )
	sleep( 1 )
