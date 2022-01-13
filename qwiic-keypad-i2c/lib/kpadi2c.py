"""
kpadi2c.py - I2C Qwiic Keypad driver (COM-15290, SparkFun)

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

Remarks:
  Original product API is descrived here. Function name are almost identicals.
  https://qwiic-keypad-py.readthedocs.io/en/latest/apiref.html#qwiic-keypad

------------------------------------------------------------------------

History:
  10 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""
import time

__version__ = "0.0.1"

REG_KEYPAD_ID             = const(0x00)
REG_KEYPAD_VERSION1       = const(0x01)
REG_KEYPAD_VERSION2       = const(0x02)
REG_KEYPAD_BUTTON         = const(0x03)
REG_KEYPAD_TIME_MSB       = const(0x04)
REG_KEYPAD_TIME_LSB       = const(0x05)
REG_KEYPAD_UPDATE_FIFO    = const(0x06)
REG_KEYPAD_CHANGE_ADDRESS = const(0x07)

class Keypad_I2C():
	def __init__( self, i2c, address=0x4B ):
		self.address = address
		self.i2c = i2c
		self.buf1 = bytearray(1)

	def read_reg( self, reg ):
		self.buf1[0] = reg
		self.i2c.writeto( self.address, self.buf1 )
		self.i2c.readfrom_into( self.address, self.buf1 )
		return self.buf1[0]

	def write_reg( self, reg, value ):
		self.buf1[0] = value
		self.i2c.writeto_mem( self.address, reg, self.buf1 )


	def update_fifo( self ):
		""" commands the keypad to plug in the next button into the registerMap """
		self.write_reg( REG_KEYPAD_UPDATE_FIFO, 0x01 )



	def change_address( self, new_addr ):
		""" Change the I2C address of this address to new_addr.
		 	ADR jumper should be closed for this to work"""
		assert 8 <= new_addr <= 119, "Address outside 8-119 range"

		self.write_reg( REG_KEYPAD_CHANGE_ADDRESS, new_addr ) # Does not seems to work

	@property
	def is_connected( self ):
		return self.address in self.i2c.scan()

	@property
	def version( self ):
		_major = self.read_reg( REG_KEYPAD_VERSION1 )
		_minor = self.read_reg( REG_KEYPAD_VERSION2 )
		return "v%s.%s" % (_major,_minor)

	@property
	def button( self ):
		"""  Returns the button at the top of the stack (oldest pressed).
			value is the 'ascii' code. """
		return self.read_reg( REG_KEYPAD_BUTTON )

	@property
	def time_since_pressed( self ):
		""" Returns the number of milliseconds since the current button in FIFO was pressed. """
		_msb = self.read_reg( REG_KEYPAD_TIME_MSB)
		_lsb = self.read_reg( REG_KEYPAD_TIME_LSB)
		return ((_msb << 8) | _lsb)
