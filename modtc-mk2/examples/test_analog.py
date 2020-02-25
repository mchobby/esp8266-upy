# Read the ANALOG INPUTS on MOD-TC-MK2-31855 device
# Only GPIO 0, 1, 2, 5, 6 offers Analog read capability (0 to 3.3V)
#
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
	iter += 1

	for pin in [0,1,2,5,6]: # PinNumber with Analog support
		value = mk2.analog_read( pin ) # 10 bits reading
		volts = value / 1023 * 3.3 # Voltage
		print( "Analog %s = %3.2f v (%4i)" % (pin,volts,value ) )
	sleep(1)
