"""
alight.py : MicroPython driver for M5Stack U136/U134, Ambiant Light Sensor based on BH1750FVI I2C sensor.

* Author(s):
   22 aug 2022: Meurisse D. (shop.mchobby.be) - port to MicroPython
	https://github.com/m5stack/M5-DLight
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u136"

from micropython import const
import time
import struct

POWER_DOWN                      =const( 0b00000000 )
POWER_ON                        =const( 0b00000001 )
RESET                           =const( 0b00000111 )
CONTINUOUSLY_H_RESOLUTION_MODE  =const( 0b00010000 )
CONTINUOUSLY_H_RESOLUTION_MODE2 =const( 0b00010001 )
CONTINUOUSLY_L_RESOLUTION_MODE  =const( 0b00010011 )
ONE_TIME_H_RESOLUTION_MODE      =const( 0b00100000 )
ONE_TIME_H_RESOLUTION_MODE2     =const( 0b00100001 )
ONE_TIME_L_RESOLUTION_MODE      =const( 0b00100011 )

class AmbiantLight:
	def __init__(self, i2c, addr=0x23 ):
		self.i2c = i2c
		self.addr = addr
		# Buffer
		self.buf1 = bytearray(1)
		self.buf2 = bytearray(2)
		self.power_on()

	def power_on( self ):
		self.buf1[0] = POWER_ON
		self.i2c.writeto( self.addr, self.buf1 )

	def power_off( self ):
		self.buf1[0] = POWER_OFF
		self.i2c.writeto( self.addr, self.buf1 )

	def reset( self ):
		self.buf1[0] = RESET
		self.i2c.writeto( self.addr, self.buf1 )

	def set_mode( self, mode ): # byte
		self.buf1[0] = mode
		self.i2c.writeto( self.addr, self.buf1 )

	@property
	def lux( self ):
		self.i2c.readfrom_into( self.addr, self.buf2 )
		return struct.unpack( ">H", self.buf2 )[0]
