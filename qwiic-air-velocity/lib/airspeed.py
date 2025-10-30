"""
airspeed.py - a FS3000-1015 Air Velocity sensor - SparkFun (SEN-18768) portage to MicroPython.

based on [SparkFun former](https://www.sparkfun.com/sparkfun-air-velocity-sensor-breakout-fs3000-1015-qwiic.html)

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
    [SparkFun  Air Velocity Sensor Breakout - FS3000-1015 (Qwiic SEN-18768)](https://www.sparkfun.com/sparkfun-air-velocity-sensor-breakout-fs3000-1015-qwiic.html) @ SparkFun

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  11 august 2025 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const
import time

__version__ = '0.1.0'

AIRFLOW_RANGE_7_MPS  = const(0x00)  # FS3000-1005 has a range of 0-7.23 meters per second
AIRFLOW_RANGE_15_MPS = const(0x01)  # FS3000-1015 has a range of 0-15 meters per second

MPS_DATAPOINT_7_MPS = [0, 1.07, 2.01, 3.00, 3.97, 4.96, 5.98, 6.99, 7.23 ] # FS3000-1005 have 9 datapoints
RAW_DATAPOINT_7_MPS =  [409, 915, 1522, 2066, 2523, 2908, 3256, 3572, 3686 ] # FS3000-1005 have 9 datapoints

MPS_DATAPOINT_15_MPS = [ 0, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 13.00, 15.00 ] # FS3000-1015 have 13 datapoints
RAW_DATAPOINT_15_MPS  = [409, 1203, 1597, 1908, 2187, 2400, 2629, 2801, 3006, 3178, 3309, 3563, 3686 ]    # FS3000-1015 have 13 datapoints


class FS3000():
	"""Base class to control SparkFun SerLCD (LCD-16397) over I2C bus."""

	def __init__(self, i2c, address=0x28 ):
		"""Initialize I2C LCD at specified I2C address on the I2C Bus."""
		self.address = address
		self.i2c = i2c
		# The entire response from the FS3000 is 5 bytes.
		#   [0] Checksum
		#   [1] data high byte
		#   [2] data low byte
		#   [3] generic checksum data
		#   [4] generic checksum data
		self._buff = bytearray(5)
		self._range = AIRFLOW_RANGE_7_MPS # defaults for FS3000-1005
		self._mpsDataPoint = MPS_DATAPOINT_7_MPS # defaults to FS3000-1005 datapoints (floats)
		self._rawDataPoint = RAW_DATAPOINT_7_MPS # defaults to FS3000-1005 datapoints (integer)

	def set_range( self, airflow_range  ):
		""" Set the measurement range """
 		self._range = airflow_range
 		if self._range == AIRFLOW_RANGE_7_MPS:
			self._mpsDataPoint = MPS_DATAPOINT_7_MPS # defaults to FS3000-1005 datapoints (floats)
			self._rawDataPoint = RAW_DATAPOINT_7_MPS # defaults to FS3000-1005 datapoints (integer)
		elif self._range == AIRFLOW_RANGE_15_MPS:
			self._mpsDataPoint = MPS_DATAPOINT_15_MPS # defaults to FS3000-1005 datapoints (floats)
			self._rawDataPoint = RAW_DATAPOINT_15_MPS # defaults to FS3000-1005 datapoints (integer)
		else:
			raise ValueError( 'Invalid %s airflow_range for set_range()' % airflow_range )

	def checksum( self ):
		# Check if checksum is OK in the buffer
		sum=0 # uint8_t sum = 0;
		# Add bytes from 1 to 4
		for i in range( 4 ): # 0..3 
			sum = (sum + self._buff[i+1]) % 256

		#uint8_t calculated_cksum = (~(sum) + 1);
		#not used -> calculated_cksum = (0xFF ^ sum)+1
		crcbyte = self._buff[0]
		overall = (sum+crcbyte)%256

		return overall == 0x00

	def read_raw( self ):
		""" read raw data from sensor or None (invalid transmission)"""
		self.i2c.readfrom_into( self.address, self._buff )
		if not self.checksum(): 
			return None
		# DataFlow is 12 bits long => Masking the High Byte
		return ( (self._buff[1] & 0b00001111)<<8 ) + self._buff[2]


	def read_mps( self ):
		""" Returns float in Meter Per Second (or None) """
		airflow_raw = self.read_raw()
		if airflow_raw==None:
			return None

		data_idx = 0
		for i in range( len(self._rawDataPoint)-1 ): # 0 to 11 (for a 13 datapoints array)
			if airflow_raw > self._rawDataPoint[i]:
				data_idx = i

		# Below min or max ==> return min_mps or max_mps
		if airflow_raw <= 499:
			return 0 # Meter Per Second
		if airflow_raw >= 3686:
			return 7.0 if self._range==AIRFLOW_RANGE_7_MPS else 15.0
		# Interpolate the result
		window_size = self._rawDataPoint[data_idx+1] - self._rawDataPoint[data_idx] # Window size in Raw Value
		window_mps  = self._mpsDataPoint[data_idx+1] - self._mpsDataPoint[data_idx] # Window size in MPS
		diff  = airflow_raw - self._rawDataPoint[data_idx] # Diff from the bottom window_size
		ratio = diff / window_size # difference in percent
		return self._mpsDataPoint[data_idx] + ( window_mps * ratio )
