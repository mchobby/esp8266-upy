# Implementation of the library for the HT0740 Breakout
#
# Copyright (c) 2021 MC Hobby SPRL
# Author: DMeurisse
#
# See project source at: https://github.com/mchobby/esp8266-upy/tree/master/ht0740-switch
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

class HT0740():
	""" HT0740 I2C controlable power mosfet (PIM455) """

	def __init__(self, i2c, address=0x38 ):
		self.address = address
		self.i2c = i2c
		# Mosfet Driver is controled in reverse logic
		self.i2c.writeto_mem( self.address, REG_ADDR_OUTPUT, bytes([0x01]) ) # P0 @ High = OFF
		# Set the pin P0 as output
		self.i2c.writeto_mem( self.address, REG_ADDR_CONFIG, bytes([0x7e]) ) # P0 as Output

	def output( self, value ):
		""" Activate or not the Output """
		self.i2c.writeto_mem( self.address, REG_ADDR_OUTPUT, bytes( [0x00 if value else 0x01] ) ) # P0 @ High = OFF

	def on( self ):
		self.output(True)

	def off( self ):
		self.output(False)
