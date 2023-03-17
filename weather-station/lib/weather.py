# Weather Station  MicroPython Driver - for Serial Weather Station SEN0186
#
# mar 16, 2023, Domeu, initial writing
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__version__ = '0.0.1'

import time

MAX_ERROR_COUNT = 100 # Number of continuous errors detected before raising exception. 0 for ignore

class WeatherStation(object):
	""" Abstraction for Weather Station Serial transmission """
	def __init__( self, uart ):
		self._uart = uart
		self._buffer = None
		self._buf2 = None
		self.error_count = 0

	def is_valid_buf( self, buf ):
		if len(self._buf2)<80: # Must have professonnal Protocol
			return False
		if not( (self._buf2[0]==ord('A')) and (self._buf2[5]==ord('B')) and (self._buf2[9]==ord('C')) ):
			return False
		if not( (self._buf2[14]==ord('D')) and (self._buf2[19]==ord('E')) and (self._buf2[24]==ord('F')) ):
			return False
		if not( (self._buf2[29]==ord('G')) and (self._buf2[34]==ord('H')) and (self._buf2[39]==ord('I')) ):
			return False
		if not( (self._buf2[44]==ord('J')) and (self._buf2[49]==ord('K')) and (self._buf2[54]==ord('L')) ):
			return False
		if not( (self._buf2[59]==ord('M')) and (self._buf2[63]==ord('N')) and (self._buf2[69]==ord('O')) ):
			return False
		return True

	def update( self, retries=10 ):
		""" Update internal buffer with data coming from UART.
		    Return True if a new valid buffer is received. """
		_count = 0 # Local retries counter
		while _count < retries:
			self._buf2 = self._uart.readline()
			if (self._buf2 != None) and self.is_valid_buf(self._buf2):
				self._buffer = self._buf2 # Swap buffers
				self._buf2 = None
				self.error_count = 0
				return True

			self.error_count += 1
			if (MAX_ERROR_COUNT > 0) and (self.error_count >= MAX_ERROR_COUNT):
				raise Exception( 'Max continuous error reached on reads. Professional protocol not detected' )

			_count += 1
			time.sleep_ms( 100 )
		return False # Nothing valid received

	@property
	def wind_dir( self ):
		""" Wind Direction 0 to 33"""
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[6:9]) # B field

	@property
	def wind_speed_real( self ):
		""" Wind Speed Instantaneous m/s """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[15:19])/10 # D

	@property
	def wind_speed( self ):
		""" Wind Speed m/s (mean on the last minute) """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[20:24])/10 # E

	@property
	def wind_speed_max( self ):
		""" Wind Speed m/s (max on the last 5 minutes) """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[25:29])/10 # F

	@property
	def rain_cycle_real( self ):
		""" Rain bucket cycles (0-9999) """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[30:34]) # G

	@property
	def rain_cycle( self ):
		""" Mean Rain bucket cycles (0-9999) over the last minute"""
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[35:39]) # H

	@property
	def rain_mm( self ):
		""" Rain in mm the last minute """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[40:44])/10 # I

	@property
	def rain_mm_hour( self ):
		""" Rain in mm the last hour """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[45:49])/10 # J

	@property
	def rain_mm_day( self ):
		""" Rain in mm the last 24 hour """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[50:53])/10 # K

	@property
	def temp( self ):
		""" temperature """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[55:59])/10 # L

	@property
	def hrel( self ):
		""" Relative humidity (percent) """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[60:63])/10 # M

	@property
	def pressure( self ):
		""" Atmospheric pressure (hPa) """
		if not self._buffer:
			return -1
		else:
			return int(self._buffer[64:69])/10 # N
