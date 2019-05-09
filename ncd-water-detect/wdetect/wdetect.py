"""
Driver for the Water Detect (I2C) sensor board from National Control Device.

Water Detect is an I2C sensor with 4.41 cm^2 sensitive area and a buzzer.

NCD-Water-Detection : http://shop.mchobby.be/
NCD-Water-Detection : https://store.ncd.io/product/water-detection-sensor-with-buzzer/
Datasheet : https://media.ncd.io/sites/2/20170721134419/PCA9536_WDBZ_I2CS.pdf

The MIT License (MIT)
Copyright (c) 2019 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
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

from pca9536 import PCA9536
from machine import Pin

class WaterDetect():
	"""
	Class to control the NCD Water Detect with Buzzer sensor.
	"""

	def __init__( self, i2c_bus ):
	 	# Initialized I2C bus, use the default I2C Address
		self._pca  = PCA9536( i2c_bus )
		self._pca.setup( 0, Pin.IN ) # Water detector pin
		self._pca.setup( 3, Pin.OUT ) # buzzer
		self._pca.output( 3, False )  # Deactivate buzzer

	#def init( self ):
	#	pass

	def buzzer( self, state ):
		""" Activate / Deactive the buzzer. State must be True/False """
		self._pca.output( 3, state )

	@property
	def has_water( self ):
		""" Check if the sensor detected some liquid """
		return not( self._pca.input(0) )

	#== Mimic PCA9536 but restrict pins =======================
	# Not all the PCA api have been assigned here
	def _validate_pin( self, pin ):
		""" Only IO1 and IO2 can be manipulated on Water Detect """
		if not( 1 <= pin <= 2 ):
			raise Exception( "Only IO 1 and 2 are available. %s cannot be used!" % pin )

	def setup( self, pin, mode ):
		self._validate_pin( pin )
		self._pca.setup( pin, mode )

	def input( self, pin ):
		self._validate_pin( pin )
		return self._pca.input( pin )

	def output( self, pin, state ):
		self._validate_pin( pin )
		self._pca.output( pin, state )

	def polarity( self, pin, inverted ):
		self._validate_pin( pin )
		self._pca.polarity( pin, inverted )
