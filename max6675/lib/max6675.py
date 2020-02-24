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
MAX6675 - Thermocouple type-K amplifier
=======================================
This library supports the use of the MAX6675 in MicroPython.
Author(s):
* Meurisse D for MC Hobby sprl (portage from Arduino to MicroPython)
* Adafruit Industries for Arduino version
"""
from machine import Pin
from time import sleep_ms

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"

class MAX6675:
	""" MAX6675 thermocouple amplifier driver """
	def __init__( self, data_pin, clk_pin, cs_pin ):
		""" Constructor accepting Pin instance or PinName

		:param data_pin: the input data pin on the microcontroleur (MISO on the MAX6675).
		:param clk_pin: the clock pin
		:param cs_pin: the chip select pin
		"""
		if data_pin is Pin:
			self.data_pin = data_pin
		else:
			self.data_pin = Pin( data_pin, Pin.IN )

		if clk_pin is Pin:
			self.clk_pin = clk_pin
		else:
			self.clk_pin = Pin( clk_pin, Pin.OUT )

		if cs_pin is Pin:
			self.cs_pin = cs_pin
		else:
			self.cs_pin = Pin( cs_pin, Pin.OUT )
			self.cs_pin.value( 1 ) # deactivate the max6675

	def read_celsius( self ):
		v = 0
		# activate the MAX6675
		self.cs_pin.value( 0 )
		sleep_ms( 1 )
		v = self.spi_read()
		v = v << 8
		v = v | self.spi_read()
		# deactivate the MAX6675
		self.cs_pin.value( 1 )

		if v & 0x4:
			# uh oh, no thermocouple attached!
			raise Exception( "No thermocouple attached" )

		# v >>= 3;
		v = v >> 3
		return v*0.25

	def spi_read( self ):
		""" read a byte from SPI bus """
		d = 0

		for i in range( 7, -1, -1 ):
			self.clk_pin.value( 0 )
			sleep_ms( 1 )

			if self.data_pin.value():
				# set the bit to 0 no matter what
				d = d | (1 << i)

			self.clk_pin.value( 1 )
			sleep_ms( 1 )

		return d

	@property
	def temperature( self ):
		""" Returns the temperature in celcius degree """
		return self.read_celsius()
