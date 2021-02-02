
# Implementation of the TCA9554A 8 bits GPIO expansion (100 KOhms pull-up in input)
#
# Copyright (c) 2021 MC Hobby SPRL
# Author: DMeurisse
#
# See project source at: https://github.com/mchobby/esp8266-upy/tree/master/tca9554a
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
from machine import Pin, I2C

REG_ADDR_INPUT = 0x00
REG_ADDR_OUTPUT = 0x01
REG_ADDR_POLARITY = 0x02
REG_ADDR_CONFIG = 0x03

class TCA9554A():
	""" TCA9554A 8 bits GPIO extender. """

	def __init__(self, i2c, address=0x38 ):
		self.address = address
		self.i2c = i2c
		# Buffer register values so they can be changed without reading.
		self.iodir = bytearray(1)  # Default direction to all inputs.
		self.iodir[0] = 0x00
		self.gpio  = bytearray(1)
		# Write current direction
		self.write_iodir()

	def _validate_pin(self, pin):
		"""Promoted to mcp implementation from prior Adafruit GPIO superclass"""
		# Raise an exception if pin is outside the range of allowed values.
		if pin < 0 or pin >= 8:
			raise ValueError('Invalid GPIO value, must be between 0 and 7.')

	def writeList(self, register, data):
		"""Introduced to match the writeList implementation of the Adafruit I2C _device member"""
		return self.i2c.writeto_mem(self.address, register, data)

	def readList(self, register, length):
		"""Introduced to match the readList implementation of the Adafruit I2C _device member"""
		return self.i2c.readfrom_mem(self.address, register, length)

	def setup(self, pin, mode):
		"""Set the pin to input or output mode. Mode = Pin.IN or Pin.OUT either OUT or IN. """
		self._validate_pin(pin)
		# Set bit to 1 for input or 0 for output.
		if mode == Pin.IN:
			self.iodir[0] |= 1 << (int(pin))
		elif mode == Pin.OUT:
		    self.iodir[0] &= ~(1 << (int(pin)))
		else:
			raise ValueError('Invalid mode')
		self.write_iodir()


	def output(self, pin, value):
		"""Set the pin to high/low. Value is boolean"""
		self.output_pins({pin: value})

	def toggle_pins( self, lst ):
		""" Swap the state of a list of output pins """
		# prepare a dict to store new pin states
		new_states = {}
		for pin in lst:
			# Invert gpio state
			new_states[pin] = not( self.gpio[0] & ( 1 << (pin) ) )
		# Apply new state
		self.output_pins( new_states )

	def output_pins(self, pins):
		"""Set multiple pins high or low at once.  Pins = dict of pin:state """
		[self._validate_pin(pin) for pin in pins.keys()]
		# Set each changed pin's bit.
		for pin, value in iter(pins.items()):
			if value:
				self.gpio[0] |= 1 << pin
			else:
				self.gpio[0] &= ~(1 << pin)
		# Write GPIO state.
		self.write_gpio()


	def input(self, pin, read=True):
		"""Read the specified pin state. Read = force GPIO read."""
		return self.input_pins([pin], read)[0]

	def input_pins(self, pins, read=True):
		"""Read multiple pins and return list of state. Pins = list of pins. Read Force GPIO read"""
		[self._validate_pin(pin) for pin in pins]
		if read:
			# Get GPIO state.
			self.read_gpio()
		# Return True if pin's bit is set.
		return [(self.gpio[0] & 1 << pin) > 0 for pin in pins]


	def pullup(self, pin, enabled):
		""" Activate/deactivate pull-up resistor on pin """
		# Max portability with MCP23017
		self._validate_pin(pin)
		if enabled==False:
			raise Exception('Input pins always have pullup on TCA9554A')

	def read_gpio(self):
		# As gpio may be altered for output operation, it MUST be a bytearray type!
		self.gpio = bytearray( self.readList(REG_ADDR_OUTPUT, 1) )

	def write_gpio(self, gpio=None):
		"""Write the specified byte value (or current buffer) to the GPIO registor"""
		if gpio is not None:
			self.gpio = gpio
		self.writeList(REG_ADDR_OUTPUT, self.gpio)

	def write_iodir(self, iodir=None):
		"""Write the specified byte value (or current buffer) to the IODIR registor"""
		if iodir is not None:
			self.iodir = iodir
		self.writeList(REG_ADDR_CONFIG, self.iodir)
