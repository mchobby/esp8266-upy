"""
joyi2c.py : MicroPython driver for M5Stack U024/U024-, I2C based analog Joystick grove unit.

* Author(s):
   22 aug 2022: Meurisse D. (shop.mchobby.be) - port to MicroPython
	https://github.com/m5stack/M5Stack/tree/master/examples/Unit/JOYSTICK
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u024"

from micropython import const
import time
import struct

class Joystick:
	def __init__(self, i2c, addr=0x52 ):
		self.i2c = i2c
		self.addr = addr

		self._x = 0 # See update()
		self._y = 0
		self._button = 0
		# Buffer
		self.buf3 = bytearray(3)

		self.update()

	def update( self ):
		self.i2c.readfrom_into( self.addr, self.buf3 )
		self._x, self._y, self._button = struct.unpack( "<BBB", self.buf3 )

	@property
	def x( self ):
		return self._x

	@property
	def y( self ):
		return self._y

	@property
	def button( self ):
		return self._button > 0
