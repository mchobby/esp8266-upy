"""
PECMAC Driver  (I2C) for 'AC Current Monitor' (from National Control Device board).

MPL115A2 is an I2C pressure and temperature sensor.

NCD-PR29-6_10A (PECMAC) : http://shop.mchobby.be/
NCD-PR29-6_10A (PECMAC): https://store.ncd.io/product/2-channel-on-board-97-accuracy-ac-current-monitor-with-i2c-interface/
Based on the following source code
Community code sample  : https://github.com/ControlEverythingCommunity/PECMAC
Datasheet : https://media.ncd.io/sites/2/20170721135011/Current-Monitoring-Reference-Guide-12.pdf

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
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
import struct
import time
from micropython import const

PECMAC_SENSOR_TYPES = {1:'DLCT03C20', 2: 'DLCT27C10', 3: 'DLCT03CL20', 4:'OPCT16AL'}

class PECMAC():
	"""
	Class to control read I2C AC current monitor sensor board.
	"""

	def __init__( self, i2c_bus, addr=0x2A ):
		self.i2c   = i2c_bus # Initialized I2C bus
		self.addr = addr # MPL115A2 board address
		self.init()

	def init( self ):
		""" Read the identification of board """
		# Write to register 0x92(146)
		# 0x6A(106), 0x02(2), 0x00(0),0x00(0), 0x00(0) 0x00(0), 0xFE(254)
		# Header byte=106, command=2, byte 3, 4, 5 and 6 are reserved, checksum
		self.i2c.writeto_mem(self.addr, 0x92, bytes( [0x6A, 0x02, 0x00, 0x00, 0x00, 0x00, 0xFE] ) )
		time.sleep( 0.5 )

		# Read data back from 0x55, 3 bytes
		# Type of Sensor, Maximum Current, No. of Channels
		data = self.i2c.readfrom_mem(self.addr, 0x55, 3)
		self.sensor_type  = data[0]
		self.max_current  = data[1]
		self.channels     = data[2] # Nbr of channels

	def read_data( self ):
		""" Read the data for every channels, one entry per channel """
		r = []

		# Command for reading current
		# Write to register 0x92(146)
		# 0x6A(106), 0x01(1), 0x01(1),0x0C(12), 0x00(0), 0x00(0) 0x0A(10)
		# Header byte=106, command=1, start channel=1, stop channel=12, byte 5 and 6 reserved, checksum
		self.i2c.writeto_mem(self.addr, 0x92, bytes( [0x6A, 0x01, 0x01, 0x0C, 0x00, 0x00, 0x0A] ) )
		time.sleep( 0.5 )

		# Read data back from 0x55(85), No. of Channels * 3 bytes
		# current MSB1, current MSB, current LSB
		data = self.i2c.readfrom_mem( self.addr, 0x55, self.channels*3 )
		# Convert the data
		for i in range( self.channels ) :
			msb1 = data[i * 3]
			msb = data[1 + i * 3]
			lsb = data[2 + i * 3]
			# Convert the data to Amps
			r.append( (msb1 * 65536 + msb * 256 + lsb) / 1000.0 )

		return r # Return the resulting list

	def _checksum( self, register, command ):
		""" Calculate the checksum of PECMAC command. """
		# When writing command: the register is considered as part of the command (named header)
		# When reading value  : the register is not included in the calculation of the checksum
		sum = 0 if register==None else register
		for ival in command: # command is a list
			sum += ival
		return sum % 256

	def read_calibration( self, channel ):
		""" Read a channel calibration data (uint 16 bits) """
		# statut: alpha
		assert 1<= channel <= self.channels, 'Invalid channel value'

		cmd = [106, 3, channel, channel, 0, 0]
		chk = self._checksum( 0x92, cmd )
		cmd.append( chk )
		self.i2c.writeto_mem(self.addr, 0x92, bytes( cmd ) )
		time.sleep( 0.5 )

		# Read data back from 0x55(85), No. of Channels * 3 bytes
		# current MSB, current LSB, checksum
		data = self.i2c.readfrom_mem( self.addr, 0x55, 3 )
		# verify the checksum
		chk = self._checksum( None, list(data)[:-1] ) # exclude register from checksum calculation
		if chk != data[-1]:
			raise Exception( 'Invalid CRC on read')
		# Convert the data
		return data[0] * 256 + data[1]

	def write_calibration( self, channel, value ):
		""" Write a channel calibration value (uint 16 bits) """
		# statut: not implemented
		assert 1<= channel <= self.channels, 'Invalid channel value'
		raise NotImplementedError()

	@property
	def raw_values( self ):
		""" Computer friendly values. Tuple of (Ch1_Amps, Ch2_Amps, ...) """
		#p,t = self.read_compensated_data()
		return tuple( self.read_data() )

	@property
	def values( self ):
		""" Human readeable values.  Tuple of (Ch1_Amps, Ch2_Amps, ...) """
		return tuple( [ "{0:.3f}A".format(amps) for amps in self.read_data() ] )
