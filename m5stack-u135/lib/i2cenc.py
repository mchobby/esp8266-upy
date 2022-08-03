"""
mdds.py : MicroPython driver for M5Stack U105, 4 relays I2C grove unit.
* Author(s):
   28 may 2021: Meurisse D. (shop.mchobby.be) - port to MicroPython
				https://github.com/m5stack/M5Stack/tree/master/examples/Unit/DDS_AD9833
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u105"

from micropython import const
import struct

# ENCODER_ADDR 0x40
ENCODER_REG = const(0x10)
BUTTON_REG  = const(0x20)
RGB_LED_REG = const(0x30)

class I2CEncoder:
	""" Drive the I2C Encoder unit (U135)
		:param i2c: the connected i2c bus machine.I2C
		:param address: the device address; defaults to 0x40 """

	def __init__(self, i2c, address=0x40):
		self.i2c = i2c
		self.address = address
		self.buf4 = bytearray(4)
		self.buf2 = bytearray(2)
		self.buf1 = bytearray(1)
		self._color = (0,0,0) # Last known color

	def set_led( self, index, value ):
		""" 0: all leds, otherwise: LED index (1..n) """
		self.buf4[0] = index # Index
		self.buf4[1] = value[0] # R
		self.buf4[2] = value[1] # G
		self.buf4[3] = value[2] # B
		self.i2c.writeto_mem( self.address,RGB_LED_REG, self.buf4 )
		self._color = value

	@property
	def position( self ):
		# -32768 <= encoder_position <= 32767
		self.i2c.readfrom_mem_into( self.address, ENCODER_REG, self.buf2 )
		_r = struct.unpack( "<h", self.buf2 ) # signed short
		return _r[0]

	@position.setter
	def position( self, value ):
		# -32768 <= encoder_position <= 32767
		assert -32768 <= value <= 32767
		struct.pack_into( "<h", self.buf2, 0, value ) # @ offset 0
		self.i2c.writeto_mem( self.address, ENCODER_REG, self.buf2 )

	@property
	def button( self ):
		""" Return 1 if the button is currently pressed """
		self.i2c.readfrom_mem_into( self.address, BUTTON_REG, self.buf1 )
		return self.buf1[0]==0 # Yo! currently pressed

	@property
	def color( self ):
		# return last know value
		return self._color

	@color.setter
	def color( self, value ):
		""" set all the LEDs to (r,g,b) value """
		self.set_led( 0, value )

class I2CRelEncoder( I2CEncoder ):
	""" Super class to workaround the counter reset isssue (in encoder firmware) """
	def __init__(self, i2c, address=0x40):
		super().__init__( i2c, address )
		self._ref = 0 # Reference to return the position
		self.reset()

	def reset( self ):
		self._ref = self.position

	@property
	def rel_position( self ):
		return self.position - self._ref
