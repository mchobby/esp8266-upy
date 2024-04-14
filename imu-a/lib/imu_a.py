""" imu_a.py - 9DOF IMU library for LSM6DSOx and LIS3MDL for MicroPython

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2024 - domeu - extraction for imu_a.py
15 jun 2022 - domeu - initial portage from ZumoIMU.cpp

Based on project source @ https://github.com/mchobby/micropython-zumo-robot
"""

__version__ = "0.0.2"
__repo__ = "https://github.com/esp8266-upy/imu-a/lib/imu_a.py"

from micropython import const
import struct
import math
import time

#LSM303DLHC_ACC_ADDR = const( 0b0011001 )
#LSM303DLHC_MAG_ADDR = const( 0b0011110 )
#LSM303D_ADDR   = const( 0b0011101 )
#L3GD20H_ADDR   = const( 0b1101011 )
LSM6DS33_ADDR  = const( 0x6A ) # or 0X6B
LIS3MDL_ADDR   = const( 0x1C ) # or 01xD

# Register address
#LSM303DLHC_REG_CTRL_REG1_A  = const( 0x20 )
#LSM303DLHC_REG_CTRL_REG4_A  = const( 0x23 )
#LSM303DLHC_REG_STATUS_REG_A = const( 0x27 )
#LSM303DLHC_REG_OUT_X_L_A    = const( 0x28 )

#LSM303DLHC_REG_CRA_REG_M    = const( 0x00 )
#LSM303DLHC_REG_CRB_REG_M    = const( 0x01 )
#LSM303DLHC_REG_MR_REG_M     = const( 0x02 )
#LSM303DLHC_REG_OUT_X_H_M    = const( 0x03 )
#LSM303DLHC_REG_SR_REG_M     = const( 0x09 )

#LSM303D_REG_STATUS_M  = const( 0x07 )
#LSM303D_REG_OUT_X_L_M = const( 0x08 )
#LSM303D_REG_WHO_AM_I  = const( 0x0F )
#LSM303D_REG_CTRL1     = const( 0x20 )
#LSM303D_REG_CTRL2     = const( 0x21 )
#LSM303D_REG_CTRL5     = const( 0x24 )
#LSM303D_REG_CTRL6     = const( 0x25 )
#LSM303D_REG_CTRL7     = const( 0x26 )
#LSM303D_REG_STATUS_A  = const( 0x27 )
#LSM303D_REG_OUT_X_L_A = const( 0x28 )

#L3GD20H_REG_WHO_AM_I = const( 0x0F )
#L3GD20H_REG_CTRL1    = const( 0x20 )
#L3GD20H_REG_CTRL4    = const( 0x23 )
#L3GD20H_REG_STATUS   = const( 0x27 )
#L3GD20H_REG_OUT_X_L  = const( 0x28 )

LSM6DS33_REG_WHO_AM_I   = const( 0x0F )
LSM6DS33_REG_CTRL1_XL   = const( 0x10 )
LSM6DS33_REG_CTRL2_G    = const( 0x11 )
LSM6DS33_REG_CTRL3_C    = const( 0x12 )
LSM6DS33_REG_STATUS_REG = const( 0x1E )
LSM6DS33_REG_OUTX_L_G   = const( 0x22 )
LSM6DS33_REG_OUTX_L_XL  = const( 0x28 )

LIS3MDL_REG_WHO_AM_I   = const( 0x0F )
LIS3MDL_REG_CTRL_REG1  = const( 0x20 )
LIS3MDL_REG_CTRL_REG2  = const( 0x21 )
LIS3MDL_REG_CTRL_REG3  = const( 0x22 )
LIS3MDL_REG_CTRL_REG4  = const( 0x23 )
LIS3MDL_REG_STATUS_REG = const( 0x27 )
LIS3MDL_REG_OUT_X_L    = const( 0x28 )

#IMU_TYPE_Unknown = 0
#IMU_TYPE_LSM303DLHC = 1       # LSM303DLHC accelerometer + magnetometer
#IMU_TYPE_LSM303D_L3GD20H = 2  # LSM303D accelerometer + magnetometer, L3GD20H gyro

#IMU_TYPE_LSM6DS33_LIS3MDL = 3 # LSM6DS33 gyro + accelerometer, LIS3MDL magnetometer


TEST_REG_ERROR  = const( -1 )

#LSM303D_WHO_ID  = const( 0x49 )
#L3GD20H_WHO_ID  = const( 0xD7 )
LSM6DS33_WHO_ID = const( 0x6A )
LSM6DSOX_WHO_ID = const( 0x6C )
LIS3MDL_WHO_ID  = const( 0x3D )

class Vector:
	__slots__ = ['x','y','z']

	def __init__( self, x=None, y=None, z=None):
		"""" Create and init the vector with x,y,z parameters. x can also be a tuple with (x,y,z) values."""
		if type(x)==tuple: # Feeded with a tuple of 3 parameter (x,y,z)
			assert len(x)==3, "3 position required in tuple!"
			self.x = x[0]
			self.y = x[1]
			self.z = x[2]
		else:
			# Feeded with 3 NAMED parameter
			self.x=x
			self.y=y
			self.z=z

	def __repr__( self ):
		return "<%s %s,%s,%s>" % (self.__class__.__name__, self.x, self.y, self.z)

	def set( self, x=None, y=None, z=None ):
		""" Update the values which are not None in one operation. x can also be a tuple with (x,y,z) values."""
		if type(x)==tuple: # Feeded with a tuple of 3 parameter (x,y,z)
			assert len(x)==3, "3 position required in tuple!"
			if x[0]: self.x = x[0]
			if x[1]: self.y = x[1]
			if x[2]: self.z = x[2]
		else:
			# Feeded with 3 NAMED parameter
			if x: self.x = x
			if y: self.y = y
			if z: self.z = z

	@property
	def values( self ):
		return (self.x,self.y,self.z)

	def cross( self, b, out ):
		""" Cross operation with b Vector.  Update the out Vector """
		# vector_cross( a, b, out ) with a being the self vector
		# template <typename Ta, typename Tb, typename To> static void vector_cross(const vector<Ta> *a, const vector<Tb> *b, vector<To> *out);
		out.x = (self.y * b.z) - (self.z * b.y)
		out.y = (self.z * b.x) - (self.x * b.z)
		out.z = (self.x * b.y) - (self.y * b.x)

	def dot( self, b ):
		""" Dot operation with b Vector. Returns float """
		# def vector_dot( a, b ) with a being the self vector
		return (self.x * b.x) + (self.y * b.y) + (self.z * b.z)

	def normalize( self ):
		""" Normalize the vector and update its x,y,z values """
		mag = sqrt(self.dot(self)) # produce a float
		self.x /= mag
		self.y /= mag
		self.z /= mag

class IMU_A:
	""" Interfaces with the inertial sensors on the LSM6DS33 & LIS3MDL """
	def __init__( self, i2c, lsm6_addr=LSM6DS33_ADDR, lis3_addr=LIS3MDL_ADDR ):
		self.i2c = i2c
		self.lsm6_addr = lsm6_addr
		self.lis3_addr = lis3_addr
		self.a = Vector( 0, 0, 0 ) # Int16, Raw Accelerometer reading
		self.g = Vector( 0, 0, 0 ) # Int16, Raw Gyro reading
		self.m = Vector( 0, 0, 0 ) # Int16, Raw magnetometer reading
		#self._imu_type = IMU_TYPE_Unknown
		self.buf1 = bytearray( 1 )
		self.buf6 = bytearray( 6 )

		if ( self.__test_reg( self.lsm6_addr, LSM6DS33_REG_WHO_AM_I) not in(LSM6DSOX_WHO_ID,LSM6DS33_WHO_ID) ):
		 	raise Exception( "IMU lsm6 detection failed" )
		if self.__test_reg( self.lis3_addr,  LIS3MDL_REG_WHO_AM_I) !=  LIS3MDL_WHO_ID :
			raise Exception( "IMU lis3 detection failed" )

		# initialize the default
		self.enable_default()


	def enable_default( self ):
		# --- Accelerometer ---
		# 0x30 = 0b00110000
		# ODR = 0011 (52 Hz (high performance)); FS_XL = 00 (+/- 2 g full scale)
		self.__write_reg(self.lsm6_addr, LSM6DS33_REG_CTRL1_XL, 0x30)
		# --- Gyro ---
		# 0x50 = 0b01010000
		# ODR = 0101 (208 Hz (high performance)); FS_G = 00 (+/- 245 dps full scale)
		self.__write_reg(self.lsm6_addr, LSM6DS33_REG_CTRL2_G, 0x50)
			# --- Accelerometer + Gyro ---
		# 0x04 = 0b00000100
		# IF_INC = 1 (automatically increment register address)
		self.__write_reg(self.lsm6_addr, LSM6DS33_REG_CTRL3_C, 0x04)
		# --- Magnetometer ---
		# 0x70 = 0b01110000
		# OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR)
		self.__write_reg(self.lis3_addr, LIS3MDL_REG_CTRL_REG1, 0x70)
		# 0x00 = 0b00000000
		# FS = 00 (+/- 4 gauss full scale)
		self.__write_reg(self.lis3_addr, LIS3MDL_REG_CTRL_REG2, 0x00)
		# 0x00 = 0b00000000
		# MD = 00 (continuous-conversion mode)
		self.__write_reg(self.lis3_addr, LIS3MDL_REG_CTRL_REG3, 0x00)
		# 0x0C = 0b00001100
		# OMZ = 11 (ultra-high-performance mode for Z)
		self.__write_reg(self.lis3_addr, LIS3MDL_REG_CTRL_REG4, 0x0C)


	def __test_reg( self, addr, reg ):
		try:
			self.i2c.readfrom_mem_into( addr, reg, self.buf1 )
			return self.buf1[0]
		except:
			return TEST_REG_ERROR

	def __read_axes( self, addr, first_reg, vector, endianness="<hhh" ):
		# read 16 bits axes and populate "vector", assume we are in little-endian by default
		self.i2c.readfrom_mem_into( addr, first_reg, self.buf6 )
		vector.x, vector.y, vector.z = struct.unpack( endianness, self.buf6 )

	def __write_reg( self, addr, reg, value ):
		self.buf1[0] = value
		self.i2c.writeto_mem( addr, reg, self.buf1 )


	def config_for_compass_heading( self ):
		# Configures the sensors with settings optimized for determining a
		# compass heading with the magnetometer

		# --- Magnetometer ---
		# 0x7C = 0b01111100
		# OM = 11 (ultra-high-performance mode for X and Y); DO = 111 (80 Hz ODR)
		self.__write_reg(self.lis3_addr, LIS3MDL_REG_CTRL_REG1, 0x7C)


	def read_acc( self ):
		#  Reads the 3 accelerometer channels and stores them in vector a
		# assumes register address auto-increment is enabled (IF_INC in CTRL3_C)
		self.__read_axes( self.lsm6_addr, LSM6DS33_REG_OUTX_L_XL, self.a )


	def read_mag( self ):
		# set MSB of register address for auto-increment
		self.__read_axes( self.lis3_addr, LIS3MDL_REG_OUT_X_L | (1 << 7), self.m )


	def read_gyro( self ):
		# assumes register address auto-increment is enabled (IF_INC in CTRL3_C)
		self.__read_axes( self.lsm6_addr, LSM6DS33_REG_OUTX_L_G, self.g )

	def read( self ):
		# read all 3 sensors
		self.read_acc()
		self.read_gyro()
		self.read_mag()

	@property
	def mag_data_ready( self ):
		return self.__read_reg( self.lis3_addr, LIS3MDL_REG_STATUS_REG) & 0x08 > 0

	@property
	def acc_data_ready( self ):
		return self.__read_reg( self.lsm6_addr, LSM6DS33_REG_STATUS_REG) & 0x01 > 0

	@property
	def gyro_data_ready( self ):
		return self.__read_reg( self.lsm6_addr, LSM6DS33_REG_STATUS_REG) & 0x02 > 0
