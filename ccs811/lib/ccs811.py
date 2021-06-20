# The MIT License (MIT)
#
# Copyright (c) 2020 Meurisse Dominique for MC Hobby SPRL - Backport to MicroPython
#
# Based on the Adafruit Arduino code from https://github.com/adafruit/Adafruit_CCS811
# Copyright (c) 2017 Adafruit Industries
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
CCS811 Air Quality Sensor Breakout - VOC and eCO2
======================================================================
This library supports the use of the CCS811 air quality sensor in MicroPython.

Author(s):
* Meurisse D for MC Hobby sprl (portage fro Arduino to MicroPython)
* Adafruit Industries for Arduino version

**Notes:**

#. `Datasheet
<https://cdn-learn.adafruit.com/assets/assets/000/044/636/original/CCS811_DS000459_2-00-1098798.pdf?1501602769>`_
"""
import time
import struct
from micropython import const

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"


CCS811_STATUS = const(0x00)
CCS811_MEAS_MODE = const(0x01)
CCS811_ALG_RESULT_DATA = const(0x02)
CCS811_RAW_DATA = const(0x03)
CCS811_ENV_DATA = const(0x05)
CCS811_NTC = const(0x06)
CCS811_THRESHOLDS = const(0x10)
CCS811_BASELINE = const(0x11)
CCS811_HW_ID = const(0x20)
CCS811_HW_VERSION = const(0x21)
CCS811_FW_BOOT_VERSION = const(0x23)
CCS811_FW_APP_VERSION = const(0x24)
CCS811_ERROR_ID = const(0xE0)
CCS811_SW_RESET = const(0xFF)

# _BASELINE = 0x11
# _HW_ID = 0x20
# _HW_VERSION = 0x21
# _FW_BOOT_VERSION = 0x23
# _FW_APP_VERSION = 0x24
# _ERROR_ID = 0xE0

_SW_RESET = const(0xFF)

CCS811_BOOTLOADER_APP_ERASE = 0xF1
CCS811_BOOTLOADER_APP_DATA = 0xF2
CCS811_BOOTLOADER_APP_VERIFY = 0xF3
CCS811_BOOTLOADER_APP_START = 0xF4


CCS811_DRIVE_MODE_IDLE = const(0x00)
CCS811_DRIVE_MODE_1SEC = const(0x01)
CCS811_DRIVE_MODE_10SEC = const(0x02)
CCS811_DRIVE_MODE_60SEC = const(0x03)
CCS811_DRIVE_MODE_250MS = const(0x04)

_HW_ID_CODE = const(0x81)
_REF_RESISTOR = const(100000)

class Status:
	__slot__ = ['error', 'data_ready', 'app_valid', 'fw_mode' ]

	def __init__( self ):
		self.error = True
		self.data_ready = True
		self.app_valid = True
		self.fw_mode = True

	def set( self, data ):
		self.error = (data & 0x01)>0
		self.data_ready = ((data >> 3) & 0x01)>0
		self.app_valid = ((data >> 4) & 0x01)>0
		self.fw_mode = ((data >> 7) & 0x01)>0

class MeasMode:
	__slot__ = ['int_thresh', 'int_datardy', 'drive_mode']

	def __init__(self):
		self.int_thresh = 1
		self.int_datardy = 1
		self.drive_mode = 3

	def get( self ):
		return (self.int_thresh << 2) | (self.int_datardy << 3) | (self.drive_mode << 4)

class ErrorId:
	__slot__ = ['write_reg_invalid','read_reg_invalid','measmode_invalid','max_resistance','heater_fault','heater_supply']

	def init( self ):
		self.write_reg_invalid = True
		self.read_reg_invalid  = True
		self.measmode_invalid  = True
		self.max_resistance    = True
		self.heater_fault      = True
		self.heater_supply     = True

	def set( self, data ):
		self.write_reg_invalid = (data & 0x01)>0
		self.read_reg_invalid  = ((data & 0x02) >> 1)>0
		self.measmode_invalid  = ((data & 0x04) >> 2)>0
		self.max_resistance    = ((data & 0x08) >> 3)>0
		self.heater_fault      = ((data & 0x10) >> 4)>0
		self.heater_supply     = ((data & 0x20) >> 5)>0

	@property
	def as_text( self ):
		lst = []
		if self.write_reg_invalid :
			lst.append( 'write_reg_invalid' )
		if self.read_reg_invalid  :
			lst.append( 'read_reg_invalid' )
		if self.measmode_invalid  :
			lst.append( 'measmode_invalid' )
		if self.max_resistance    :
			lst.append( 'max_resistance' )
		if self.heater_fault      :
			lst.append( 'heater_fault' )
		if self.heater_supply     :
			lst.append( 'heater_supply' )
		return ','.join(lst)

class CCS811:
	""" CCS811 gas sensor driver. """

	def __init__(self, i2c_bus, address=0x5A):
		""" Constructor for CCS811

			:param i2c: The I2C bus.
			:param int addr: The I2C address of the CCS811.
		"""
		self.i2c_device = i2c_bus
		self.address = address

		self._TVOC = None
		self._eCO2 = None
		self.status = Status()
		self.meas_mode = MeasMode()
		self.error_id  = ErrorId()

		print( 'reset' )
		self.reset()
		time.sleep( 0.100 )
		#check that the HW id is correct
		if self._read8( CCS811_HW_ID ) != _HW_ID_CODE:
			raise RuntimeError("Device ID returned is not correct! Please check your wiring.")

		# try to start the app
		# this->write(CCS811_BOOTLOADER_APP_START, NULL, 0);
		self.i2c_device.writeto( self.address, bytes([CCS811_BOOTLOADER_APP_START])  )
		time.sleep( 0.100 )

		# make sure there are no errors and we have entered application mode
		if self.check_error:
			raise RuntimeError( "Cannot start CCS811 APP due to error %s" % self.error_id.as_text )

		# check_error did update the status on the CCS811
		# if(!_status.FW_MODE) return false;
		if not self.status.fw_mode:
			raise RuntimeError( "Firmware not in application mode!" )

		#disableInterrupt();
		self.set_interrupt( False )

		# default to read every second
		self.set_drive_mode( CCS811_DRIVE_MODE_1SEC )
		time.sleep( 0.100 ) # I added it

	def _read8( self, reg ):
		""" read the content of a register and return the value """
		data = self.i2c_device.readfrom_mem( self.address, reg, 1 )
		# debug: print( "_read8: reg %i -> %r" % (reg,data) )
		return data[0]

	def _write8( self, reg, value ):
		""" write a value into a register """
		# debug: print( "_write8: reg %i -> %r" % (reg,value) )
		self.i2c_device.writeto( self.address, bytes([reg, value]) )

	def _update_status( self ):
		self.status.set( self._read8(CCS811_STATUS) )

	@property
	def data_ready( self ):
		""" Checks if data is available to be read. """
		self._update_status()
		return self.status.data_ready

	@property
	def check_error( self ):
		""" Check the error flag in the status. In case of error, load the error
		    details in self.error_id object """
		#_status.set(read8(CCS811_STATUS));
		self._update_status()
		if self.status.error:
			# Update the error_id
			self.error_id.set( self._read8( CCS811_ERROR_ID ) )
		return self.status.error

	def _read_data(self):
		""" Read the data from sensor and store the result """
		if not self.data_ready:
			return False
		else:
			data = bytearray( 8 )
			# this->read(CCS811_ALG_RESULT_DATA, buf, 8);
			self.i2c_device.readfrom_mem_into( self.address, CCS811_ALG_RESULT_DATA ,data )

			# _eCO2 = ((uint16_t)buf[0] << 8) | ((uint16_t)buf[1]);
			# _TVOC = ((uint16_t)buf[2] << 8) | ((uint16_t)buf[3]);
			self._eCO2 = (data[0]<<8) | data[1]
			self._TVOC = (data[2]<<8) | data[3]
			if self.status.error :
				return data[5]
			else:
				return 0

	@property
	def tvoc(self): # pylint: disable=invalid-name
		"""Total Volatile Organic Compound in parts per billion."""
		self._read_data()
		return self._TVOC

	@property
	def eco2(self): # pylint: disable=invalid-name
		"""Equivalent Carbon Dioxide in parts per million. Clipped to 400 to 8192ppm."""
		self._read_data()
		return self._eCO2

	@property
	def temperature(self):
		RuntimeError("No more NTC on the CCS811 device.")

	def set_environmental_data(self, humidity, temperature):
		"""Set the temperature and humidity used when computing eCO2 and TVOC values.

		:param int humidity: The current relative humidity in percent.
		:param float temperature: The current temperature in Celsius.

		STATUS: Not tested yet!"""
		# Humidity is stored as an unsigned 16 bits in 1/512%RH. The default
		# value is 50% = 0x64, 0x00. As an example 48.5% humidity would be 0x61,
		# 0x00.
		humidity = int(humidity * 512)

		# Temperature is stored as an unsigned 16 bits integer in 1/512 degrees
		# there is an offset: 0 maps to -25C. The default value is 25C = 0x64,
		# 0x00. As an example 23.5% temperature would be 0x61, 0x00.
		temperature = int((temperature + 25) * 512)

		buf = bytearray(5)
		buf[0] = CCS811_ENV_DATA # the target register
		struct.pack_into(">HH", buf, 1, humidity, temperature)

		#with self.i2c_device as i2c:
		#    i2c.write(buf)
		self.i2c_device.writeto( self.address, buf )

	def reset(self):
		"""Initiate a software reset."""
		# reset sequence from the datasheet
		seq = bytearray([0x11, 0xE5, 0x72, 0x8A])
		self.i2c_device.writeto( self.address, bytes([CCS811_SW_RESET]), False  )
		self.i2c_device.writeto( self.address, seq )

	def set_drive_mode( self, mode ):
		""" sample rate of the sensor.
			:param mode: one of CCS811_DRIVE_MODE_IDLE, CCS811_DRIVE_MODE_1SEC, CCS811_DRIVE_MODE_10SEC, CCS811_DRIVE_MODE_60SEC, CCS811_DRIVE_MODE_250MS. """
		self.meas_mode.drive_mode = mode
		# write8(CCS811_MEAS_MODE, _meas_mode.get())
		self._write8( CCS811_MEAS_MODE, self.meas_mode.get() )

	def set_interrupt( self, enabled ):
		""" enable/disable the data ready interrupt pin on the device """
		self.meas_mode.int_datardy = 1 if enabled else 0
		#this->write8(CCS811_MEAS_MODE, _meas_mode.get());
		self._write8( CCS811_MEAS_MODE, self.meas_mode.get() )
