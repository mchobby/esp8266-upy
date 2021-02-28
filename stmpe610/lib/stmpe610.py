# Library for the Resistive Touch sensor (SPI interface)
#
# Project home: https://github.com/mchobby/esp8266-upy/tree/master/stmpe610
#
# Based on Adafruit_STMPE610.cpp available at https://github.com/adafruit/Adafruit_STMPE610/blob/master/Adafruit_STMPE610.cpp
#
from micropython import const
from time import sleep_us, sleep_ms
from machine import Pin

__version__ = '0.0.1'

# Reset Control
STMPE_SYS_CTRL1 = const(0x03)
STMPE_SYS_CTRL1_RESET = const(0x02)

# Clock Contrl
STMPE_SYS_CTRL2 = const(0x04)

# Touchscreen controller setup
STMPE_TSC_CTRL = const( 0x40 )
STMPE_TSC_CTRL_EN = const( 0x01 )
STMPE_TSC_CTRL_XYZ = const( 0x00 )
STMPE_TSC_CTRL_XY = const( 0x02 )

# Interrupt control
STMPE_INT_CTRL  = const( 0x09 )
STMPE_INT_CTRL_POL_HIGH = const( 0x04 )
STMPE_INT_CTRL_POL_LOW = const( 0x00 )
STMPE_INT_CTRL_EDGE = const( 0x02 )
STMPE_INT_CTRL_LEVEL = const( 0x00 )
STMPE_INT_CTRL_ENABLE = const( 0x01 )
STMPE_INT_CTRL_DISABLE = const( 0x00 )

# Interrupt enable
STMPE_INT_EN = const( 0x0A )
STMPE_INT_EN_TOUCHDET = const( 0x01 )
STMPE_INT_EN_FIFOTH = const( 0x02 )
STMPE_INT_EN_FIFOOF = const( 0x04 )
STMPE_INT_EN_FIFOFULL = const( 0x08 )
STMPE_INT_EN_FIFOEMPTY = const( 0x10 )
STMPE_INT_EN_ADC = const( 0x40 )
STMPE_INT_EN_GPIO = const( 0x80 )

# Interrupt status
STMPE_INT_STA = const( 0x0B )
STMPE_INT_STA_TOUCHDET = const( 0x01 )

# ADC control
STMPE_ADC_CTRL1 = const( 0x20 )
STMPE_ADC_CTRL1_12BIT = const( 0x08 )
STMPE_ADC_CTRL1_10BIT = const( 0x00 )

STMPE_ADC_CTRL2 = const( 0x21 )
STMPE_ADC_CTRL2_1_625MHZ = const( 0x00 )
STMPE_ADC_CTRL2_3_25MHZ = const( 0x01 )
STMPE_ADC_CTRL2_6_5MHZ = const( 0x02 )

# Touchscreen controller configuration
STMPE_TSC_CFG = const( 0x41 )
STMPE_TSC_CFG_1SAMPLE = const( 0x00 )
STMPE_TSC_CFG_2SAMPLE = const( 0x40 )
STMPE_TSC_CFG_4SAMPLE = const( 0x80 )
STMPE_TSC_CFG_8SAMPLE = const( 0xC0 )
STMPE_TSC_CFG_DELAY_10US = const( 0x00 )
STMPE_TSC_CFG_DELAY_50US = const( 0x08 )
STMPE_TSC_CFG_DELAY_100US = const( 0x10 )
STMPE_TSC_CFG_DELAY_500US = const( 0x18 )
STMPE_TSC_CFG_DELAY_1MS = const( 0x20 )
STMPE_TSC_CFG_DELAY_5MS = const( 0x28 )
STMPE_TSC_CFG_DELAY_10MS = const( 0x30 )
STMPE_TSC_CFG_DELAY_50MS = const( 0x38 )
STMPE_TSC_CFG_SETTLE_10US = const( 0x00 )
STMPE_TSC_CFG_SETTLE_100US = const( 0x01 )
STMPE_TSC_CFG_SETTLE_500US = const( 0x02 )
STMPE_TSC_CFG_SETTLE_1MS = const( 0x03 )
STMPE_TSC_CFG_SETTLE_5MS = const( 0x04 )
STMPE_TSC_CFG_SETTLE_10MS = const( 0x05 )
STMPE_TSC_CFG_SETTLE_50MS = const( 0x06 )
STMPE_TSC_CFG_SETTLE_100MS = const( 0x07 )

# FIFO level to generate interrupt
STMPE_FIFO_TH = const( 0x4A )

# Current filled level of FIFO
STMPE_FIFO_SIZE = const( 0x4C )

# Current status of FIFO
STMPE_FIFO_STA = const( 0x4B )
STMPE_FIFO_STA_RESET = const( 0x01 )
STMPE_FIFO_STA_OFLOW = const( 0x80 )
STMPE_FIFO_STA_FULL = const( 0x40 )
STMPE_FIFO_STA_EMPTY = const( 0x20 )
STMPE_FIFO_STA_THTRIG = const( 0x10 )

# Touchscreen controller drive I
STMPE_TSC_I_DRIVE = const( 0x58 )
STMPE_TSC_I_DRIVE_20MA = const( 0x00 )
STMPE_TSC_I_DRIVE_50MA = const( 0x01 )

# Data port for TSC data address
STMPE_TSC_DATA_X = const( 0x4D )
STMPE_TSC_DATA_Y = const( 0x4F )
STMPE_TSC_FRACTION_Z = const( 0x56 )

# GPIO
STMPE_GPIO_SET_PIN = const( 0x10 )
STMPE_GPIO_CLR_PIN = const( 0x11 )
STMPE_GPIO_DIR = const( 0x13 )
STMPE_GPIO_ALT_FUNCT = const( 0x17 )

class STMPE610:
	def __init__(self, spi, cs ):
		# :param spi: initialized @ 1 MHz, MSBFirst, SPI_MODE1 (mode 0 does not return the proper version number)
		# :param cs : ChipSelect / SlaveSelect
		# :param r  : Rotation : 1 & 3 = __landscape__ with width=320 height=240
		#              : 0 & 2 = __portrait__ with width=240 height=320
		self.spi = spi
		self.cs = cs

		self.cs.init( Pin.OUT, value=True )
		self.buf4 = bytearray(4)
		self.init()

	def init( self ):
		ver = self.version
		if ver != 0x811:
			raise Exception('Invalid chip version 0x%x (expected 0x811) or incorrect SPI_MODE1' % ver )

		self.write_reg8(STMPE_SYS_CTRL1, STMPE_SYS_CTRL1_RESET)
		sleep_ms(10)

		for i in range( 65 ):
			self.read_reg8( i )

		self.write_reg8( STMPE_SYS_CTRL2, 0x0) # turn on clocks!
		self.write_reg8( STMPE_TSC_CTRL, STMPE_TSC_CTRL_XYZ | STMPE_TSC_CTRL_EN) # XYZ and enable!
		self.write_reg8( STMPE_INT_EN, STMPE_INT_EN_TOUCHDET )
		self.write_reg8( STMPE_ADC_CTRL1, STMPE_ADC_CTRL1_10BIT | (0x6 << 4) ) # 96 clocks per conversion
		self.write_reg8( STMPE_ADC_CTRL2, STMPE_ADC_CTRL2_6_5MHZ )
		self.write_reg8( STMPE_TSC_CFG, STMPE_TSC_CFG_4SAMPLE | STMPE_TSC_CFG_DELAY_1MS | STMPE_TSC_CFG_SETTLE_5MS )
		self.write_reg8( STMPE_TSC_FRACTION_Z, 0x6 )
		self.write_reg8( STMPE_FIFO_TH, 1 )
		self.write_reg8( STMPE_FIFO_STA, STMPE_FIFO_STA_RESET )
		self.write_reg8( STMPE_FIFO_STA, 0 ) # unreset
		self.write_reg8( STMPE_TSC_I_DRIVE, STMPE_TSC_I_DRIVE_50MA )
		self.write_reg8( STMPE_INT_STA, 0xFF ) # reset all ints
		self.write_reg8( STMPE_INT_CTRL, STMPE_INT_CTRL_POL_HIGH | STMPE_INT_CTRL_ENABLE )

	def read_reg8( self, reg ):
		sleep_us( 10 )
		self.cs.value( False )
		sleep_us( 10 )
		self.spi.write( bytes([0x80 | reg, 0x00]) )
		sleep_us( 10 )
		data = self.spi.read( 1 )
		self.cs.value( True )
		return data[0]

	def write_reg8( self, reg, value ): # reg, value must be bytes
		sleep_us( 10 )
		self.cs.value( False )
		sleep_us( 10 )
		self.spi.write( bytes([reg, value]) )
		self.cs.value( True )

	def read_data( self ):
		""" Returns (x,y,z) values from the device """
		for i in range(4):
			self.buf4[i] = self.read_reg8( 0xD7 )

		x = (self.buf4[0] << 4)
		x |= (self.buf4[1] >> 4)
		y = ((self.buf4[1] & 0x0F) << 8)
		y |= self.buf4[2]
		z = self.buf4[3]
		return (x,y,z)

	@property
	def version( self ):
		""" Returns the STMPE version """
		v = self.read_reg8(0)
		v <<= 8
		v |= self.read_reg8(1)
		return v

	@property
	def touched( self ):
		return (self.read_reg8(STMPE_TSC_CTRL) & 0x80) > 0

	@property
	def buffer_size( self ):
		""" STMPE buffer size as integer """
		return self.read_reg8( STMPE_FIFO_SIZE )

	@property
	def buffer_empty( self ):
		return (self.read_reg8(STMPE_FIFO_STA) & STMPE_FIFO_STA_EMPTY) == STMPE_FIFO_STA_EMPTY

	@property
	def point( self ):
		""" Returns point for touchscreen data as a TS_Point reference """
		# Making sure that we are reading all data before leaving
		coord = None
		while not( self.buffer_empty ):
			coord = self.read_data()

		if self.buffer_empty:
			self.write_reg8( STMPE_INT_STA, 0xFF ) # reset all ints

		return coord

	@property
	def points( self ):
		""" pop-off all the points from the STMPE fifo and return them as a list """
		r = []
		last = None
		# To finish
