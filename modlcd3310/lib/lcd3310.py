""" lcd3310 is a FrameBuffer based MicroPython driver for the Olimex MOD-LCD3310 or Nokia 3310 display.

MOD-LCD3310 : http://shop.mchobby.be/product.php?id_product=1867
MOD-LCD3310 : https://www.olimex.com/Products/Modules/LCD/MOD-LCD3310/open-source-hardware

see project: https://github.com/mchobby/esp8266-upy/tree/master/modlcd3310

Author:
  20 july 2020 - Domeu - initial code writing

The MIT License (MIT) - see LICENSE file
"""

import time
import framebuf

LCD_START_LINE_ADDR	= 66-3 # cannot be greater than 66

LCD_X_RES = 84
LCD_Y_RES = 48

class LCD3310( framebuf.FrameBuffer ):
	def __init__( self, spi, ssel, lcd_reset, lcd_data, width = LCD_X_RES, height = LCD_Y_RES ):
		""" constructor

			:param spi: initialized spi bus (only mosi is used)
			:param ssel: slave select pin for the SPI bus
			:param lcd_reset: pin that will handle the LCD_RESET signal
			:param lcd_data: pin that will handle the LCD_DATA signal (Data/Command)
		"""
		# Driving the LCD3310
		self.spi = spi
		self.lcd_reset = lcd_reset
		self.lcd_data  = lcd_data
		self.ssel = ssel

		# Other properties
		self.height = height
		self.width  = width
		self._contrast = 72 # default contrast

		# Initialize the FrameBuffer
		_bufsize = (self.width * self.height)//8
		self._buffer = bytearray( _bufsize ) # 8 pixels per Bytes MONO_VLSB (1bit/pixel, 7th bit the topmost pixel)
		super().__init__(
						self._buffer,
						self.width, # pixels width
						self.height, # pixels height
						framebuf.MONO_VLSB # 1 bit per pixel, 7th bit the topmost pixel
				)
		# Initilize controler
		self._begin()
		# Clear and Update
		self.clear()
		self.update()

	def _lcd_send( self, data, cmd ):
		""" send data over SPI either as command cmd=True either as real data cmd=False """
		self.ssel.value( False )
		self.lcd_data.value( not(cmd) ) # cmd==True --> lcd_data=LOW
		# send the data over SPI
		if (type( data ) is list):
			self.spi.write( bytearray(data) )
		elif (type(data) is bytearray):
			self.spi.write( data )
		else:
			self.spi.write( bytearray([data]))
		self.ssel.value( True )

	def _begin(self):
		""" Initialize the LCD controler """
		self.ssel.value( True )

		# Toggle reset pin
		self.lcd_reset.value( False )
		time.sleep_ms( 5 )
		self.lcd_reset.value( True )
		time.sleep_ms( 5 )

		# Send sequence of command
		self._lcd_send( 0x21, cmd=True ) # LCD Extended Commands.
		self._lcd_send( 0xC8, cmd=True) # Set LCD Vop (Contrast). 0xC8
		self._lcd_send( 0x04 | (LCD_START_LINE_ADDR & (1 << 6)), cmd=True ) # Set Temp S6 for start line
		self._lcd_send( 0x40 | (LCD_START_LINE_ADDR & ((1 << 6) - 1)), cmd=True ) # Set Temp S[5:0] for start line
		# self._lcd_send( 0x13, cmd=True )  # LCD bias mode 1:48.
		self._lcd_send( 0x12, cmd=True ) # LCD bias mode 1:68.
		self._lcd_send( 0x20, cmd=True ) # LCD Standard Commands, Horizontal addressing mode.
		# self._lcd_send( 0x22, cmd=True )   LCD Standard Commands, Vertical addressing mode.
		self._lcd_send( 0x08, cmd=True ) # LCD blank
		self._lcd_send( 0x0C, cmd=True ) # LCD in normal mode.

	def clear( self ):
		self.fill( 0 ) # All transparent pixels

	@property
	def contrast( self ):
		return self._contrast

	@contrast.setter
	def contrast( self, value ):
		assert 0<= value <= 127, "value from 0..127"
		#  LCD Extended Commands.
		self._lcd_send( 0x21, cmd=True )
		# Set LCD Vop (Contrast).
		self._lcd_send( 0x80 | value, cmd=True )
		# LCD Standard Commands, horizontal addressing mode.
		self._lcd_send( 0x20, cmd=True )


	def update( self ):
		# Ported from
		# https://github.com/OLIMEX/UEXT-MODULES/blob/master/MOD-LCD3310/Software/Arduino(AVR)/lcd3310_GPIO.c
		for y in range( self.height//8 ):
			self._lcd_send( 0x80, cmd=True ) # X address in RAM 0x80 + 0..83(dec)
			self._lcd_send( 0x40 | y, cmd=True ) # y Bank address in RAM 0x40 + 0..6
			self._lcd_send( self._buffer[y*84:(y+1)*84], cmd=False )
