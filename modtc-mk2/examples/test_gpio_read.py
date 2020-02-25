# Read the state GPIO INPUTS on MOD-TC-MK2-31855 device
# All GPIOs supports inputs
#
from machine import I2C, Pin
from modtc_mk2 import MODTC_MK2
from time import sleep

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk2 = MODTC_MK2( i2c )

for gpio in range( 7 ): # from 0 to 6
	mk2.pin_mode( gpio, Pin.IN )

# Activate Pullup as needed
# mk2.pullup( gpio=0, enable=True )
# mk2.pullup( gpio=1, enable=True )
# mk2.pullup( gpio=2, enable=True )
# mk2.pullup( gpio=4, enable=False ) # disable the Pullup activated @ startup

iter = 1
while True:
	print( '--- %i %s' % (iter, '-'*40) )
	iter += 1

	for gpio in range( 7 ): # 0..6
		print( "GPIO %s = %s" % (gpio, mk2.digital_read( gpio ) ) )
	sleep(1)
