# Read the temperature from the MOD-TC-MK2-31855 device
# It reads (internal_temperature & external_temperature)
#
# external_temperature correspond to the Type-K thermocouple
#
from machine import I2C
from modtc_mk2 import MODTC_MK2
from time import sleep

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk2 = MODTC_MK2( i2c )


iter = 1
while True:
	print( '--- %i %s' % (iter, '-'*40) )
	# Internal & External temperatures
	temp_in, temp_ext = mk2.temperatures
	# display
	print( "Internal Temp = %s" % temp_in )
	print( "External Temp = %s" % temp_ext )
	iter += 1
	sleep(1)
