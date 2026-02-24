# Basic demo for accelerometer/gyro readings from ISM330DHCX
#
# Based on Adafruit Implementation for Arduino
# https://github.com/adafruit/Adafruit_LSM6DS/blob/master/examples/adafruit_ism330dhcx_test/adafruit_ism330dhcx_test.ino

from micropython import const
from lsm6ds import LSM6DSOX, LSM6DS_CTRL3_C
from sensor import *

ISM330DHCX_CHIP_ID = const(0x6B)

class ISM330DHCX( LSM6DSOX ):
	def __init__( self, i2c, address=0x6A ):
		super().__init__( i2c, address, whoami=ISM330DHCX_CHIP_ID )

	def _init( self, sensor_id ): # Named address in ancestor
		print( 'ism330:_init()' )
		self._sensorid_accel = sensor_id
		self._sensorid_gyro  = sensor_id+1
		self._sensorid_temp  = sensor_id+2

		self.reset()

		super()._init( sensor_id )

		# set the Block Data Update bit
		# this prevents MSB/LSB data registers from being updated until both are read
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL3_C, self.buf1 )  # Buf1 owned by ancestor
		value = self.buf1[0] | 0b01000000
		self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL3_C, self.buf1 )

		return True

