"""
Test the MPL115A2 (I2C) sensor board from National Control Device.

MPL115A2 is an I2C pressure and temperature sensor.

NCD-MPL115A2 : http://shop.mchobby.be/
NCD-MPL115A2 : https://store.ncd.io/product/mpl115a2-digital-barometer-50-to-115-kpa-i2c-mini-module/
MPL115A2-BRK : https://shop.mchobby.be/fr/nouveaute/1587-mpl115a2-is-an-i2c-pressure-and-temperature-sensor-3232100015876.html
Based on the following source code
Community code sample  : https://github.com/ControlEverythingCommunity/MPL115A2
CircuitPython for MPL115A2 : https://github.com/adafruit/Adafruit_CircuitPython_MPL115A2
Datasheet : https://media.ncd.io/sites/2/20170721134618/MPL115A2.pdf

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

# Registers
REGISTER_PRESSURE_MSB     = const(0x00)
REGISTER_A0_COEFF_MSB     = const(0x04)
REGISTER_STARTCONVERSION  = const(0x12)


class MPL115A2():
	"""
	Class to control the MPL115A2 sensor.
	"""

	def __init__( self, i2c_bus, addr=0x60 ):
		self.i2c   = i2c_bus # Initialized I2C bus
		self.addr = addr # MPL115A2 board address
		self.init()

	def init( self ):
		# Reading Coefficents for compensation
		#data = self.i2c.readfrom_mem( self.addr, REGISTER_A0_COEFF_MSB, 8)
		buf = bytearray(8)
		self.i2c.writeto(self.addr, bytes( [REGISTER_A0_COEFF_MSB] ) )
		self.i2c.readfrom_into(self.addr, buf)
		a0, b1, b2, c12 = struct.unpack(">hhhh", buf)
		c12 >>= 2
		# see datasheet pg. 9, do math
		self._a0 = a0 / 8
		self._b1 = b1 / 8192
		self._b2 = b2 / 16384
		self._c12 = c12 / 4194304
		#print( self._a0, self._b1, self._b2, self._c12 )

	def read_compensated_data( self ):
		""" Reads the data from the sensors and returns the compensated data.
			(pressure_in_kPa, temperature_Celcius) """
		# Send Pressure measurement command, 0x12
		# New version --------------------------------------------------------
		self.i2c.writeto( self.addr, bytes([REGISTER_STARTCONVERSION,0x00]) )
		time.sleep( 0.005 ) # 5ms in arduino code, 500ms
		# Read data back from 0x00(00), 4 bytes
		# pres MSB, pres LSB, temp MSB, temp LSB
		data = bytearray(4)
		self.i2c.writeto(self.addr, bytes([REGISTER_PRESSURE_MSB]) )
		self.i2c.readfrom_into( self.addr, data )

		pressure, temp = struct.unpack(">HH", data)
		pressure >>= 6
		temp     >>= 6

		# see datasheet pg. 6, eqn. 1, result in counts
		pressure = self._a0 + (self._b1 + self._c12 * temp) * pressure + self._b2 * temp
		# see datasheet pg. 6, eqn. 2, result in kPa
		pressure = (65/1023) * pressure + 50
		# stolen from arduino driver, result in deg C
		temp = (temp - 498) / -5.35 + 25
		return pressure, temp

	@property
	def raw_values( self ):
		""" Computer friendly values. Tuple of (pressure_hPa, temperature_Celcius) """
		p,t = self.read_compensated_data()
		return (p*10,t)

	@property
	def values( self ):
		""" Human readeable values.  Tuple of (pressure_hPa, temp_celcius)"""
		p,t = self.read_compensated_data()
		return ( "{0:.2f}hPa".format(p*10), "{}C".format(t) )
