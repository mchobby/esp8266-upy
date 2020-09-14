# MCP23Sxx MicroPython Driver - for MCP23Sxx SPI GPIO Expander.
#
# Based on former work of Florian Mueller for Raspberry-Pi
#    Copyright 2016-2019 Florian Mueller (contact@petrockblock.com)
#    https://github.com/petrockblog/RPi-MCP23S17/tree/master/RPiMCP23S17
#
# Aug 13, 2019 : make it compatible with MicroPython against the machine.SPI interface
# Aug 13, 2019 : make it compatible with MicroPython against the machine.SPI interface
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

__version__ = '0.0.1'

from time import sleep_ms
from machine import Pin

"""Register addresses as documented in the technical data sheet at
http://ww1.microchip.com/downloads/en/DeviceDoc/21952b.pdf
"""
MCP23S17_IODIRA = 0x00
MCP23S17_IODIRB = 0x01
MCP23S17_IPOLA = 0x2
MCP23S17_IPOLB = 0x3
MCP23S17_GPIOA = 0x12
MCP23S17_GPIOB = 0x13
MCP23S17_OLATA = 0x14
MCP23S17_OLATB = 0x15
MCP23S17_IOCON = 0x0A
MCP23S17_GPPUA = 0x0C
MCP23S17_GPPUB = 0x0D

"""Bit field flags as documentined in the technical data sheet at
http://ww1.microchip.com/downloads/en/DeviceDoc/21952b.pdf
"""
IOCON_UNUSED = 0x01
IOCON_INTPOL = 0x02
IOCON_ODR = 0x04
IOCON_HAEN = 0x08
IOCON_DISSLW = 0x10
IOCON_SEQOP = 0x20
IOCON_MIRROR = 0x40
IOCON_BANK_MODE = 0x80

IOCON_INIT = 0x28  # IOCON_SEQOP and IOCON_HAEN from above

MCP23S17_CMD_WRITE = 0x40
MCP23S17_CMD_READ = 0x41

class MCP23S17(object):
	""" This class provides an abstraction of the GPIO expander MCP23S17 """

	def __init__(self, spi, pin_cs, device_id=0x00):
		""" spi : initialized SPI bus (mode 0).
		pin_cs : The Chip Select pin of the MCP.
		device_id : The device ID of the component, i.e., the hardware address (default 0)
		"""
		self.device_id = device_id
		self._GPIOA = 0
		self._GPIOB = 0
		self._IODIRA = 0
		self._IODIRB = 0
		self._GPPUA = 0
		self._GPPUB = 0
		self._pin_reset = -1 # removed from parameters
		#self._bus = bus
		self._pin_cs = pin_cs
		#self._spimode = 0b00
		self._spi = spi
		self.begin()

	def begin(self):
		#Initializes the MCP23S17 with hardware-address access and sequential operations mode.
		self._writeRegister( MCP23S17_IOCON, IOCON_INIT)

		# set defaults
		for index in range(0, 16): # 0 to 15
			self.setup(index, Pin.IN)
			self.pullup(index, True)

	def setup(self, pin, mode):
		""" Sets the direction for a given pin. """
		# Parameters:
		#  pin -- The pin index (0 - 15)
		#  mode -- The direction of the pin (Pin.In, Pin.OUT)

		self._validate_pin(pin)
		assert ((mode == Pin.IN) or (mode == Pin.OUT))

		if (pin < 8):
			register = MCP23S17_IODIRA
			data = self._IODIRA
			noshifts = pin
		else:
			register = MCP23S17_IODIRB
			noshifts = pin & 0x07
			data = self._IODIRB

		if (mode == Pin.IN):
			data |= (1 << noshifts)
		else:
			data &= (~(1 << noshifts))

		self._writeRegister(register, data)

		if (pin < 8):
			self._IODIRA = data
		else:
			self._IODIRB = data

	def input(self, pin):
		""" Reads the logical level of a given pin. """
		# pin -- The pin index (0 - 15)
		self._validate_pin(pin)

		if (pin < 8):
			self._GPIOA = self._readRegister(MCP23S17_GPIOA)
			if ((self._GPIOA & (1 << pin)) != 0):
				return True
			else:
				return False
		else:
			self._GPIOB = self._readRegister(MCP23S17_GPIOB)
			pin &= 0x07
			if ((self._GPIOB & (1 << pin)) != 0):
				return True
			else:
				return False

	def pullup(self, pin, enabled):
		""" Enables or disables the pull-up mode for input pins. """
		self._validate_pin( pin )

		if pin < 8:
			register = MCP23S17_GPPUA
			data = self._GPPUA
			noshifts = pin
		else:
			register = MCP23S17_GPPUB
			noshifts = pin & 0x07
			data = self._GPPUB

		if (enabled):
			data |= (1 << noshifts)
		else:
			data &= (~(1 << noshifts))

		self._writeRegister(register, data)

		if (pin < 8):
			self._GPPUA = data
		else:
			self._GPPUB = data

	def input_pins( self, pins, read=True ):
		""" Read multiple pins and return list of state. Pins = list of pins. Read Force GPIO read"""
		[self._validate_pin(pin) for pin in pins]
		if read:
			# Get GPIO state.
			self.read_gpio()
		# Return True if pin's bit is set.
		r = []
		for pin in pins:
			if (pin < 8):
				if ((self._GPIOA & (1 << pin)) != 0):
					r.append( True )
				else:
					r.append( False )
			else:
				pin &= 0x07
				if ((self._GPIOB & (1 << pin)) != 0):
					r.append( True )
				else:
					r.append( False )
		# Return the result
		return r

	def output(self, pin, level):
		""" Sets the level of a given pin. """
		# pin -- The pin idnex (0 - 15)
		# level -- The logical level to be set (False, True)
		self._validate_pin( pin )

		if (pin < 8):
			register = MCP23S17_GPIOA
			data = self._GPIOA
			noshifts = pin
		else:
			register = MCP23S17_GPIOB
			noshifts = pin & 0x07
			data = self._GPIOB

		if level :
			data |= (1 << noshifts)
		else:
			data &= (~(1 << noshifts))

		self._writeRegister(register, data)

		if (pin < 8):
			self._GPIOA = data
		else:
			self._GPIOB = data

	def output_pins(self, pins):
		"""S et multiple pins high or low at once.  Pins = dict of pin:state """
		[self._validate_pin(pin) for pin in pins.keys()]
		# Set each changed pin's bit.
		for pin, value in iter(pins.items()):
			if (pin < 8):
				register = MCP23S17_GPIOA
				data = self._GPIOA
				noshifts = pin
			else:
				register = MCP23S17_GPIOB
				noshifts = pin & 0x07
				data = self._GPIOB

			if value :
				data |= (1 << noshifts)
			else:
				data &= (~(1 << noshifts))

			if (pin < 8):
				self._GPIOA = data
			else:
				self._GPIOB = data

		# Write GPIO states.
		buff = (self._GPIOB << 8) | self._GPIOA
		self._writeRegisterWord(MCP23S17_GPIOA, buff )

	def write_gpio(self, data):
		""" Sets the data port value for all pins with a 16 bit values AND send it to the MCP23Sxx """
		self._GPIOA = (data & 0xFF)
		self._GPIOB = (data >> 8)
		self._writeRegisterWord(MCP23S17_GPIOA, data)

	def read_gpio(self):
		""" Reads the data port value of all pins. Store the values internally then returns a 16 bits data """
		data = self._readRegisterWord(MCP23S17_GPIOA)
		self._GPIOA = (data & 0xFF)
		self._GPIOB = (data >> 8)
		return data

	def _writeRegister(self, register, value):
		command = MCP23S17_CMD_WRITE | ((self.device_id) << 1)
		self._pin_cs.value( 0 )
		sleep_ms( 1 )
		self._spi.write( bytes([command, register, value]) )
		self._pin_cs.value( 1 )
		sleep_ms( 1 )

	def _readRegister(self, register):
		command = MCP23S17_CMD_READ | ((self.device_id) << 1)
		self._pin_cs.value( 0 )
		sleep_ms( 1 )
		#self._setSpiMode(self._spimode)
		self._spi.write( bytes([command, register]) )
		#data = self._spi.xfer2([command, register, 0])
		data = self._spi.read( 1 )
		self._pin_cs.value( 1 )
		sleep_ms( 1 )
		return data[0]# data[2]

	def _readRegisterWord(self, register):
		buffer = [0, 0]
		buffer[0] = self._readRegister(register)
		buffer[1] = self._readRegister(register + 1)
		return ((buffer[1] << 8) | buffer[0])

	def _writeRegisterWord(self, register, data):
		self._writeRegister(register, data & 0xFF)
		self._writeRegister(register + 1, data >> 8)

	def _validate_pin(self, pin):
		# Raise an exception if pin is outside the range of allowed values.
		if pin < 0 or pin >= 16:
			raise ValueError('Invalid GPIO value, must be between 0 and 15.')
