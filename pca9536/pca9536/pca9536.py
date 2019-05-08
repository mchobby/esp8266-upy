"""
PCA9536 4 Bit GPIO extender (I2C) Driver.

The API follows the MCPxx GPIO extender (so Adafruit's Industries API)

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
#import ustruct
#import time


# Registers
REG_INPUT    = 0  # default
REG_OUTPUT   = 1
REG_POLARITY = 2
REG_CONFIG   = 3

# Pin Name should not be necessary
# IO0 = 0
# IO1 = 1
# IO2 = 2
# IO3 = 3

# IO Pin Mode
IO_MODE_OUTPUT = 0
IO_MODE_INPUT  = 1

# IO State
# IO_LOW  = 0
# IO_HIGH = 1

# Polarity feature
IO_POLARITY_NON_INVERTED = 0
IO_POLARITY_INVERTED     = 1

# ALL_INPUT        = 0xFF
# ALL_OUTPUT       = 0x00
# ALL_LOW          = 0x00
# ALL_HIGH         = 0xFF
# ALL_NON_INVERTED = 0x00
# ALL_INVERTED     = 0xFF
# COM_SUCCESS      = 0x00

class PCA9536():
	"""
	Class to control the PCA9536 GPIO Extender.

	All methods mimic the MCP implementation, so based on the Adafruit Industries MCP implementation.
	"""

	def __init__( self, i2c_bus, addr=0x41 ):
		self.i2c   = i2c_bus # Initialized I2C bus
		self.addr = addr # MPL115A2 board address
		#self.init()

	#def init( self ):
	#	pass

	def _validate_pin(self, pin):
		# Raise an exception if pin is outside the range of allowed values.
		if pin < 0 or pin > 3:
			raise ValueError('Invalid GPIO value, must be between 0 and {0}.'.format(4))

	def setup(self, pin, mode):
		"""Set the pin to input or output mode. Mode = Pin.IN or Pin.OUT either OUT or IN. """
		self._validate_pin(pin)
		# Read the current config
		iodir = self.i2c.readfrom_mem( self.addr, REG_CONFIG, 1 )[0]
		# Set bit to 1 for input or 0 for output.
		if mode == Pin.IN:
			iodir |= 1 << pin # Set the bit
		elif mode == Pin.OUT:
			iodir &= ~(1 << pin) # Reset the bit
		else:
			raise ValueError('Invalid mode')
		# Write the config.
		self.i2c.writeto_mem( self.addr, REG_CONFIG, bytes([iodir]) )

	def output(self, pin, value):
		"""Set the pin to high/low. Value is boolean"""
		self.output_pins({pin: value})

	def output_pins(self, pins):
		"""Set multiple pins high or low at once.  Pins = dict of pin: state """
		[self._validate_pin(pin) for pin in pins.keys()]
		# Read GPIO states
		gpio = self.i2c.readfrom_mem( self.addr, REG_OUTPUT, 1 )[0]
		# Set each changed pin's bit.
		for pin, value in iter(pins.items()):
			if value:
				gpio |= (1 << pin) # Set the bit
			else:
				gpio &= ~(1 << pin) # Clear the bit
		# Write GPIO state.
		self.i2c.writeto_mem( self.addr, REG_OUTPUT, bytes([gpio]) )

	def input( self, pin ):
		""" read the value of a given pin """
		return self.input_pins([pin])[0]

	def input_pins( self, pins ):
		""" returns the state of multiple pins as list of boolean values.
			Pins is a list of pins. """
		[self._validate_pin(pin) for pin in pins]
		# Read the input buffer
		data = self.i2c.readfrom_mem( self.addr, REG_INPUT, 1 )[0]

		return [ True if data & (1<<pin) else False for pin in pins ]

	def pullup( self, pin, enabled ):
		""" Activate / Deactivate the pull-up on a given pin """
		raise Exception( 'Internal pull-up cannot be disabled!' )

	# === Extra API for pca9536 ================================================
	def reset( self ):
		""" Reset the PCA configuration """
		# Set all pins as Input (High impedance)
		for pin in range( 4 ):
			self.setup( pin, Pin.IN )
		# Set pin level to High
		self.output_pins( {0:True, 1:True, 2: True, 3: True} )
		# Reset Polarity
		self.polarity_pins( [(0,False),(1,False),(2,False),(3,False)] )

	def polarity( self, pin, inverted ):
		""" Allow to invert the polarity of a input pin when reading the data """
		# Status: Experimental
		self.polarity_pins( [(pin,inverted)] )

	def polarity_pins( self, lst ):
		""" Allow to invert the polarity of severam input pins (when reading the data).
		list must be a list of tuple (pin, inverted) """
		# Status: Experimental
		[self._validate_pin(pin) for pin, inverted in lst]
		# Read Polarity states
		data = self.i2c.readfrom_mem( self.addr, REG_POLARITY, 1 )[0]
		# Set each changed pin's bit.
		for pin, inverted in lst:
			if not(inverted):
				data &= ~(1 << pin) # Clear the bit
			else:
				data |= (1 << pin) # Set the bit
		# Write Polarity state.
		self.i2c.writeto_mem( self.addr, REG_POLARITY, bytes([data]) )
