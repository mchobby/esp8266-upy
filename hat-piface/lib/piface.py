# PiFace MicroPython Driver
#
# Author Meurisse D. for MCHobby.be
#
# Aug 15, 2019 : Domeur : initial version
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

from machine import Pin
from mcp23Sxx import MCP23S17

class PiFace( MCP23S17 ):
	def __init__( self, spi, cs_pin, device_id=0x00 ):
		super().__init__( spi, cs_pin, device_id )
		# Input as PullUp ( GPB0..GPB7 )
		for pin in range(8, 16):
			self.setup(pin, Pin.IN)
			self.pullup(pin, True )
		# Output Pins (GPA0..GPA7)
		for x in range(0, 8):
			self.setup(x, Pin.OUT)

		# Assign facades
		self.outputs = OutputFacade( owner = self )
		self.inputs  = InputFacade( owner = self )

	def set_output( self, nr, state ):
		""" Change the state of an output """
		assert 0 <= nr <= 7, "Outputs must be in 0..7"
		super().output( nr, state )

	def get_input( self, nr ):
		""" return the state of an input """
		assert 0 <= nr <= 7, "Inputs must be in 0..7"
		return not( super().input( nr+8 ) ) # Pullup = reverse logic

	def reset( self ):
		# reset the board
		self.output_pins( {0:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False} )

class OutputFacade:
	""" Access to output by their number """
	def __init__( self, owner ):
		self._owner = owner

	def __getitem__( self, relay_nr ):
		""" Last know state of output """
		raise Exception( 'Cannot read back output status' )

	def __setitem__( self, relay_nr, value ):
		""" Set the state of the relay """
		return self._owner.set_output( relay_nr, value ) # change the relay

class InputFacade:
	""" Access to inputs by their number """
	def __init__( self, owner ):
		self._owner = owner

	def __getitem__( self, input_nr ):
		""" Last know state of output """
		return self._owner.get_input( input_nr )

	def __setitem__( self, input_nr, value ):
		""" Set the state of the relay """
		raise Exception( 'Cannot set value for input' )

	@property
	def all( self ):
		""" Return the status of all inputs as a list """
		return [ not(value) for value in self._owner.input_pins( [8,9,10,11,12,13,14,15] ) ]
