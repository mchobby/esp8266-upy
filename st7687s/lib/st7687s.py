# The MIT License (MIT)
#
# Copyright (c) 2020 Meurisse D. fro MC Hobby
#

"""
st7687s.py : MicroPython driver for the ST7687S LATCH driver for TFT.


* Author(s):
   21 apr 2020: Meurisse D. (shop.mchobby.be) - portage from Arduino code
   17 aug 2018: DFRobot Arduino's version - https://github.com/DFRobot/DFRobot_ST7687S

"""
from time import sleep_ms, sleep_us

BEGIN_WAR_NOTEST = 1 # Strange DFRobot constant with unknown value

class HC595_SPI:
	def __init__( self, spi, pin_rck ):
		self.pin_rck = pin_rck
		self.spi = spi

	def begin( self ):
		self.writeRCK( 0 )

	def writeRCK( self, value ):
		self.pin_rck.value( value )

	def delay_us( self ):
		sleep_us( 1 )

	def writeDat( self, dat ):
		self.spi.write( bytes([dat]) )

	def writeReg( self, dat, action ):
		self.writeDat( dat )
		if action:
			self.writeRCK( 1 )
			self.delay_us()
			self.writeRCK( 0 )

class ST7687S:
	def __init__( self, spi, cs ):
		""" initializer

			:param spi: initialized bus in mode 0, MSBFirst
			:param cs:  chip select pin (initialized) """
		self.spi = spi
		self.cs  = cs
		self.cs.value( 1 ) # disable slave


class ST7687S_Latch( ST7687S ):
	def __init__( self, spi, cs, rs, wr, lck ):
		super( ST7687S_Latch, self ).__init__(spi,cs)
		self.rs = rs
		self.wr = wr
		self.hc595 = HC595_SPI( spi, lck ) # the LCK pin is also named RCK
		self.hc595.begin()

		self.cs.value( 1 )
		self.rs.value( 1 ) # also named pin_cd
		self.hc595.pin_rck.value( 1 ) # Also name lck
		self.wr.value( 1 )

		self._begin() # Initialize the screen

	def _begin(self):
		def _writeCD(cmd,dat):
			self.writeCmd(cmd)
			self.writeDat(dat)

		sleep_ms(120)
		_writeCD(0xd7,0x9f)
		_writeCD(0xE0,0x00)
		sleep_ms(200)
		_writeCD(0xFA,0x01)
		sleep_ms(100)
		self.writeCmd(0xE3) # Read from EEPROM
		sleep_ms(200)
		self.writeCmd([0xE1,0x28,0x11])
		sleep_ms(50)
		_writeCD(0xc0,[0x17,0x01])
		_writeCD(0x25,0x1E)
		_writeCD(0xC3,0x03)
		_writeCD(0xC4,0x07)
		_writeCD(0xC5,0x01)
		_writeCD(0xCB,0x01)
		_writeCD(0xB7,0x00)
		_writeCD(0xD0,0x1d)
		_writeCD(0xB5,0x89)
		_writeCD(0xBD,0x02)
		_writeCD(0xF0,[0x07,0x0C,0x0C,0x12])
		_writeCD(0xF4,[0x33,0x33,0x33,0x00,0x33,0x66,0x66,0x66])
		self.writeCmd(0x20)
		_writeCD(0x2A,[0x00,0x7F])
		_writeCD(0x2B,[0x00,0x7f])
		_writeCD(0x3A,0x05)
		_writeCD(0x36,0x80)
		_writeCD(0xB0,0x7F)
		self.writeCmd(0x29) # Display On
		_writeCD(0xF9,[0x00,0x02,0x04,0x06,0x08,0x0a,0x0c,0x0e,0x10,0x12,0x14,0x16,0x18,0x1A,0x1C,0x1E])
		self.writeCmd(0x29) # Display on
		return BEGIN_WAR_NOTEST

	def writeCmdDat( self, value, is_cmd=True ):
		def _write( dat ):
			self.rs.value( 0 if is_cmd else 1 ) # rs=0 for send Cmd, rs=1 for send Data
			self.cs.value( 0 )
			self.hc595.writeReg( dat, 1 )
			self.wr.value( 0 )
			self.hc595.delay_us()
			self.wr.value( 1 )
			self.cs.value( 1 )
		if type(value) is list: # write a list of data OR a simple data
			for data in value:
				_write(data)
		else:
			_write(value)

	def writeCmd( self, cmd ):
		self.writeCmdDat( cmd, is_cmd=True )

	def writeDat( self, dat ):
		self.writeCmdDat( dat, is_cmd=False )

	def writeDatBytes(self, pDat): # pDat is a buffer
		self.rs.value( 1 ) # Pin command High
		self.cs.value( 0 )
		for value in pDat:
			self.hc595.writeReg( value, 1 )
			self.wr.value( 0 )
			self.hc595.delay_us()
			self.wr.value( 1 )
			self.hc595.delay_us()
		self.cs.value( 1 )

	def writeRepeatPixel(self, color, count, repeatCount ):
		""" Send the data for a series of pixels.
		   writeToRam() must have been called first """
		colorBuf = bytes( [(color >> 8) & 0xFF, color & 0xFF] )
		for i in range(repeatCount * count):
			self.writeDatBytes(colorBuf)

	def setCursorAddr(self, x0, y0, x1, y1): # 16 bits
		""" Define the column address X and row address Y to access tge Frame Memory
			:param x0: XStart for column start (0-127)
			:param x1: XEnd
			:param y0: YStart for row start  (0-127)
			:param y1: YEnd """
		self.writeCmd(0x2A) # CASET: column Adrress Set
		self.writeDat( [x0,x1] )
		self.writeCmd(0x2b)
		self.writeDat( [y0,y1] )

	def writeToRam( self ):
		""" Start writing in Frame memory """
		self.writeCmd(0x2C)

	# --- Utilities ---
	def turn_on( self, value ):
		""" Turn display On of Off """
		self.writeCmd( 0x29 if value else 0x28 )
