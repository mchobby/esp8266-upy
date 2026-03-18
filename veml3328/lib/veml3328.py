""" veml3328.py - library for VEML3328 light color sensor under MicroPython

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2026 - domeu - creation

see source @ https://github.com/mchobby/esp8266-upy/veml3328
"""
from micropython import const
import struct

__version__ = "0.1.0"
__repo__ = "https://github.com/esp8266-upy/mchobby/esp8266-upy/veml3328"

# REGISTER CONF (00H) SETTINGS

SD1_ENABLE = const(0x0000)
SD1_DISABLE= const(0x8000)

# Digital Gain
DG_1	= const(0x0000)
DG_2	= const(0x1000)
DG_4	= const(0x2000)
DG_RES	= const(0x3000)
# Sensor GAIN
GAIN_12	= const( 0x0C00 ) # 1/2
GAIN_1  = const( 0x0000 )
GAIN_2  = const( 0x0400 )
GAIN_4  = const( 0x0800 )

SENSITIVITY_0 = const(0x00)
SENSITIVITY_1 = const(0x40)			

# Integration time
IT_50MS  = const( 0x00 )
IT_100MS = const( 0x10 )
IT_200MS = const( 0x20 )
IT_400MS = const( 0x30 )


# high_sens 0
# low_sens  1

TRIG_DISABLE = const(0x00)
TRIG_ENABLE  = const(0x04)

AF_AUTO = const(0x00)
AF_FORCE= const(0x08)

SD0_ENABLE  = const(0x00)
SD0_DISABLE = const(0x01)

# COMMAND CODES
CMD_CODE_CONF = const(0x00)
CMD_CODE_RED  = const(0x05)
CMD_CODE_GREEN= const(0x06)
CMD_CODE_BLUE = const(0x07)
CMD_CODE_CLEAR= const(0x04)
CMD_CODE_IR   = const(0x08)

LUX_RES = {"True,4,4,400": 0.003, "True,4,4,200": 0.006, "True,4,4,100": 0.012, "True,4,4,50": 0.024,
	"True,4,2,400": 0.006, "True,4,2,200": 0.012, "True,4,2,100": 0.024, "True,4,2,50": 0.048,
	"True,4,1,400": 0.012, "True,4,1,200": 0.024, "True,4,1,100": 0.048, "True,4,1,50": 0.096,
	"True,4,0.5,400": 0.024, "True,4,0.5,200": 0.048, "True,4,0.5,100": 0.096, "True,4,0.5,50": 0.192,

	"True,2,4,400": 0.006, "True,2,4,200": 0.012, "True,2,4,100": 0.024, "True,2,4,50": 0.048,
        "True,2,2,400": 0.015, "True,2,2,200": 0.024, "True,2,2,100": 0.048, "True,2,2,50": 0.096,
        "True,2,1,400": 0.024, "True,2,1,200": 0.048, "True,2,1,100": 0.096, "True,2,1,50": 0.192,
        "True,2,0.5,400": 0.048, "True,2,0.5,200": 0.096, "True,2,0.5,100": 0.192, "True,2,0.5,50": 0.384,

	"True,1,4,400": 0.012, "True,1,4,200": 0.024, "True,1,4,100": 0.048, "True,1,4,50": 0.096,
        "True,1,2,400": 0.024, "True,1,2,200": 0.048, "True,1,2,100": 0.096, "True,1,2,50": 0.192,
        "True,1,1,400": 0.048, "True,1,1,200": 0.096, "True,1,1,100": 0.192, "True,1,1,50": 0.384,
        "True,1,0.5,400": 0.096, "True,1,0.5,200": 0.192, "True,1,0.5,100": 0.384, "True,1,0.5,50": 0.768,

        "False,1,4,400": 0.036, "False,1,4,200": 0.072, "False,1,4,100": 0.144, "False,1,4,50": 0.288,
        "False,1,2,400": 0.072, "False,1,2,200": 0.144, "False,1,2,100": 0.288, "False,1,2,50": 0.576,
        "False,1,1,400": 0.144, "False,1,1,200": 0.288, "False,1,1,100": 0.576, "False,1,1,50": 1.152,
        "False,1,0.5,400": 0.288, "False,1,0.5,200": 0.576, "False,1,0.5,100": 1.152, "False,1,0.5,50": 2.304
 }

class VEML_CONFIG:
	def __init__( self ):
		self._sensitivity = 0
		self._digital_gain = 0
		self._gain = 0
		self._integration = 0
		self._lx_res = None # Lux Resolution

	def __repr__( self ):
		return "<%s sens=%s, digital_gain=%s, gain=%s, integration=%s>" % (self.__class__.__name__, self._sensitivity, self._digital_gain, self._gain, self._integration)

	@property
	def sensitivity( self ):
		return self._sensitivity
	@sensitivity.setter
	def sensitivity( self, value ): # True/False
		self._sensitivity = value 
		self._lx_res = None

	@property
	def digital_gain( self ):
		return self._digital_gain
	@digital_gain.setter
	def digital_gain( self, value ): # 1,2,4
		self._digital_gain = value
		self._lx_res = None
	
	@property
	def gain( self ):
		return self._gain
	@gain.setter
	def gain( self, value ): # 0.5, 1, 2, 4
		self._gain = value
		self._lx_res = None

	@property
	def integration( self ):
		return self._integration
	@integration.setter
	def integration( self, value ): # 50, 100, 200, 400
		self._integration = value
		self._lx_res = None
	
	@property
	def lux_res( self ):
		""" Lux Resolution """
		if self._lx_res==None:
			try:
				key = "%s,%s,%s,%s" % (self._sensitivity, self._digital_gain, self._gain, self._integration)
				self._lx_res = LUX_RES[key]
			except:
				raise ValueError( "Invalid combination %r for lux resolution" % self )
		return self._lx_res


class VEML3328:
	def __init__( self, i2c, address=0x10 ):
		self.i2c = i2c
		self.address = address
		self.buf2 = bytearray(2)
		# Store the current configuration
		# Digital Gain = 1 by default
		# Sensor Gain = 1 by default
		# Integration time = 50 ms by default
		# sensitivity =  high by default (so True)
		self.config = VEML_CONFIG() # Use default config as starting point
		self.sensitivity( high=True )
		self.digital_gain( 1 )
		self.gain( 1 ) # Sensor Gain
		self.integration( 50 ) # ms

	def __read( self, cmd ): # Uint16
		self.i2c.readfrom_mem_into( self.address, cmd, self.buf2 )
		return struct.unpack('<H',self.buf2)[0]
		
	def __set_configuration( self, value ): # unit16
		self.buf2[0]= value & 0xFF
		self.buf2[1]= (value>>8) & 0xFF
		#self.buf3[2]= 0
		self.i2c.writeto_mem( self.address, CMD_CODE_CONF, self.buf2 )

	# Configuration
	def enable( self ):
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (SD0_DISABLE ^ 0xFFFF ) # Disable SD0 & SD1 bits
		_val = _val & (SD1_DISABLE ^ 0xFFFF ) 
		self.__set_configuration( _val )

	def disabled( self ):
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (SD0_DISABLE ^ 0xFFFF ) # Disable SD0 & SD1 bits
		_val = _val & (SD1_DISABLE ^ 0xFFFF )
		_val = _val ^ SD0_DISABLE
		_val = _val ^ SD1_DISABLE
		self.__set_configuration( _val )

	def sensitivity( self, high ): # void setSensitivity(bool);
		""" Set the sensitivity to High (high=True) or Low (high=False) """
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (SENSITIVITY_1 ^ 0xFFFF) # Reset sensitivity bit

		if high==True:
			_val = _val ^ SENSITIVITY_1
		else:
			if self.config.digital_gain>1:
				raise ValueError( "Low sensitivity restrict Digital Gain to max 1. Current value %s" % self.config.digital_gain )
			_val = _val ^ SENSITIVITY_0

		self.__set_configuration( _val )
		self.config.sensitivity = high

	def gain( self, value ): # void setGain(float);
		""" Set the sensor gain between 0.5, 1, 2, 4 """
		assert value in (0.5, 1, 2, 4 ), "Invalid gain value %f" % value
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (GAIN_12 ^ 0xFFFF) # reset gain to 00
		if value==0.5:
			_val = _val ^ GAIN_12
		elif value==1:
			_val = _val ^ GAIN_1
		elif value==2:
			_val = _val ^ GAIN_2
		elif value==4:
			_val = _val ^ GAIN_4
		self.__set_configuration( _val )
		self.config.gain = value

	def digital_gain( self, value ): # void setDG(uint8_t);
		""" Set the digital gain between 1, 2, 4 """
		assert value in (1,2,4), "invalid gain value %i" % value 
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (DG_RES ^ 0xFFFF) # Reset DG to 00
		if (self.config.sensitivity==False) and (value>1):
			raise ValueError( "Low sensitivity restrict Digital Gain to max 1. Invalid setting attempt to %s" % value )

		if value==1:
			_val = _val ^ DG_1
		elif value==2:
			_val = _val ^ DG_2
		elif value==4:
			_val = _val ^ DG_4
		self.__set_configuration( _val )
		self.config.digital_gain = value

	def integration( self, ms ): # void setIntegrationTime(uint16_t);
		""" Set the integration time 50, 100, 200, 400 ms """
		assert ms in (50,100,200,400), "invalid integration time %i ms" % ms
		_val = self.__read( CMD_CODE_CONF )
		_val = _val & (IT_400MS ^ 0xFFFF)  # Reset IT to 00
		if ms==50:
			_val = _val ^ IT_50MS
		elif ms==100:
			_val = _val ^ IT_100MS
		elif ms==200:
			_val = _val ^ IT_200MS
		elif ms==400:
			_val = _val ^ IT_400MS

		self.__set_configuration( _val )
		self.config.integration = ms

	# Read the values
	@property
	def red( self ):
		return self.__read( CMD_CODE_RED )

	@property
	def green( self ):
		return self.__read( CMD_CODE_GREEN )

	@property
	def blue( self ):
		return self.__read( CMD_CODE_BLUE )

	@property
	def clear( self ):
		return self.__read( CMD_CODE_CLEAR )
	
	@property
	def ir( self ):
		return self.__read( CMD_CODE_IR )

	@property
	def lux( self ):
		return self.__read( CMD_CODE_GREEN ) * self.config.lux_res
