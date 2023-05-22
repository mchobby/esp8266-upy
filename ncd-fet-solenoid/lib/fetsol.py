"""
FET Solenoid (I2C) board driver (for National Control Device board).

Will work with
* MCP23008 4-Channel 8W 12V FET + 4 GPIO Solenoid Driver Valve Controller with I2C Interface.
* MCP23008 8-Channel 8W 12V FET Solenoid Driver Valve Controller with I2C Interface.

NCD-4Channel-FET-Solenoid-4Gpio : https://store.ncd.io/product/mcp23008-4-channel-8w-12v-fet-solenoid-driver-valve-controller-4-channel-gpio-with-i2c-interface/
NCD-8Channel-FET-Solenoid       : https://store.ncd.io/product/mcp23008-8-channel-8w-12v-fet-solenoid-driver-valve-controller-with-i2c-interface/
See also NCD Product at : http://shop.mchobby.be/

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from machine import Pin
from mcp230xx import MCP23008

class FetSolenoid4( MCP23008 ):
	"""
	Class to control the NCD 4-Channel FET Solenoid + 4 GPIO.

	FETs  are on GPIO 0-3 (Output ONLY)
	GPIOs are on GPIO 4-7 (Output, Input with/without PullUp)
	"""

	def __init__( self, i2c, address=0x20 ):
		super().__init__( i2c, address )
		self.init()

	def init( self ):
		# 4 first GPIO are OUTPUT ONLY
		for gpio in range( 4 ):
			super().setup( gpio, Pin.OUT )

	def _fetsol_validate_pin(self, pin):
		""" Can only change the pin setup from GPIO 4 """
		if pin < 4 or pin >= self.NUM_GPIO:
			raise ValueError('Invalid GPIO value, must be between 4 and {0}.'.format(self.NUM_GPIO))

	def setup(self, pin, mode ):
		""" Allow setup IN/OUT for gpio 4-7 """
		self._fetsol_validate_pin( pin )
		super().setup(pin, mode)

	def pullup(self, pin, enabled):
		""" Allow pullup for gpio 4-7 """
		self._fetsol_validate_pin( pin )
		super().pullup( pin, enabled )

	def reset(self):
		""" Reset all FETs """
		d = {}
		for i in range( 4 ):
			d[i] = False
		self.output_pins( d )

class FetSolenoid8( MCP23008 ):
	"""
	Class to control the NCD 8-Channel FET Solenoid

	FETs  are on GPIO 0-7 (Output ONLY)
	GPIOs none available
	"""

	def __init__( self, i2c, address=0x20 ):
		super().__init__( i2c, address )
		self.init()

	def init( self ):
		# 4 first GPIO are OUTPUT ONLY
		for gpio in range( self.NUM_GPIO ):
			super().setup( gpio, Pin.OUT )

	def _fetsol_validate_pin(self, pin):
		raise ValueError( 'No configurable GPIO available.' )

	def setup(self, pin, mode ):
		# Raising exception
		self._fetsol_validate_pin( -1 )

	def pullup(self, pin, enabled):
		# Raising exception
		self._fetsol_validate_pin( -1 )

	def reset(self):
		""" Reset all FETs """
		d = {}
		for i in range( self.NUM_GPIO ):
			d[i] = False
		self.output_pins( d )
