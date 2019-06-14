"""
MLX90614 is a micropython module for the Melexis MLX90614 Non-Contact IR Thermometer.

The MLX90614 is also used on the Olimex MOD-IR-TEMP UEXT board.

It allows the user to control one or more MOD-LCD1x9 board.
MOD-IR-TEMP :
MOD-IR-TEMP : https://www.olimex.com/Products/Modules/Sensors/MOD-IR-TEMP/open-source-hardware
Datasheet  : https://www.olimex.com/Products/Modules/Sensors/MOD-IR-TEMP/resources/MLX90614_rev001.pdf

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

#import ustruct
#from machine import Pin
from time import sleep
import ubinascii

# RAM
MLX90614_RAWIR1 = 0x04
MLX90614_RAWIR2 = 0x05
MLX90614_TA    = 0x06
MLX90614_TOBJ1 = 0x07
MLX90614_TOBJ2 = 0x08
# EEPROM
MLX90614_TOMAX = 0x20
MLX90614_TOMIN = 0x21
MLX90614_PWMCTRL = 0x22
MLX90614_TARANGE = 0x23
MLX90614_EMISS = 0x24
MLX90614_CONFIG = 0x25
MLX90614_ADDR = 0x0E
MLX90614_ID1 = 0x3C
MLX90614_ID2 = 0x3D
MLX90614_ID3 = 0x3E
MLX90614_ID4 = 0x3F

class MLX90614():
	""" Class to control the MLX90614 non contact IR thermometer. """
	def __init__( self, i2c_bus, addr=0x5A ):
		self.i2c    = i2c_bus # Initialized I2C bus
		self.addr = addr # MOD-LCD1x9 board address

		if not self._initialize():
			raise Exception( 'init failure')

	def _initialize( self ):
		""" Equivalent of begin() under Arduino """
		# Should be able to read the ID Numbers from the Melexis
		self.readID()
		return True

	def readID( self ):
		""" Read the Melexis 4 Bytes indentification """
		data = self.i2c.readfrom_mem( self.addr, MLX90614_ID1, 4 )
		# self.i2c.writeto( self.addr, bytes([MLX90614_ID1]) )
		# data = self.i2c.readfrom( self.addr, 4) # Read 4 bytes
		return ubinascii.hexlify( data ).decode() # made it a string

	def read_temp( self, reg ):
		""" Read the temperature from sensor register MLX90614_TA or MLX90614_TOBJ1.
		    Returns a tuple with calcultated temperature and PEC """

		data = self.i2c.readfrom_mem( self.addr, reg, 3 )
		# self.i2c.writeto( self.addr, bytes([reg]) )
		# sleep( 0.150 )
		# data = self.i2c.readfrom( self.addr, 3) # Read 3 bytes

		temp_data = data[0] + (data[1]<<8)
		pec       = data[2]

		return ( (temp_data*0.02)-273.15 , pec )

	def readObjectTempC( self ):
		""" Return temperature of object Celcius degree & PEC """
		return self.read_temp( MLX90614_TOBJ1 )

	def readAmbientTempC( self ):
		""" Return ambiant temperature & PEC """
		return self.read_temp( MLX90614_TA )

	@property
	def raw_values( self ):
		""" Return Ambiant temperature and object temperature """
		return ( self.readAmbientTempC()[0] , self.readObjectTempC()[0] ) # Ignoring PEC results

	@property
	def values( self ):
		""" Return the Ambiant & Object temperature as user friendly strings """
		AmbiantTemp,ObjectTemp = self.raw_values
		return ( "{0:.3f} C".format(AmbiantTemp), "{0:.3f} C".format(ObjectTemp) )
