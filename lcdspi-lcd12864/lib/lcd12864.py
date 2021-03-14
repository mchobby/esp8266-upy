"""" lcd12864 is a FrameBuffer based MicroPython driver for the graphical
     LiquidCrystal LCD12864 display (also known as DFR0091).

LCD-128x64-WHITE-SPI : https://shop.mchobby.be/fr/gravity-boson/1878-afficheur-lcd-128x64-spi-3-fils-3232100018785-dfrobot.html
LCD-128x64-WHITE-SPI : https://www.dfrobot.com/product-372.html

see project: https://github.com/mchobby/esp8266-upy/tree/master/lcdspi-lcd12864

Author:
  08 march 2020 - Domeu - initial code writing

The MIT License (MIT) - see LICENSE file
"""


import framebuf
import time

LCD_X_RES = 128
LCD_Y_RES = 64

DELAY_US = 80

class SPI_LCD12864( framebuf.FrameBuffer ):
	def __init__( self, spi, cs, width = LCD_X_RES, height = LCD_Y_RES ):
		""" constructor

			:param spi: initialized spi bus (only mosi is used)
			:param cs: slave select pin for the SPI bus
		"""
		# Driving the LCD3310
		self.spi = spi
		self.cs = cs

		# Other properties
		self.height = height
		self.width  = width
		self._buf1 = bytearray( 1 ) # 1 byte data

		# Initialize the FrameBuffer
		_bufsize = (self.width * self.height)//8
		self._buffer = bytearray( _bufsize ) # 8 pixels per Bytes MONO_VLSB (1bit/pixel, 7th bit the topmost pixel)
		super().__init__(
						self._buffer,
						self.width, # pixels width
						self.height, # pixels height
						framebuf.MONO_HLSB # 1 bit per pixel, 7th bit the leftmost pixel
				)
		# Initilize controler
		self._begin()
		# Clear and Update
		self.clear()

	def _write_byte( self, dat ):
		self.cs.value( 1 )
		time.sleep_us( DELAY_US )
		self._buf1[0] = dat
		self.spi.write( self._buf1 )
		self.cs.value( 0 )

	def _write_cmd( self, cmd ):
		self._write_byte( 0xF8 )
		self._write_byte( cmd & 0xF0 )
		self._write_byte( (cmd & 0x0F) << 4 )

	def _write_dat( self, dat ):
		self._write_byte( 0xfa )
		self._write_byte( dat & 0xF0 )
		self._write_byte( (dat & 0x0F) << 4 )

	def _begin(self):
		""" Initialize the LCD controler """
		self._write_cmd( 0x30 )
		self._write_cmd( 0x0c )
		self._write_cmd( 0x01 )
		self._write_cmd( 0x06 )
		time.sleep_us( DELAY_US ) # Don't start too fast

	def clear( self ):
		self.fill( 0 ) # Clear FrameBuffer
		self._write_cmd( 0x30 ) # Send clear @ LCD
		self._write_cmd( 0x01 )

	def update( self ):
		# Send FrameBuffer to lcd
		for ygroup in range(64):
			if ygroup<32:
				x=0x80
				y=ygroup+0x80
			else:
				x=0x88
				y=ygroup-32+0x80

			self._write_cmd(0x34)
			self._write_cmd(y)
			self._write_cmd(x)
			self._write_cmd(0x30)
			for i in range(16):
				self._write_dat(self._buffer[(ygroup*16)+i])

		self._write_cmd(0x34)
		self._write_cmd(0x36)
