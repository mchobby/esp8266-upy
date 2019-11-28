""" LSM303 compass+accelerometer - calculate calibration values for Magnetometer

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

# Min & Max vector for calibration
running_min = Vector( 32767, 32767, 32767 )
running_max = Vector( -32768, -32768, -32768 )

compass.enableDefault()

# Create vectors for easy xyz management
acc_v = Vector()
mag_v = Vector()

print( "Move around to calibrate the magnetometer min & max values")
print( "Press Ctrl+C to stop the script and catch the resulting vectors")
try:
	while True:
		acc, mag = compass.read()
		mag_v.set( mag )

		running_min.x = min(running_min.x, mag_v.x)
		running_min.y = min(running_min.y, mag_v.y)
		running_min.z = min(running_min.z, mag_v.z)

		running_max.x = max(running_max.x, mag_v.x)
		running_max.y = max(running_max.y, mag_v.y)
		running_max.z = max(running_max.z, mag_v.z)

		print( "Mag min: %6d %6d %6d    max: %6d %6d %6d" % (
					running_min.x,running_min.y,running_min.z ,
					running_max.x,running_max.y,running_max.z) )

		sleep( 0.1 )
except KeyboardInterrupt:
	pass
except: # Other errors 
	raise

print("")
print(" === Magnetometer Min & Max ===========================")
print( "running_min = %s" % running_min )
print( "running_max = %s" % running_max )
