"""
IRDA+ Infrared I2C module with support of RC5 (Philips) and SIRCS protocols
===========================================================================
This library supports the MOD-IRDA+ from Olimex under MicroPython.

Products:
---> https://shop.mchobby.be/fr/pico-rp2040/2037-interface-hat-pour-raspberry-pi-pico-3232100020375.html
---> https://www.olimex.com/Products/Modules/Interface/MOD-IRDA+/open-source-hardware

MCHobby investit du temps et des ressources pour écrire de la
                documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.
------------------------------------------------------------------------
History:
  06 july 2021 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const
import time

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"

CMD_SET_ADDRESS = const( 0xF0 )
CMD_GET_ID	= const( 0x20 )
CMD_SET_MODE= const( 0x01 )
CMD_WRITE	= const( 0x02 )
CMD_READ 	= const( 0x03 )

MODE_SIRC = const( 0x01 )
MODE_RC5  = const( 0x00 )

IRDA_ID = const( 0x54 )

class IrdaPlus:
	def __init__( self, i2c, address=0x24 ):
		self.address = address
		self.i2c = i2c
		self.mode = None
		self.buf1 = bytearray(1)
		self.buf2 = bytearray(2)
		self.buf3 = bytearray(3)
		if self.get_id() != IRDA_ID:
			raise Exception( 'Invalid module ID!')
		self.set_mode( MODE_SIRC ) # Sony remote are more popular

	def _reverse( self, data, len ):
		reverse = 0
		for i in range( len ):
			reverse <<= 1
			reverse |= 1 if (data & (1<<i)) else 0
		return reverse

	def get_id( self ):
		self.buf1[0] = CMD_GET_ID
		self.i2c.writeto( self.address, self.buf1 )
		self.i2c.readfrom_into( self.address, self.buf1 )
		return self.buf1[0]

	def set_mode( self, mode ):
		self.mode = mode
		self.buf2[0] = CMD_SET_MODE
		self.buf2[1] = mode
		self.i2c.writeto( self.address, self.buf2 )
		return self.buf1[0]

	def read_data( self ):
		""" Read raw data containing remote commande and devive adress.
		    May returns None if nothing detected. """
		self.buf1[0] = CMD_READ
		self.i2c.writeto( self.address, self.buf1 )
		self.i2c.readfrom_into( self.address, self.buf2 )
		val = self.buf2[0]<<8 | self.buf2[1]
		return val if val!=65535 else None

	def read_command( self ):
		""" Read raw THEN extract the (device_address, command) from raw data. RC5 decoding append the Toggle flag. """
		val = self.read_data()
		if val==None:
			return None

		if self.mode==MODE_RC5:
			command = val & 0x3F
			device = (val >> 6) & 0x1F
			toggle = True if (val >> 11) & 0x01 else False
			return ( device, command, toggle )
		elif self.mode==MODE_SIRC:
			device = self._reverse( val & 0x1F, 5 )
			command = self._reverse( (val>>5) & 0x7F, 7 )
			return ( device, command )
		else:
			raise Exception( 'Unsupported mode!')

	def send_command( self, device, cmd ):
		""" Send a 'cmd' command to the target 'device' address. """
		self.buf3[0] = CMD_WRITE
		self.buf3[1] = device # device address
		self.buf3[2] = cmd  # command
		self.i2c.writeto( self.address, self.buf3 )
