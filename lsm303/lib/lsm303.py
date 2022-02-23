# The MIT License (MIT)
#
# Copyright (c) 2019 Braccio Martin for MCHobby.be - backport to MicroPython.
# Copyright (c) Adafruit Industries & Pololu - original mixed sources for this driver
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`LSM303` - LSM303 Compass + accelerometer I2C
=============================================

MicroPython library to support LSM303 sensor.
Made to be compatible with Zumo Robot from Pololu


* Author(s): Braccio Martin for MCHobby.be - backport to MicroPython
* Author(s): mixed source from Adafruit & Pololu

Implementation Notes
--------------------
This MicroPython port is based on:
- Adafruit LSM303 for CircuitPython @ https://github.com/adafruit/Adafruit_CircuitPython_LSM303_Accel
- Pololu LSM303 for Arduino @ https://github.com/pololu/lsm303-arduino

**Hardware:**

* Adafruit `Triple-axis Accelerometer+Magnetometer (Compass) Board - LSM303
  <https://www.adafruit.com/products/1120>`_ (Product ID: 1120)
* Pololu `LSM303D 3D Compass and Accelerometer Carrier with Voltage Regulator
  <https://www.pololu.com/product/2127>`

**Software and Dependencies:**

* MicroPython machin.I2C

**Notes:**

#.

"""
from math import sqrt, pi, atan2
from machine import I2C
from micropython import const
import struct

_ADDRESS        =const(0x1D)    #1 1101   (29)

TEMP_OUT_L      = const(0x05)
TEMP_OUT_H      = const(0x06)
STATUS_M        = const(0x07)
OUT_X_L_M       = const(0x08)
OUT_X_H_M       = const(0x09)
OUT_Y_L_M       = const(0x0A)
OUT_Y_H_M       = const(0x0B)
OUT_Z_L_M       = const(0x0C)
OUT_Z_H_M       = const(0x0D)

WHO_AM_I        = const(0x0F)

INT_CTRL_M      = const(0x12)
INT_SRC_M       = const(0x13)
INT_THS_L_M     = const(0x14)
INT_THS_H_M     = const(0x15)
OFFSET_X_L_M    = const(0x16)
OFFSET_X_H_M    = const(0x17)
OFFSET_Y_L_M    = const(0x18)
OFFSET_Y_H_M    = const(0x19)
OFFSET_Z_L_M    = const(0x1A)
OFFSET_Z_H_M    = const(0x1B)

REFERENCE_X     = const(0x1C)
REFERENCE_Y     = const(0x1D)
REFERENCE_Z     = const(0x1E)
CTRL0           = const(0x1F)
CTRL1           = const(0x20)
CTRL2           = const(0x21)
CTRL3           = const(0x22)
CTRL4           = const(0x23)
CTRL5           = const(0x24)
CTRL6           = const(0x25)
CTRL7           = const(0x26)

STATUS_A        = const(0x27)
OUT_X_L_A       = const(0x28)
OUT_X_H_A       = const(0x29)
OUT_Y_L_A       = const(0x2A)
OUT_Y_H_A       = const(0x2B)
OUT_Z_L_A       = const(0x2C)
OUT_Z_H_A       = const(0x2D)

FIFO_CTRL       = const(0x2E)
FIFO_SRC        = const(0x2F)
IG_CFG1         = const(0x30)
IG_SRC1         = const(0x31)
IG_THS1         = const(0x32)
IG_DUR1         = const(0x33)
IG_CFG2         = const(0x34)
IF_SRC2         = const(0x35)
IG_THS2         = const(0x36)
IG_DUR2         = const(0x37)
CLICK_CFG       = const(0x38)
CLICK_SRC       = const(0x39)
CLICK_THS       = const(0x3A)

TIME_LIMIT      = const(0x3B)
TIME_LATENCY    = const(0x3C)
TIME_WINDOW     = const(0x3D)
Act_THS         = const(0x3E)
Act_DUR         = const(0x3F)

#magnetometre data rates
MAGRATE_3_1     = const(0x00)
MAGRATE_6_2     = const(0x01)
MAGRATE_12_5    = const(0x02)
MAGRATE_25      = const(0x03)
MAGRATE_50      = const(0x04)
MAGRATE_100     = const(0x05)

#Magnetometer gauss
MAGGAIN_2       =const(0x00)
MAGGAIN_4       =const(0x01)
MAGGAIN_8       =const(0x02)
MAGGAIN_12      =const(0x03)

#accelometre data rates   (CTRL1)
ACCRATE_0       = const(0x00)
ACCRATE_3_1     = const(0x01)
ACCRATE_6_2     = const(0x02)
ACCRATE_12_5    = const(0x03)
ACCRATE_25      = const(0x04)
ACCRATE_50      = const(0x05)
ACCRATE_100     = const(0x06)
ACCRATE_200     = const(0x07)
ACCRATE_400     = const(0x08)
ACCRATE_800     = const(0x09)
ACCRATE_1600    = const(0x0A)

#accelerometre gaude
ACCGAIN_2       = const(0x00)
ACCGAIN_4       = const(0x01)
ACCGAIN_6       = const(0x02)
ACCGAIN_8       = const(0x03)
ACCGAIN_16      = const(0x04)

# Conversion constants
_LSM303ACCEL_MG_LSB        = 16704.0
_GRAVITY_STANDARD          = 9.80665      # Earth's gravity in m/s^2
_GAUSS_TO_MICROTESLA       = 100.0        # Gauss to micro-Tesla multiplier

#Acceleration anti-alias filter Bandwidth. CTRL2 bits 7-6
ALIAS_FILTER_773            = const(0x00)
ALIAS_FILTER_194            = const(0x01)
ALIAS_FILTER_362            = const(0x02)
ALIAS_FILTER_50             = const(0x03)

# ------------------------------------------------------------------------------
#    VECTOR
# ------------------------------------------------------------------------------
#template <typename T> struct vector { T x, y, z; };
class Vector( object ):
	__slots__ = ['x','y','z']

	def __init__( self, x=None, y=None, z=None):
		""" Create and init the vector with x,y,z parameters.
			x can also be a tuple with (x,y,z) values."""
		# Feeded with a tuple of 3 parameter (x,y,z)
		if type(x)==tuple:
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
		""" Update the values which are not None in one operation.
		 	x can also be a tuple with (x,y,z) values."""
		# Feeded with a tuple of 3 parameter (x,y,z)
		if type(x)==tuple:
			assert len(x)==3, "3 position required in tuple!"
			if x[0]: self.x = x[0]
			if x[1]: self.y = x[1]
			if x[2]: self.z = x[2]
		else:
			# Feeded with 3 NAMED parameter
			if x: self.x = x
			if y: self.y = y
			if z: self.z = z

	def cross( self, b, out ):
		""" Cross operation with b Vector.
			Update the out Vector """
		# vector_cross( a, b, out ) with a being the self vector
		# template <typename Ta, typename Tb, typename To> static void vector_cross(const vector<Ta> *a, const vector<Tb> *b, vector<To> *out);
		out.x = (self.y * b.z) - (self.z * b.y)
		out.y = (self.z * b.x) - (self.x * b.z)
		out.z = (self.x * b.y) - (self.y * b.x)

	def dot( self, b ):
		""" Dot operation with b Vector.
			Returns float """
		# def vector_dot( a, b ) with a being the self vector
		# template <typename Ta, typename Tb> static float vector_dot(const vector<Ta> *a, const vector<Tb> *b);
		return (self.x * b.x) + (self.y * b.y) + (self.z * b.z)

	def normalize( self ):
		""" Normalize the vector and update its x,y,z values """
		# static void vector_normalize(vector<float> *a);
		mag = sqrt(self.dot(self)) # produce a float
		self.x /= mag
		self.y /= mag
		self.z /= mag

# ------------------------------------------------------------------------------
#    LSM303
# ------------------------------------------------------------------------------
class LSM303( object ):
	""" MicroPython class to manage the LSM303. """

	# Class-level buffer for reading and writing data with the sensor.
	# This reduces memory allocations but means the code is not re-entrant or
	# thread safe!
	_BUFFER = bytearray(6)

	def __init__(self, i2c, address=_ADDRESS ): # 0x29
		self._address = address
		self._device = i2c

		self._write_u8( CTRL1, 0x27)  # Enable the accelerometer

		self._lsm303mag_gauss_lsb_xy = 1100.0    # registre _REG_MAG_CRB_REG_M: 3 bites de poids fort 001
		self._lsm303mag_gauss_lsb_z = 980.0
		self._mag_rate = MAGRATE_6_2
		self._mag_gain = MAGGAIN_2
		self.m_min = Vector(-32767, -32767, -32767 ) # Default min calibration for compass
		self.m_max = Vector( +32767, +32767, +32767) # Default min calibration for compass


	def enableDefault(self):
		#accelerometer
		#0x00 = 0b00000000
		#AFS = 0 (+/- 2 g full scale)
		self._write_u8( CTRL2, 0x00)
		#0x57 = 0b01010111
		#AODR = 0101 (50 Hz ODR); AZEN = AYEN = AXEN = 1 (all axes enabled)
		self._write_u8( CTRL1, 0x57)   #101 0111   3 acc-axis enable and data rate a 50Hz
		#megnetometer
		#0x64 = 0b01100100
		#M_RES = 11 (high resolution mode); M_ODR = 001 (6.25 Hz ODR)
		self._write_u8( CTRL5,0x64)
		#0x20 = 0b00100000
		#MFS = 01 (+/- 4 gauss full scale)
		self._write_u8( CTRL6,0x20)
		#0x00 = 0b00000000
		#MLP = 0 (low power mode off); MD = 00 (continuous-conversion mode)
		self._write_u8( CTRL7,0x00)

	@property
	def raw_acceleration(self):
		"""The raw accelerometer sensor values.
		A 3-tuple of X, Y, Z axis values that are 16-bit signed integers.
		"""
		self._read_bytes(OUT_X_L_A, 6, self._BUFFER)
		return struct.unpack_from('>hhh', self._BUFFER[0:6])

	@property
	def acceleration(self):
		"""The processed accelerometer sensor values.
		A 3-tuple of X, Y, Z axis values in meters per second squared that are signed floats.
		"""
		raw_accel_data = self.raw_acceleration
		return tuple([n / _LSM303ACCEL_MG_LSB * _GRAVITY_STANDARD for n in raw_accel_data])

	@property
	def raw_magnetic(self):
		"""The raw magnetometer sensor values.
		A 3-tuple of X, Y, Z axis values that are 16-bit signed integers.
		"""
		self._read_bytes(OUT_X_H_M, 6, self._BUFFER)
		raw_values = struct.unpack_from('>hhh', self._BUFFER[0:6])
		return (raw_values[0], raw_values[1], raw_values[2])


	@property
	def magnetic(self):
		"""The processed magnetometer sensor values.
		A 3-tuple of X, Y, Z axis values in microteslas that are signed floats.
		"""
		mag_x, mag_y, mag_z = self.raw_magnetic
		return (mag_x / self._lsm303mag_gauss_lsb_xy * _GAUSS_TO_MICROTESLA,
				mag_y / self._lsm303mag_gauss_lsb_xy * _GAUSS_TO_MICROTESLA,
				mag_z / self._lsm303mag_gauss_lsb_z * _GAUSS_TO_MICROTESLA)


	@property
	def mag_rate(self):
		"""The magnetometer update rate."""
		return self._mag_rate

	@mag_rate.setter
	def mag_rate(self, value):
		assert value in (MAGRATE_3_1, MAGRATE_6_2, MAGRATE_12_5, MAGRATE_25, MAGRATE_50, MAGRATE_100)

		self._mag_rate = value
		reg_m = (((value & 0x07) << 2)| 0x60) & 0xFF
		print("REG_M: %s" %reg_m)
		self._write_u8( CTRL5, reg_m)
		print("CTRL5")


	@property
	def mag_gain(self):
		"""The magnetometer's gain."""
		print("mag_gain")
		return self._mag_gain


	@mag_gain.setter
	def mag_gain(self, value):
		assert value in (MAGGAIN_2, MAGGAIN_4, MAGGAIN_8, MAGGAIN_12)

		self._mag_gain = value
		reg_g = ((value & 0x01)<<5) & 0xFF      #(0x20) dans le registre
		self._write_u8( CTRL6, reg_g)
		print("CTRL6")

		"""if self._mag_gain == MAGGAIN_2:
			self._lsm303mag_gauss_lsb_xy = 1100.0
			self._lsm303mag_gauss_lsb_z = 980.0
		elif self._mag_gain == MAGGAIN_1_9:
			self._lsm303mag_gauss_lsb_xy = 855.0
			self._lsm303mag_gauss_lsb_z = 760.0
		elif self._mag_gain == MAGGAIN_2_5:
			self._lsm303mag_gauss_lsb_xy = 670.0
			self._lsm303mag_gauss_lsb_z = 600.0
		elif self._mag_gain == MAGGAIN_4_0:
			self._lsm303mag_gauss_lsb_xy = 450.0
			self._lsm303mag_gauss_lsb_z = 400.0
		elif self._mag_gain == MAGGAIN_4_7:
			self._lsm303mag_gauss_lsb_xy = 400.0
			self._lsm303mag_gauss_lsb_z = 355.0
		elif self._mag_gain == MAGGAIN_5_6:
			self._lsm303mag_gauss_lsb_xy = 330.0
			self._lsm303mag_gauss_lsb_z = 295.0
		elif self._mag_gain == MAGGAIN_8_1:
			self._lsm303mag_gauss_lsb_xy = 230.0
			self._lsm303mag_gauss_lsb_z = 205.0"""

	def _read_u8(self, register):
		#Lecture de 8bits (non signé) depuis l'adresse mentionnée.
		self._BUFFER[0] = (register & 0xFF)
		data = bytes([self._BUFFER[0]])
		self._device.writeto(self._address,data)           #self.address = CAPTEUR | data = REGISTRE qu'on veut lire

		#lecture 1 octet
		data = bytearray(1)
		self._device.readfrom_into(self._address,data)      #self.address = CAPTEUR | data = DONNEES qui se trouve dans le REGISTRE demandé
		return data[0]#retour du 1ier octet

	def _write_u8(self, register, val):
		#Ecrire de 8 bits (non-signé) à l'adresse indiqué
		buffer= bytearray(2)
		buffer[0]= register & 0xFF
		buffer[1] = val & 0xFF

		self._device.writeto(self._address, buffer)   #vers self.address = CAPTEUR on envoie buffer[1:0].
		                                            #composé du REGISTRE au quel on veut ecrire une VAL

	def _read_bytes(self,address, count, buf):
		#Lecture de 16-bits non signés
		data=bytes([address & 0xFF])
		#Ecriture de 1 octet
		self._device.writeto(self._address,data)
		#lecture de 2 octets
		self._device.readfrom_into(self._address, self._BUFFER)
		#composer un entier 16Bit
		return (self._BUFFER[1]<<8 | self._BUFFER[0])

	def read( self ):
		""" Returns accelerometer and Magnetometer data.
			returns ( (acc_x, acc_y, acc_z), (mag_x, mag_y, mag_z) )"""
		self.readAcc()
		self.readMag()

		return ((self._xa, self._ya, self._za),(self._xm,self._ym,self._zm))

	def readMag(self):
		x_lm = self._read_u8(0x08)
		x_hm = self._read_u8(0x09)
		y_lm = self._read_u8(0x0A)
		y_hm = self._read_u8(0x0B)
		z_lm = self._read_u8(0x0C)
		z_hm = self._read_u8(0x0D)

		ym=bytes([y_hm,y_lm])
		xm=bytes([x_hm,x_lm])
		zm=bytes([z_hm,z_lm])
		self._ym=struct.unpack(">h",ym)[0]
		self._xm=struct.unpack(">h",xm)[0]
		self._zm=struct.unpack(">h",zm)[0]

		return (self._xm, self._ym, self._zm)

	def readAcc(self):
		x_la = self._read_u8(0x28)
		x_ha = self._read_u8(0x29)
		y_la = self._read_u8(0x2A)
		y_ha = self._read_u8(0x2B)
		z_la = self._read_u8(0x2C)
		z_ha = self._read_u8(0x2D)

		ya=bytes([y_ha,y_la])
		xa=bytes([x_ha,x_la])
		za=bytes([z_ha,z_la])
		self._ya=struct.unpack(">h",ya)[0]
		self._xa=struct.unpack(">h",xa)[0]
		self._za=struct.unpack(">h",za)[0]
		# self.val_accel = [self._xa, self._ya, self._za]
		return (self._xa, self._ya, self._za)

	def heading(self, from_vector=None ):
		""" Give the heading (a float in degrees) from a given from_vector otherwise the default (1,0,0) vector."""
		_from = Vector(1,0,0)
		if from_vector:
			_from.set( from_vector.x, from_vector.y, from_vector.z )
		temp_m = Vector( self._xm, self._ym, self._zm ) # extract the last magnetic reading
		temp_m.x -= (self.m_min.x + self.m_max.x)/2
		temp_m.y -= (self.m_min.y + self.m_max.y)/2
		temp_m.z -= (self.m_min.z + self.m_max.z)/2

		val_accel = Vector( self._xa, self._ya, self._za ) # extract the last accelerometer reading
		E = Vector()
		temp_m.cross( val_accel, E ) # E = temp_m x E
		E.normalize()
		N = Vector()
		val_accel.cross( E, N ) # N = val_accel x E
		N.normalize()

		val_heading=atan2( E.dot(_from) ,N.dot(_from) ) *180 / pi
		if (val_heading < 0):
		    val_heading += 360
		return (val_heading)

	"""
	def vector_normalize(self,a):
		mag=math.sqrt(self.vector_dot(self.val_accel,self.val_accel))
		self.val_accel[0] /= mag
		self.val_accel[1] /= mag
		self.val_accel[2] /= mag


	def vector_cross(self,a,b):
		x=(a[1]*b[2])-(a[2]*b[1])
		y=(a[2]*b[0])-(a[0]*b[2])
		z=(a[0]*b[1])-(a[1]*b[0])
		return(x,y,z)

	def vector_dot(self,a,b):
		return((a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2]))"""
