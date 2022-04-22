"""
pm25.py - PMS5003 serial driver (Air Quality Measurement)

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

Remarks:
  Partially based on the CircuitPython library from Adafruit
  https://github.com/adafruit/Adafruit_CircuitPython_PM25
------------------------------------------------------------------------

History:
  2 april 2022 - Dominique - initial portage from Arduino/CircuitPython
  7 april 2022 - Dominique - using particles.um03 instead of pm25.data.particles.um3
"""
__version__ = "0.0.2"
__repo__ = "https://github.com/mchobby/esp8266-upy"

import struct

class PMData:
	def __init__(self):
		self.pm10 = None # 1.0 µM
		self.pm25 = None # 2.5 µM
		self.pm100 = None# 10.0 µM

class ParticlesData:
	def __init__(self):
		self.um03 = None # 0.3 µM
		self.um05 = None
		self.um10 = None # 1.0 µM
		self.um25 = None
		self.um50 = None
		self.um100 = None # 10.0 µM

class SensorData:
	def __init__( self ):
		self.std = PMData()
		self.env = PMData()
		self.particles = ParticlesData()

RETRIES = 5
class PM25:
	def __init__( self, uart ):
		self.uart = uart
		self._buffer = bytearray(32)
		self.data = SensorData() # Decoded data

	def _read_frame( self ):
		""" Read a data frame from uart """
		# Wait for start frame 0x42 until timeout
		while True:
			ch = self.uart.read(1)
			# print( ch )
			if ch == None:
				raise RuntimeError( 'PM25: time-out before getting Start-of-Frame' )
			if ch[0] == 0x42: # Start of Frame
				break
		self._buffer[0] = 0x42
		# Read 31 remaining bytes
		for i in range( 31 ): # 0..30 --> 31 time
			ch = self.uart.read( 1 )
			# print( '2:', ch)
			if ch==None:
				raise RuntimeError( 'PM25: incomplete frame length' )
			self._buffer[i+1] = ch[0] # copy it to buffer

	def acquire( self ):
		""" read Fraùe of data & decode it """
		# attempt to acquire the data multple times from UART
		err = 0
		while True:
			try:
				self._read_frame()
				break
			except RuntimeError:
				err += 1
				if err >= RETRIES:
					raise
		# check data Header
		if not( (self._buffer[0] == 0x42) and (self._buffer[1] == 0x4d) ):
			raise RuntimeError( 'PM25 invalid header!')
		# decode data
		_d = struct.unpack( ">HHHHHHHHHHHH", self._buffer[4:28] )
		print( _d )
		self.data.std.pm10 = _d[0]
		self.data.std.pm25 = _d[1]
		self.data.std.pm100 = _d[2]
		self.data.env.pm10 = _d[3]
		self.data.env.pm25 = _d[4]
		self.data.env.pm100 = _d[5]
		self.data.particles.um03 = _d[6]
		self.data.particles.um05 = _d[7]
		self.data.particles.um10 = _d[8]
		self.data.particles.um25 = _d[9]
		self.data.particles.um50 = _d[10]
		self.data.particles.um100 = _d[11]
