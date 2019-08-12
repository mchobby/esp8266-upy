# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse Dominique for MC Hobby SPRL
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
Controlling the Adafruit Joy Bonnet (ID:3464) from MicroPython.
Wiring based on NADHAT PYB405 as exposed on pyboard-driver GitHub

* Author(s): Meurisse Dominique (MicroPython).

* Adafruit Joy Bonnet : https://www.adafruit.com/product/3464
"""
from ads1x15 import ADS1015
from machine import Pin, Signal

# Default setup for the JOY-BONNET Pins.
# The NADHAT PYB405 have NRST wired to GPIO 15 --> CAN'T USE IT for Player2!
DEFAULT_PIN_SETUP = { \
	'SELECT' : 'X8', 'START': 'X11', \
	'PLAYER1' : 'Y3', 'PLAYER2':None, \
	'A': 'X1', 'Y': 'X2', 'X' : 'X12', 'B': 'Y13'  }

class JoyBonnet():
	def __init__(self, i2c, pin_setup = DEFAULT_PIN_SETUP ):
		"""Initialize Joy Bonnet specific Pins and ADC reader (for the joystick) """
		self.i2c = i2c
		self.adc = ADS1015(i2c = i2c, address = 72 )
		self.pin_setup = pin_setup
		self.last_state = {} # retain the last state of buttons
		self.x_center = self.adc.read( rate=0, channel1=1 ) # around 833
		self.y_center = self.adc.read( rate=0, channel1=0 ) # around 824
		self.x_thresold = 10 # minimum thresold around the center value
		self.y_thresold = 10 # minimum thresold around the center value
		# maximum & scale
		self.x_max      = 1652
		self.y_max      = 1652
		self.x_scale    = 100/(self.x_max/2) # scale to retreive value between -100 & +100
		self.y_scale    = 100/(self.y_max/2)

		for name, pinname in self.pin_setup.items():
			if not pinname: # skip unassigned button
				continue
			p = Pin( pinname, Pin.IN, Pin.PULL_UP )
			self.pin_setup[name]  = Signal( p, invert=True ) # replace PinName by Signal(Pin) Instance
			self.last_state[name] = False # Initialize last know button state

	def button( self, name ):
		""" Read the state of a named button (see pin_setup) """
		_s = self.pin_setup[name]
		return _s() if _s else False # Some buttons are not assigned

	@property
	def all_buttons( self ):
		""" read all the buttons state """
		for name,signal in self.pin_setup.items():
			if signal:
				self.last_state[name] = signal()
		return self.last_state

	@property
	def axis( self ):
		x_val = self.adc.read( rate=0, channel1=1 ) - self.x_center
		y_val = -1* (self.adc.read( rate=0, channel1=0 ) - self.y_center) # Invert axis (+ toward top)
		if abs(x_val) <= self.x_thresold:
			x_val = 0
		x_val = int( x_val * self.x_scale ) # scale to -100 <-> +100
		if abs(y_val) <= self.y_thresold:
			y_val = 0
		y_val = int( y_val * self.y_scale ) # scale to -100 <-> +100
		return (x_val, y_val)
