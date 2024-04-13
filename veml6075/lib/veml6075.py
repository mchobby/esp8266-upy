""" VEML6075 : Ultraviolet (UV) Sensor with MicroPython

  Library @ https://github.com/mchobby/esp8266-upy/tree/master/veml6075

Buy VEML6075 at:
 * https://shop.mchobby.be/en/environnemental-press-temp-hum-gas/1881-gravity-veml6075-uv-sensor-i2c-3232100018815-dfrobot.html
 * https://www.dfrobot.com/product-1906.html

History:
 * 2024-01-21 Portage to MicroPython by [MCHobby](shop.mchobby.be)
 				based on https://github.com/DFRobot/DFRobot_VEML6075/tree/master

"""
__version__ = '0.1.0'

from micropython import const

VEML6075_ID_DEFAULT   = const( 0x26 )
VEML6075_ADDR         = const( 0x10 )

UVI_LOW               = 2.0
UVI_MODERATE          = 5.0
UVI_HIGH              = 7.0
UVI_VERY_HIGH         = 10.0
UVI_EXTREME           = 12.0

VEML6075_CONF         = const( 0x00 )
VEML6075_CONF_DEFAULT = const( 0x00 )
VEML6075_UVA          = const( 0x07 )
VEML6075_UVB          = const( 0x09 )
VEML6075_UV_COMP1     = const( 0x0a )
VEML6075_UV_COMP2     = const( 0x0b )
VEML6075_ID           = const( 0x0c )

POWER_ON  = const( 0 )
POWER_OFF = const( 1 )

ACTIVE_FORCE_MODE_DISABLED = const( 0 ) # Normal mode
ACTIVE_FORCE_MODE_ENABLED  = const( 1 )

TRIG_ONE_MEASUREMENT = const( 1 )  #  write to register VEML6075_REG_CONFIG_UV_TRIG to start one measurement if VEML6075_REG_CONFIG_UV_AF = 1

DYNAMIC_NORMAL = 0 # normal dynamic setting
DYNAMIC_HIGH   = 1 # high dynamic setting

# write to register VEML6075_REG_CONFIG_UV_IT to set integration time, for data process
UV_IT_50  = const(0) # < 50ms
UV_IT_100 = const(1) # < 100ms
UV_IT_200 = const(2) # < 200ms
UV_IT_400 = const(3) # < 400ms
UV_IT_800 = const(4) # < 800ms

# -- Defined in C file ---------------------------------------------------------

UVA_A_COEF   = 2.22
UVA_B_COEF   = 1.33
UVA_C_COEF   = 2.95
UVA_D_COEF   = 1.74

UV_ALPHA     = 1.0
UV_BETA      = 1.0
UV_GAMMA     = 1.0
UV_DELTA     = 1.0

UVA_RESPONSIVITY_100MS  = 0.001111
UVB_RESPONSIVITY_100MS  = 0.00125

UvaResponsivityList = [ \
	UVA_RESPONSIVITY_100MS / 0.5016286645, # 50ms
	UVA_RESPONSIVITY_100MS,                # 100ms
	UVA_RESPONSIVITY_100MS / 2.039087948,  # 200ms
	UVA_RESPONSIVITY_100MS / 3.781758958,  # 400ms
	UVA_RESPONSIVITY_100MS / 7.371335505 ] # 800ms

UvbResponsivityList = [ \
	UVB_RESPONSIVITY_100MS / 0.5016286645, # 50ms
	UVB_RESPONSIVITY_100MS,                # 100ms
	UVB_RESPONSIVITY_100MS / 2.039087948,  # 200ms
	UVB_RESPONSIVITY_100MS / 3.781758958,  # 400ms
	UVB_RESPONSIVITY_100MS / 7.371335505 ] # 800ms

def uvi_to_mwpcm2( uvi ):
	return uvi * 0.0025

class VEML6075_Config:
	# reg:UV_CONF, COMMAND CODE: 0x00_L (0x00 DATA BYTE LOW) OR 0x00_H (0x00 DATA BYTE HIGH)
	def __init__(self):
		# All register are 16bits!
		self._data = bytearray(2) # SD, UV_AF, UV_TRIG, HD, UV_IT, reserved1, reserved2
		self._data[0] = 0x00 # Configuration
		self._data[1] = 0x00 # Filling byte
		self.set_default()

	def set_default( self ):
		# Set default value for the configuration
		self.SD      = POWER_OFF
		self.UV_AF   = ACTIVE_FORCE_MODE_ENABLED
		self.UV_TRIG = TRIG_ONE_MEASUREMENT
		self.HD      = DYNAMIC_HIGH # uint8_t
		self.UV_IT   = UV_IT_400

	@property
	def SD( self ):
		""" Shutdown bit (one of POWER_xx) value """
		return self._data[0] & 0x01

	@SD.setter
	def SD( self, value ):
		self._data[0] = (self._data[0] & (0xFF ^ 0x01)) | value

	@property
	def UV_AF( self ):
		""" Active force mode (one of ACTIVE_FORCE_MODE_xxx ) """
		return ( self._data[0] & 0x02 ) >> 1

	@UV_AF.setter
	def UV_AF( self, value ):
		self._data[0] = (self._data[0] & (0xFF ^ 0x02)) | (value << 1 )

	@property
	def UV_TRIG( self ):
		""" can be set to TRIG_ONE_MEASUREMENT, will return to 0 """
		return (self._data[0] & 0x04) >> 2

	@UV_TRIG.setter
	def UV_TRIG( self, value ):
		self._data[0] = (self._data[0] & (0xFF ^ 0x04)) | (value << 2)

	@property
	def HD( self ):
		""" Normal or High dynamics. One of the DYNAMIC_xxx values """
		return ( self._data[0] & 0x08 ) >> 3

	@HD.setter
	def HD( self, value ):
		self._data[0] = (self._data[0] & ( 0xFF ^ 0x08 )) | (value << 3)

	@property
	def UV_IT( self ):
		""" Integration time, one of the UV_IT_xx """
		return (self._data[0] & 0b01110000) >> 4

	@UV_IT.setter
	def UV_IT( self, value ):
		self._data[0] = (self._data[0] & 0b10001111) | (value << 4)


	def write_to( self, i2c, addr):
		""" Write the configuration to the target VEML device """
		i2c.writeto_mem( addr, VEML6075_CONF, self._data )

	def  read_from( self, i2c, addr ):
		""" Read the configuration from the VEML target device """
		i2c.readfrom_mem_into( addr, VEML6075_CONF, self._data )

class VEML6075:
	def __init__(self, i2c, address=0x10 ):
		self.i2c    = i2c
		self.address= address
		self.buf2 = bytearray( 2 )

		tmp = self._read_u16( VEML6075_ID )
		# uint16_t   tmp = 0;
		if tmp != VEML6075_ID_DEFAULT:
			raise Exception( 'Invalid VEML6075 ID for %s' % tmp )

		self.conf = VEML6075_Config() # init to default values!
		self.conf.write_to( self.i2c, self.address ) # write config to VEML

		# Change the default settings!
		self.set_power( POWER_ON )
		self.set_active_force_mode( ACTIVE_FORCE_MODE_DISABLED )
		self.set_integration_time( UV_IT_100 )


	def _read_u16( self, reg ):
		""" Register are 16 bytes wides (LSB @ index 0, MSB @ index 1).
			Read two bytes from reg register and return an unsigned integer """
		self.i2c.readfrom_mem_into( self.address, reg, self.buf2 )
		return self.buf2[0] | ( self.buf2[1]<<8 )

	def set_power( self, value ):
		""" Set one of the POWER_xx values """
		self.conf.read_from( self.i2c, self.address )
		self.conf.SD = value
		self.conf.write_to( self.i2c, self.address )

	def get_power( self, value ):
		self.conf.read_from( self.i2c, self.address )
		return self.conf.SD

	def set_active_force_mode( self, value  ):
		""" Set one of the ACTIVE_FORCE_MODE_xxx  value """
		self.conf.read_from( self.i2c, self.address )
		self.conf.UV_AF = value
		self.conf.write_to( self.i2c, self.address )

	def get_active_force_mode( self ):
		""" Get one of the ACTIVE_FORCE_MODE_xxx  value """
		self.conf.read_from( self.i2c, self.address )
		return self.conf.UV_AF

	def set_integration_time( self, value ):
		""" Set one of the UV_IT_xx values """
		self.conf.read_from( self.i2c, self.address )
		self.conf.UV_IT = value
		self.conf.write_to( self.i2c, self.address )

	def get_integration_time( self, value ):
		self.conf.read_from( self.i2c, self.address )
		return self.conf.UV_IT

	def set_dynamic( self, value ):
		""" Set one of the DYNAMIC_xxx value  """
		self.conf.read_from( self.i2c, self.address )
		self.conf.HD = value
		self.conf.write_to( self.i2c, self.address )

	def get_dynamic( self ):
		""" Set one of the DYNAMIC_xxx value  """
		self.conf.read_from( self.i2c, self.address )
		return self.conf.HD

	def trig_one_measurement( self ):
		# If we do activate the Active_force_mode then we ask for a measyrement
		if self.conf.UV_AF == ACTIVE_FORCE_MODE_ENABLED:
			self.conf.read_from( self.i2c, self.address )
			self.conf.UV_TRIG = TRIG_ONE_MEASUREMENT
			self.conf.write_to( self.i2c, self.address )

	# main class process functions --------------------------------------------

	def read_uv_comp1_raw( self ):
		return self._read_u16( VEML6075_UV_COMP1 )

	def read_uv_comp2_raw( self ):
		return self._read_u16( VEML6075_UV_COMP2 )

	def read_uva_raw( self ):
		return self._read_u16( VEML6075_UVA )

	def read_uvb_raw( self ):
		return self._read_u16( VEML6075_UVB )

	@property
	def uva( self ):
		# return ((float) readUvaRaw() - ((UVA_A_COEF * UV_ALPHA * (float) readUvComp1Raw()) / UV_GAMMA)
		# 		- ((UVA_B_COEF * UV_ALPHA * (float) readUvComp2Raw()) / UV_DELTA));
		_r = 1.0 * self.read_uva_raw()
		_r = _r - ( ( 1.0 * UVA_A_COEF * UV_ALPHA * self.read_uv_comp1_raw() ) / UV_GAMMA )
		_r = _r - ( ( 1.0 * UVA_B_COEF * UV_ALPHA * self.read_uv_comp2_raw() ) / UV_DELTA )
		return _r

	@property
	def uvb( self ):
		# return ((float) readUvbRaw() - ((UVA_C_COEF * UV_BETA * (float) readUvComp1Raw()) / UV_GAMMA)
		#           - ((UVA_D_COEF * UV_BETA * (float) readUvComp2Raw()) / UV_DELTA));
		_r = 1.0 * self.read_uvb_raw()
		_r = _r - ( ( 1.0 * UVA_C_COEF * UV_BETA * self.read_uv_comp1_raw() ) / UV_GAMMA )
		_r = _r - ( ( 1.0 * UVA_D_COEF * UV_BETA * self.read_uv_comp2_raw() ) / UV_DELTA )
		return _r

	def uvi( self, uva_value , uvb_value  ):
		uva_value = uva_value * (1.0 / UV_ALPHA) * UvaResponsivityList[self.conf.UV_IT]
		uvb_value = uvb_value * (1.0 / UV_BETA ) * UvbResponsivityList[self.conf.UV_IT]
		return (uva_value + uvb_value) / 2.0
