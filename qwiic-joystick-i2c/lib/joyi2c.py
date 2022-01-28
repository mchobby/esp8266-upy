"""
joyi2c.py - I2C Qwiic Joystick driver (COM-15168, SparkFun)
* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic Joystick   : https://www.sparkfun.com/products/15168
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
Remarks:
  More information stored onto the GitHub.
  https://github.com/sparkfun/Qwiic_Joystick/
------------------------------------------------------------------------
History:
  27 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const

REG_ID       = const(0x00)
REG_VERSION1 = const(0x01)
REG_VERSION2 = const(0x02)
REG_X_MSB    = const(0x03)
REG_X_LSB    = const(0x04)
REG_Y_MSB    = const(0x05)
REG_Y_LSB    = const(0x06)
REG_BUTTON   = const(0x07)
REG_STATUS   = const(0x08) # 1 - button clicked
REG_I2C_LOCK = const(0x09)
REG_CHANGE_ADDRESS  = const(0x0A)

__version__ = "0.0.1"

class Joystick_I2C():
	def __init__( self, i2c, address=0x20 ):
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


	def change_address( self, new_addr ):
		""" Change the I2C address of this address to new_addr. """
		assert 8 <= new_addr <= 119, "Address outside 8-119 range"

		self.write_reg( REG_CHANGE_ADDRESS, new_addr ) # Does not seems to work

	def change_address( self, new_addr ):
		""" Change the I2C address of this address to new_addr.
		 	ADR jumper should be closed for this to work"""
		assert 8 <= new_addr <= 119, "Address outside 8-119 range"
		self.write_reg( REG_KEYPAD_CHANGE_ADDRESS, new_addr ) # Does not seems to work

	@property
	def version( self ):
		_major = self.read_reg( REG_VERSION1 )
		_minor = self.read_reg( REG_VERSION2 )
		return "v%s.%s" % (_major,_minor)

	@property
	def pressed( self ):
		"""  Returns True is the button is currently pressed. """
		return self.read_reg( REG_BUTTON )==0

	@property
	def was_pressed( self ):
		"""  Check if the button has been pressed and released between
			2 consecutives I2C access to the joystick. """
		status = self.read_reg( REG_STATUS )
		# Reset status bit
		self.write_reg( REG_STATUS, 0x00 )
		return status>0

	@property
	def x( self ):
		""" Returns the 10-bit ADC value for horizontal position (0..1024)"""
		return (( self.read_reg(REG_Y_MSB)<<8 )+ self.read_reg(REG_Y_LSB))>>6

	@property
	def y( self ):
		""" Returns the 10-bit ADC value for vertical position (0..1024)"""
		return (( self.read_reg(REG_X_MSB)<<8 )+ self.read_reg(REG_X_LSB))>>6

	@property
	def is_connected( self ):
		return self.address in self.i2c.scan()
