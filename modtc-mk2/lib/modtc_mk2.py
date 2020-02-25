# MAX6675 MicroPython Driver - for MAX6675 Type-K thermocouple amplifier.
#
# Copyright (c) 2020 Meurisse Dominique for MC Hobby SPRL - Port to MicroPython
#
# Based on former work of ladyada on max6675  for Arduino
#    that was published as library under public domain. enjoy!
#    www.ladyada.net/learn/sensors/thermocouple
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

"""
MOD-TC-MK2-31885 - MAX31885 Thermocouple type-K amplifier over I2C via microcontroler
=====================================================================================
This library supports the use of the MOD-TC-MK2-31885 in MicroPython.
Author(s):
* Meurisse D for MC Hobby sprl (portage from Arduino to MicroPython)
* Olimex Ltd for Arduino version
"""
from machine import Pin
from time import sleep_ms

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"

REG_SET_ADDRESS = 0xF0
REG_GET_ID		= 0x20
REG_SET_TRIS	= 0x01
REG_SET_LAT		= 0x02
REG_GET_PORT	= 0x03
REG_SET_PU		= 0x04

REG_GET_TEMP	= 0x21

# IN		1
# OUT		0
# ON		1
# OFF		0
# LO		0
# HI		1

# Registers for Analog input (AN0, AN1, AN2, AN7, AN6) corresponding to GPIOs (0,1,2,5,6)
# index is the GPIO#
ANALOG_REGS  = [ 0x10, 0x11, 0x12, None, None, 0x16, 0x17 ]

# values for GPIO_0 to GPIO_6
GPIOS    = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40 ]
# Values for Pull_Up for GPIO_0 to GPIO_4
#    GPIO_3 has an hardware pull-up on the board
#    Does not what to do with 0x10 present in the original C file
PULLUPS  = [ 0x01, 0x02, 0x04, None, 0x08, None, None ]

class MODTC_MK2():
	""" Driver for the MOD-TC-MK2-31855 from Olimex Ltd """

	def __init__( self, i2c, address=0x23 ):
		self.address = address
		self.i2c     = i2c
		self.tris_status = 0 # TriState input status (uint8_t)
		self.lat_status  = 0 # Latch Status (uint8_t)
		self.pu_status   = 0 # pullup status (uint8_t)

	def _getID( self ):
		""" return the device ID """
		data = self.i2c.readfrom_mem( self.address, REG_GET_ID, 1 ) # Read 1 byte
		return data[0]

	def _temperature_read( self ):
		""" Read the temperature on the MK2 and return the raw data as unint32_t (so 32 bits) """
		data = self.i2c.readfrom_mem( self.address, REG_GET_TEMP, 4 ) # Read 4 bytes
		# data[3] = Wire.read(); # Notice that data are inverted First vyte read stored @ position 3
		# data[2] = Wire.read();
		# data[1] = Wire.read();
		# data[0] = Wire.read();
		# temp = ((uint32_t)data[3] << 24) | ((uint32_t)data[2] << 16) | ((uint32_t)data[1] << 8) | (uint32_t)data[0];
		return (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

	def pin_mode( self, gpio, mode ):
		""" Set a GPIO as Input or Output """
		pin_value = GPIOS[ gpio ]
		if mode == Pin.IN:
			self.tris_status |= pin_value
		else:
			self.tris_status &= (0xFF ^ pin_value)

		self.i2c.writeto_mem( self.address, REG_SET_TRIS, bytes([self.tris_status]))

	def pullup( self, gpio, enable ):
		""" Activate the internal pullup resistor on a GPIO """
		pu_value = PULLUPS[gpio]
		if not(pu_value):
			raise Exception( "No pullup support for gpio %s" % gpio )

		if enable:
			self.pu_status |= pu_value
		else:
			self.pu_status &= (0xFF ^ pu_value)

		self.i2c.writeto_mem( self.address, REG_SET_PU, bytes([self.pu_status]))

	def digital_read( self, gpio ):
		""" read the status of a GPIO """
		pin_value = GPIOS[ gpio ]

		data = self.i2c.readfrom_mem( self.address, REG_GET_PORT, 1 ) # Read 1 byte
		return True if data[0] & pin_value else False

	def digital_write( self, gpio, state ):
		""" Change the OUTPUT state of a GPIO.

		:param state: the new state that must evaluate to True or False"""
		if gpio == 3:
			raise Exception( "GPIO 3 not allowed in output mode.")
		pin_value = GPIOS[ gpio ]

		if state:
			self.lat_status |= pin_value
		else:
			self.lat_status &= (0xFF ^ pin_value)

		self.i2c.writeto_mem( self.address, REG_SET_LAT, bytes([self.lat_status]))

	def analog_read( self, gpio ):
		""" read 10 bits value (0..1023) on analog input at GPIO# """

		reg = ANALOG_REGS[gpio]
		if not(reg):
			raise Exception( "No analog support for GPIO %s" % gpio)

		data = self.i2c.readfrom_mem( self.address, reg, 2 ) # Read 2 bytes
		return (data[1]<<8) | data[0]

	@property
	def device_id( self ):
		return self._getID()

	@property
	def temperatures( self ):
		""" Returns the (internal_temp, external_temp) tuple.

		Remarks: may raise exception in case of fault reading"""

		c = self._temperature_read()
		# check for fault
		if c & 0x00010000:
			if c & 0x00000001:
				raise Exception( "Open Circuit" )
			elif c & 0x00000002:
				raise Exception( "Short to GND" )
			elif c & 0x00000004:
				raise Exception( "Short to VCC" )
			else:
				raise Exception( "Undefined fault!")
		# We can decode the calue
		in_f = 0.0
		ex_f = 0.0
		# Sign Internal temperature @ D15 (16 bits)
		in_s = True if c & 0x00008000 else False
		ex_s = True if c & 0x80000000 else False # (External Temp sign)
		# Convert external temperature
		ext = (c >> 16 )
		ext &= 0x7FFF
		ext >>= 2
		ex_f = (ext >> 2) + ((ext & 0x03) * 0.25)
		if ex_s :
			ex_f = -2048 + ex_f

		# Convert internal temperature
		_in = c & 0x0000FFFF
		_in >>= 4
		in_f = (_in >> 4) + (_in & 0x0F) * 0.0625
		if in_s :
			in_f = -128 + in_f

		return (in_f, ex_f) # (Internal_temp, external_temp)
