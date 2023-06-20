""" 74hc595, Shift Register - driver for MicroPython

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/74hc595
"""

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"

from machine import Pin
import time

class ShiftReg:
	def __init__( self, datapin, clkpin, latchpin, rstpin ):
		""" Must receive the Pin instance for various signals. Will reconfigure the pins as appropriate """
		# Reset also named /SrcClr
		# Clock also named SrcClk
		# Latch also named RCLK
		self.data = datapin
		self.clk  = clkpin
		self.rst  = rstpin
		self.latch= latchpin

		self.data.init( Pin.OUT, value=False )
		self.clk.init( Pin.OUT, value=False )
		self.rst.init( Pin.OUT, value=True )
		self.latch.init(Pin.OUT, value=False )
		self.reset( latch=True )

	def reset( self, latch=False ):
		self.rst.value( False )
		time.sleep_us(1) # 100nS
		self.rst.value( True )
		if latch:
			time.sleep_us(1)
			self.latch.value( True )
			time.sleep_us(1)
			self.latch.value( False )
			time.sleep_us(1)


	def send_bit( self, value ):
		""" send a bit to the shift reguister """
		self.data.value( value )
		time.sleep_us(1) # 150nS before clocking
		self.clk.value( True )
		time.sleep_us(1) # 100nS high
		self.clk.value( False )
		time.sleep_us(1) # 100nS Low


	def write_byte( self, value, latch=True ):
		""" Write all the bit MSBF """
		self.latch.value( False )
		for i in range(8):
			bit = value & ( 1<<i )
			self.send_bit( bit )

		if latch:
			self.latch.value( True )
			time.sleep_us(1)
			self.latch.value( False )
			time.sleep_us(1)

	def write_bytes( self, values ):
		""" Write list of bytes on a daisy-chained shift-register.
		    values is a list of bytes : less significant byte first. """
		max_len = len(values)
		for idx in range(max_len):
			self.write_byte( values[idx], idx==(max_len-1) )

	def write_word( self, word ):
		""" Write a word (16 bits) on a DUAL daisy-chained shift-register.
		    Write is done with the Most Significant Bit first """
		hb = (word & 0xFF00)>>8
		lb = word & 0x00FF
		self.write_bytes( [lb,hb] )
