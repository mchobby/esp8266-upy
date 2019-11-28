""" LSM303 compass+accelerometer - reads sensors and calculate a tilt-compensated
		compass heading (a float in degrees) relative to a default vector.
		The default vector is chosen to point along the surface of the PCB, in
		the direction of the top

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

# Calibration values; the default values of +/-32767 for each axis
# lead to an assumed magnetometer bias of 0. Use the Calibrate example
# program to determine appropriate values for your particular unit.

# Change the default calibration with the result of calibration.py 
# compass.m_min = Vector( -4000,-1253,-15179 )
# compass.m_max = Vector(  927,4250,-8277 )

while True:
	compass.read()

	""" When given no arguments, the heading() function returns the angular
		difference in the horizontal plane between a default vector and
		north, in degrees.

		The default vector is chosen by the library to point along the
		surface of the PCB, in the direction of the top of the text on the
		silkscreen. This is the +X axis on the Pololu LSM303D carrier and
		the -Y axis on the Pololu LSM303DLHC, LSM303DLM, and LSM303DLH
		carriers.

		To use a different vector as a reference, use the version of heading()
		that takes a vector argument; for example, use

		compass.heading( Vector(0, 0, 1) )

		to use the +Z axis as a reference. """

	heading = compass.heading() # return a float

	print( "Heading to north: %s" % heading)
	sleep( 0.1 )
