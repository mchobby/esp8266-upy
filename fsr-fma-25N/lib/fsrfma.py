"""
  fsrfma.py is a micropython module for the 
  Honeywell FMAMSDXX025WC2C3 25N FMA force sensor. 

The MIT License (MIT)
Copyright (c) 2024 Dominique Meurisse, support@mchobby.be, shop.mchobby.be

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from micropython import const
from time import sleep_ms

FMAMSDXX025WC2C3 = const( 25 )
FMAMSDXX015WC2C3 = const( 15 )
FMAMSDXX005WC2C3 = const( 5 )

# Configuration data for the various FMA sensors
#  Max Newton, sensor_bits, Transfert_function_MIN_percent, Transfert_function_MAX_percent, 
FMA_DATA = { FMAMSDXX025WC2C3 : [25.0, 14, 0.20, 0.80],
             FMAMSDXX015WC2C3 : [15.0, 14, 0.20, 0.80],
             FMAMSDXX005WC2C3 : [5.0, 14, 0.20, 0.80] }

class FsrFmaError( Exception ):
	pass

class FsrFma():
	def __init__( self, i2c, address=0x28, model=FMAMSDXX025WC2C3 ):
		self.i2c = i2c
		self.addr = address
		self.force_range = FMA_DATA[model][0]
		self.sensor_bits = FMA_DATA[model][1]
		self.trf_func_min_pc = FMA_DATA[model][2] # Min Percent of the transfert function
		self.trf_func_max_pc = FMA_DATA[model][3] # Max Percent of the transfert function
		self.output_min = None
		self.output_max = None
		self.last_read  = None # last value must be returned when new value is not yet available from sensor
		self.offset     = 0    # Newton Measurement offset (soustracted from force reading)

		self.buf2 = bytearray( 2 )
		
		self.output_min = int( (2**self.sensor_bits)*self.trf_func_min_pc )
		self.output_max = int( (2**self.sensor_bits)*self.trf_func_max_pc )

	@property
	def force( self ):
		""" Read force in Newton """
		self.i2c.readfrom_into( self.addr, self.buf2  )
		status = (self.buf2[0] & 192)>>6
		
		if status==3:
			raise FsrFmaError( 'sensor in diagnostic mode!') # should not happen
		elif status==1:
			raise FsrFmaError( 'sensor in command mode!') # should not happen
		elif status==2:
			# stale : data not ready yet --> return last one
			return self.last_read

		# Status 0
		output = ((self.buf2[0] & 63)<<8) + self.buf2[1]
		#print( output )
		self.last_read = self.force_range*(output-self.output_min)/(self.output_max-self.output_min) 
		return self.last_read - self.offset


	def set_offset( self ):
		_offset = 0
		for i in range( 10 ):
			_offset += self.force
			sleep_ms(30)
		self.offset = _offset / 10.0


	def reset_offset( self ):
		self.offset = 0

	@property
	def weight( self ):
		""" return the weight in Kg """
		return (self.last_read-self.offset) / 9.80665
