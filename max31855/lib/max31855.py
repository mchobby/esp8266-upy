# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D for MCHobby.be
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
#
# Note:
# 22 jul 2021: Code created from this MicroPython Forum (thanks guys)
# 				https://forum.micropython.org/viewtopic.php?t=3003
#
import time

class MAX31855:
	""" Read the data from MAX31855 thermocouple amplifier """

	def __init__( self, spi, cs_pin ):
		""" constructor.

		:param spi: must be initialized (in SPI in mode0 -> polarity=0, phase=0) and baudrate=5000000
		:param cs_pin: output pin for SPI transaction. Must be initialized HIGH.
		:param mclk freq: freq of the source clock (eg: 25000000 for 25 Mhz). """
		self.spi = spi
		self.cs_pin = cs_pin # is the CSn from MAX31855
		self.buf4 = bytearray(4)

	def temperature( self ):
		""" Read the temperature. May return None in cas of error """
		try:
			retry = 0
			while True:
				retry += 1

				self.cs_pin.value(0)
				try:
					self.spi.readinto( self.buf4 )
				except:
					pass
				self.cs_pin.value(1)

				val = self.buf4[0] << 8 | self.buf4[1]
				if val & 0x0001: # this is a NaN
					if retry > 0:
						raise Exception( 'Multiple read returned NaN' )
					# Retry another time
					val.sleep_ms( 2 )
					continue # Lets make a new tries

				val >>= 2
				if val & 0x2000:
					val -= 16384
				return val * 0.25

		except:
			return None
