"""
Test the SI70x (I2C) sensor board from National Control Device.

SI7005 is an I2C relative humidity and temperature sensor.

NCD-SI7005 : http://shop.mchobby.be/
NCD-SI7005 : https://store.ncd.io/product/si7005-humidity-and-temperature-sensor-%c2%b14-5rh-%c2%b10-5c-i2c-mini-module/
Community code sample  : https://github.com/ControlEverythingCommunity/SI7005
Datasheet : https://media.ncd.io/sites/2/20170721134449/Si7005.pdf

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
import ustruct
import time
import binascii

# Registers
DATA_REG   = 0x00
CONFIG_REG = 0x03

class SI7005():
	"""
	Class to control the SI7005 sensor.
	"""

	def __init__( self, i2c_bus, addr=0x40 ):
		self.i2c   = i2c_bus # Initialized I2C bus
		self.addr = addr # MPL115A2 board address
		self.data = bytes( 3 ) # Buffer of 3 bytes
		self.init()

	def init( self ):
		pass

	def read_data( self ):
		""" Read 3 bytes from the sensor """
		#self.data = self.i2c.readfrom_mem( self.addr, DATA_REG, 3 )
		self.i2c.writeto( self.addr, bytes([0x00]) )
		self.data = self.i2c.readfrom( self.addr, 3)
		# print( binascii.hexlify(self.data) )

	def is_data_ready( self ):
		""" check if the readed data contains the DATA_READY flag """
		return (self.data[0] & 0x01) == 0

	def read_temp( self ):
		""" Reads the temperature_celcius from the sensor """
		# Configure the SI7005
		# 0x11 = Temperature, Fast mode enable, Heater Off
		# self.i2c.writeto_mem( self.addr, CONFIG_REG, bytes(0x11) )
		self.i2c.writeto( self.addr, bytes([CONFIG_REG, 0x11]) )
		time.sleep(0.5)
		self.read_data()
		while not self.is_data_ready():
			time.sleep(0.200)
			self.read_data()
		# Convert the data on 14 bits
		return ((self.data[1] * 256 + self.data[2]) / 4.0) / 32.0 - 50.0

	def read_hrel( self ):
		""" Reads the relative_humidity_in_percent from the sensor """
		# Configure the SI7005
		# 0x01 = Relative Humidity, Fast mode enable, Heater Off
		# self.i2c.writeto_mem( self.addr, CONFIG_REG, bytes(0x01) )
		self.i2c.writeto( self.addr, bytes([CONFIG_REG, 0x01]) )
		time.sleep( 0.5 ) # 500ms
		self.read_data()
		while not self.is_data_ready():
			time.sleep(0.200)
			self.read_data()
		# Convert the data to 12-bits
		return ((self.data[1] * 256 + self.data[2]) / 16.0) / 16.0 - 24.0

	@property
	def raw_values( self ):
		""" Computer friendly values. Tuple of (rel_hum_%, temperature_Celcius) """
		return ( self.read_hrel(), self.read_temp() )

	@property
	def values( self ):
		""" Human readeable values.  Tuple of (rel_hum_%, temp_celcius)"""
		hrel,temp = self.raw_values
		return ( "{0:.2f} %HRel".format(hrel), "{} C".format(temp) )
