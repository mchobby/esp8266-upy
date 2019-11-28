""" LSM303 compass+accelerometer - display of the sensor's RAW values

2019 Braccio Martin for shop.mchobby.be, support@mchobby.be - portage to MicroPython.
2016 Pololu.com - original Arduino code @ https://github.com/pololu/lsm303-arduino

The sensor outputs provided by the library are the raw 16-bit values
obtained by concatenating the 8-bit high and low accelerometer and
magnetometer data registers. They can be converted to units of g and
gauss using the conversion factors specified in the datasheet for your
particular device and full scale setting (gain).
"""

from machine import I2C
from lsm303 import LSM303, Vector
from time import sleep

# I2C bus on Pyboard and UNO-R3 for Pyboard
i2c = I2C( 2 )

compass = LSM303( i2c )
compass.enableDefault()

while True:
	acc,mag = compass.read() # Return xyz Tuples for accelerometer and magnetometer
	# Display data enclosed in the tuples
	#print( "Acc: %6d %6d %6d    Mag: %6d %6d %6d" % (
	#		acc[0], acc[1], acc[2],
	#		mag[0], mag[1], mag[2] ))

	accV = Vector( acc ) # Create Vector class populated with tuple values
	magV = Vector( mag )
	print( "Acc: %6d %6d %6d    Mag: %6d %6d %6d" % (accV.x,accV.y,accV.z , magV.x,magV.y,magV.z) )

	sleep( 0.5 )
