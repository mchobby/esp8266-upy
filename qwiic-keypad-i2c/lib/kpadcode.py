"""  kpadcode.py - I2C Qwiic Keypad Code Checker.

  Enhanced code for the Keypad_I2C class (kpadi2c.py) .

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

------------------------------------------------------------------------

History:
  10 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

__version__ = "0.0.1"

from kpadi2c import Keypad_I2C
import time


class CodeChecker( Keypad_I2C ):
	def __init__(self, i2c, address, code, timeout=30 ):
		# code : string with the code to key-in (or list of string)
		# timeout : in 100s of milliseconds
		super().__init__( i2c, address )
		self._debug = False

		# _key_code is a list of codes
		if type(code) is str:
			self._key_code = [ code ]
			self._user_entry = [' ']*len(code)
		elif type(code) is list:
			self._key_code = code # Already a list of codes
			_len = len(code[0])
			self._user_entry = [' ']*_len
			# All codes must have the same length
			for _code in self._key_code:
				if len(_code) != _len:
					raise Exception( 'Invalid length for code "%s". Must have %i chars ' % (_code,_len) )
		# other variables
		self._user_entry_index = 0
		self._user_is_active = False # used to know when a user is active and therefore we want to engage timeout stuff
		self._timeout = timeout # 30 * 100ms
		self._timeout_counter = 0 # Counter of timeout
		self._on_update = None # Update event function(user_entry_string, timeout_bool)

	def execute( self ):
		# Catch user code. Execute as long as user is active. Exit if user gets inactive (timeout)
		self.clear_entry()
		self._user_is_active = False
		self._timeout_counter = 0
		self.fire_on_update( False )

		while True:
			self.update_fifo()
			btn = self.button

			if btn > 100: # At startup a series 127's come accoss -- way out of range -- just noise
				pass
			elif btn != 0:
				self._user_entry[self._user_entry_index] = chr(btn)
				self.print_debug( ''.join(self._user_entry) )
				self._user_is_active = True # TimeOut does apply only when user is active
				self.fire_on_update( False )
				if self.check_entry():
					self.print_debug( 'KeyCode Correct' )
					self._user_is_active = False
					return True

				self._user_entry_index += 1
				if self._user_entry_index == len(self._key_code[0]):
					self._user_entry_index = 0 # Reset
					self.print_debug( ''.join(self._user_entry) )
					self.clear_entry()
					self.print_debug( ''.join(self._user_entry) )
					self.fire_on_update( False )
				self._timeout_counter = 0 # Reset with any new presses

			time.sleep_ms( 200 )
			self._timeout_counter += 1

			# This means that user is actively inputing
			if (self._timeout_counter == self._timeout):
				if self._user_is_active: # User is trying to get the code (give him chance to do it)
					self.print_debug( 'TimeOut! Try again...' )
					self._timeout_counter = 0
					self._user_entry_index = 0
					self.clear_entry()
					self.fire_on_update( True )
					self._user_is_active = False # Dont continuously timeout while inactive
				else:
					self.print_debug( 'TimeOut and Inactive user!' )
					self.print_debug( 'exit execute()' )
					return False

	def print_debug( self, str ):
		if self._debug:
			print( 'DEBUG:', str )

	@property
	def debug( self ):
		return self._debug

	@debug.setter
	def debug( self, value ):
		self._debug = value

	@property
	def on_update( self ):
		""" on_update callback """
		return self._on_update

	@property
	def user_entry( self ):
		""" Entry as encoded by the user. Including padding spaces """
		return ''.join( self._user_entry )

	@on_update.setter
	def on_update( self, func ):
		""" set it with callback function( user_entry_string, timeout_bool ) """
		self._on_update = func

	def fire_on_update( self, timeout_state ):
		if self._on_update != None:
			self._on_update( ''.join(self._user_entry), timeout_state )

	def clear_entry( self ):
		self._user_entry_index = 0
		for i in range( len(self._user_entry) ):
			self._user_entry[i] = ' '

	def check_entry( self ):
		_result = False
		_len = len( self._key_code[0] )
		for _code in self._key_code:
			if all( [self._user_entry[i] == _code[i] for i in range(_len)] ):
				return True
		return False
