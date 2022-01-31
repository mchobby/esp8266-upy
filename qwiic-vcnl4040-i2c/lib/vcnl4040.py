""" vcnl4040.py - I2C Qwiic Proximity driver (SEN-15177, SparkFun)
* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic VCNL4040   : https://www.sparkfun.com/products/15177
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
Remarks:
  More information stored onto the GitHub.
  https://github.com/sparkfun/Qwiic_Proximity_Sensor
------------------------------------------------------------------------
History:
  28 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const

__version__ = "0.0.1"

VCNL4040_ALS_IT_MASK   = const( 243 )
VCNL4040_ALS_IT_80MS   = const( 0 )
VCNL4040_ALS_IT_160MS  = const( 128 )
VCNL4040_ALS_IT_320MS  = const( 64 )
VCNL4040_ALS_IT_640MS  = const( 192 )

VCNL4040_ALS_PERS_MASK  = const( 243 )
VCNL4040_ALS_PERS_1  = const( 0 )
VCNL4040_ALS_PERS_2  = const( 4 )
VCNL4040_ALS_PERS_4  = const( 8 )
VCNL4040_ALS_PERS_8  = const( 12 )

VCNL4040_ALS_INT_EN_MASK  = const( 253 )
VCNL4040_ALS_INT_DISABLE  = const( 0 )
VCNL4040_ALS_INT_ENABLE   = const( 2 )

VCNL4040_ALS_SD_MASK      = const( 254 )
VCNL4040_ALS_SD_POWER_ON  = const( 0 )
VCNL4040_ALS_SD_POWER_OFF = const( 1 )

VCNL4040_PS_DUTY_MASK = const( 63 )
VCNL4040_PS_DUTY_40   = const( 0 )
VCNL4040_PS_DUTY_80   = const( 64 )
VCNL4040_PS_DUTY_160  = const( 128 )
VCNL4040_PS_DUTY_320  = const( 192 )

VCNL4040_PS_PERS_MASK = const( 207 )
VCNL4040_PS_PERS_1  = const( 0 )
VCNL4040_PS_PERS_2  = const( 16 )
VCNL4040_PS_PERS_3  = const( 32 )
VCNL4040_PS_PERS_4  = const( 48 )

VCNL4040_PS_IT_MASK = const( 241 )
VCNL4040_PS_IT_1T   = const( 0 )
VCNL4040_PS_IT_15T  = const( 2 )
VCNL4040_PS_IT_2T   = const( 4 )
VCNL4040_PS_IT_25T  = const( 6 )
VCNL4040_PS_IT_3T   = const( 8 )
VCNL4040_PS_IT_35T  = const( 10 )
VCNL4040_PS_IT_4T   = const( 12 )
VCNL4040_PS_IT_8T   = const( 14 )

VCNL4040_PS_SD_MASK      = const( 254 )
VCNL4040_PS_SD_POWER_ON  = const( 0 )
VCNL4040_PS_SD_POWER_OFF = const( 1 )

VCNL4040_PS_HD_MASK      = const( 247 )
VCNL4040_PS_HD_12_BIT    = const( 0 )
VCNL4040_PS_HD_16_BIT    = const( (1 << 3) )

VCNL4040_PS_INT_MASK     = const( 252 )
VCNL4040_PS_INT_DISABLE  = const( 0 )
VCNL4040_PS_INT_CLOSE    = const( 1 )
VCNL4040_PS_INT_AWAY     = const( 2 )
VCNL4040_PS_INT_BOTH     = const( 3 )

VCNL4040_PS_SMART_PERS_MASK    = const( 239 )
VCNL4040_PS_SMART_PERS_DISABLE = const( 0 )
VCNL4040_PS_SMART_PERS_ENABLE  = const( 2 )

VCNL4040_PS_AF_MASK      = const( 247 )
VCNL4040_PS_AF_DISABLE   = const( 0 )
VCNL4040_PS_AF_ENABLE    = const( 8 )
VCNL4040_PS_TRIG_MASK    = const( 247 )
VCNL4040_PS_TRIG_TRIGGER = const( 4 )

VCNL4040_WHITE_EN_MASK  = const( 127 )
VCNL4040_WHITE_ENABLE   = const( 0 )
VCNL4040_WHITE_DISABLE  = const( 128 )

VCNL4040_PS_MS_MASK     = const( 191 )
VCNL4040_PS_MS_DISABLE  = const( 0 )
VCNL4040_PS_MS_ENABLE   = const( 64 )

VCNL4040_LED_I_MASK = const( 248 )
VCNL4040_LED_50MA   = const( 0 )
VCNL4040_LED_75MA   = const( 1 )
VCNL4040_LED_100MA  = const( 2 )
VCNL4040_LED_120MA  = const( 3 )
VCNL4040_LED_140MA  = const( 4 )
VCNL4040_LED_160MA  = const( 5 )
VCNL4040_LED_180MA  = const( 6 )
VCNL4040_LED_200MA  = const( 7 )

VCNL4040_INT_FLAG_ALS_LOW   = const( 32 )
VCNL4040_INT_FLAG_ALS_HIGH  = const( 16 )
VCNL4040_INT_FLAG_CLOSE     = const( 2 )
VCNL4040_INT_FLAG_AWAY      = const( 1 )

# Used to select between upper and lower byte of command register
LOWER = True
UPPER = False

# VCNL4040 Command Codes
VCNL4040_ALS_CONF = const( 0x00 )
VCNL4040_ALS_THDH = const( 0x01 )
VCNL4040_ALS_THDL = const( 0x02 )
VCNL4040_PS_CONF1 = const( 0x03 ) # Lower
VCNL4040_PS_CONF2 = const( 0x03 ) # Upper
VCNL4040_PS_CONF3 = const( 0x04 ) # Lower
VCNL4040_PS_MS    = const( 0x04 ) # Upper
VCNL4040_PS_CANC  = const( 0x05 )
VCNL4040_PS_THDL  = const( 0x06 )
VCNL4040_PS_THDH  = const( 0x07 )
VCNL4040_PS_DATA  = const( 0x08 )
VCNL4040_ALS_DATA = const( 0x09 )
VCNL4040_WHITE_DATA = const( 0x0A )
VCNL4040_INT_FLAG = const( 0x0B ) # Upper
VCNL4040_ID       = const( 0x0C )

class VCNL4040():
	def __init__( self, i2c, address=0x60 ):
		self.address = address
		self.i2c = i2c

		self.buf1 = bytearray(1)
		self.buf2 = bytearray(2)
		if self.get_id() != 0x0186:
			raise Exception( 'Invalid sensor id!' )

		# Configure the various parts of the sensor
		self.set_led_current(200) # Max IR LED current
		self.set_ir_duty_cycle(40) # Set to highest duty cycle
		self.set_prox_integration_time(8) # Set to max integration
		self.set_prox_resolution(16) # Set to 16-bit output
		self.smart_persistance( enable=True ) # Turn on smart presistance
		self.power_proximity( enable=True ) # Turn on prox sensing
		# set_ambiant_integration_time(VCNL4040_ALS_IT_80MS); //Keep it short
		# power_ambient( enable=True ); //Turn on ambient sensing


	def read_reg16( self, reg ):
		self.i2c.readfrom_mem_into( self.address, reg, self.buf2 )
		return (self.buf2[1]<<8) + self.buf2[0]

	def write_reg16( self, reg, value ):
		self.buf2[0] = value & 0xFF # LSB
		self.buf2[1] = value >> 8   # MSB
		self.i2c.writeto_mem( self.address, reg, self.buf2 )

	def read_cmd_lower( self, cmd ):
		return self.read_reg16( cmd ) & 0xFF

	def read_cmd_upper( self, cmd ):
		return self.read_reg16( cmd ) >> 8

	def write_cmd_lower( self, cmd, value ): # write lower byte of command register (16 bits)
		reg_val = self.read_reg16( cmd ) & 0xFF00
		self.write_reg16( cmd, reg_val | value )

	def write_cmd_upper( self, cmd, value ): # write higher byte of command register (16 bits)
		reg_val = self.read_reg16( cmd ) & 0x00FF
		self.write_reg16( cmd, (value << 8) | reg_val )

	def bit_mask( self, cmd, weight, mask, value ): # uint8_t commandAddress, boolean commandHeight, uint8_t mask, uint8_t thing):
		# Given a register, read it, mask it, and then set the thing !
		# weight : is used to select between the upper or lower byte of command register
		# Example:
		#    Write dutyValue into PS_CONF1, lower byte, using the Duty_Mask
		#    bitMask(VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_DUTY_MASK, dutyValue);
		reg_val = self.read_cmd_lower( cmd ) if weight==LOWER else self.read_cmd_upper( cmd )

		# Zero-out the portions of the register we're interested in
		reg_val = reg_val & mask
		reg_val = reg_val | value

		# Change contents
		if weight==LOWER:
			self.write_cmd_lower( cmd, reg_val )
		else:
			self.write_cmd_upper( cmd, reg_val )


	def set_led_current( self, current ): # uint8_t
		# Set the IR LED sink current to one of 8 settings
		if current > 200 - 1:
			current = VCNL4040_LED_200MA
		elif current > 180 - 1:
			current = VCNL4040_LED_180MA
		elif current > 160 - 1:
			current = VCNL4040_LED_160MA
		elif current > 140 - 1:
			current = VCNL4040_LED_140MA
		elif current > 120 - 1:
			current = VCNL4040_LED_120MA
		elif current > 100 - 1:
			current = VCNL4040_LED_100MA
		elif current > 75 - 1:
			current = VCNL4040_LED_75MA
		else:
			current = VCNL4040_LED_50MA;
		self.bit_mask( VCNL4040_PS_MS, UPPER, VCNL4040_LED_I_MASK, current )

	def set_ir_duty_cycle( self, duty ): # uInt16
		# Set the duty cycle of the IR LED. The higher the duty ratio, the
		# faster the response time achieved with higher power consumption.
		# For example, PS_Duty = 1/320, peak IRED current = 100 mA, averaged
		# current consumption is 100 mA/320 = 0.3125 mA.
		if duty > 320 - 1:
			duty = VCNL4040_PS_DUTY_320
		elif duty > 160 - 1:
			duty = VCNL4040_PS_DUTY_160
		elif duty > 80 - 1:
			duty = VCNL4040_PS_DUTY_80
		else:
			duty = VCNL4040_PS_DUTY_40
		self.bit_mask(VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_DUTY_MASK, duty )

	def set_ambient_integration_time( self, value ):
		# Set ambiant light sensor integration time
		if value > 640 - 1:
			value = VCNL4040_ALS_IT_640MS
		elif value > 320 - 1:
			value = VCNL4040_ALS_IT_320MS
		elif value > 160 - 1:
			value = VCNL4040_ALS_IT_160MS
		else:
			value = VCNL4040_ALS_IT_80MS
		self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_IT_MASK, value )

	def set_prox_integration_time(self, value ): # uint8_t
		# Sets the integration time for the proximity sensor
		if value > 8 - 1:
			value = VCNL4040_PS_IT_8T
		elif value > 4 - 1:
			value = VCNL4040_PS_IT_4T
		elif value > 3 - 1:
			value = VCNL4040_PS_IT_3T
		elif value > 2 - 1:
			value = VCNL4040_PS_IT_2T
		else:
			value = VCNL4040_PS_IT_1T
		self.bit_mask( VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_IT_MASK, value);

	def set_prox_resolution( self, res ): # 12 or 16 bits
		if res > 16 - 1:
			res = VCNL4040_PS_HD_16_BIT
		else:
			res = VCNL4040_PS_HD_12_BIT
		self.bit_mask( VCNL4040_PS_CONF2, UPPER, VCNL4040_PS_HD_MASK, res )

	def set_prox_threshold( self, weight, threshold ): # UPPER or LOWER thresold setting
		if weight==UPPER:
			self.write_reg16( VCNL4040_PS_THDH, threshold )
		else:
			self.write_reg16( VCNL4040_PS_THDL, threshold )

	def set_als_threshold( self, weight, threshold ):
		# Weight = UPPER: Value that ALS must go above to trigger an interrupt
		# Weight = LOWER: Value that ALS must go below to trigger an interrupt
		if weight==UPPER:
			self.write_reg16( VCNL4040_ALS_THDH, threshold )
		else:
			self.write_reg16( VCNL4040_ALS_THDL, threshold )

	def enable_ambient_interrupts( self, enable ): # enableAmbientInterrupts
		if enable:
			self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_INT_EN_MASK, VCNL4040_ALS_INT_ENABLE )
		else:
			self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_INT_EN_MASK, VCNL4040_ALS_INT_DISABLE )

	def set_ambient_interrupt_persistance(self, value):
		# Set the Ambient interrupt persistance value
		# The ALS persistence function (ALS_PERS, 1, 2, 4, 8) helps to avoid
		# false trigger of the ALS INT. It defines the amount of
		# consecutive hits needed in order for a ALS interrupt event to be triggered.
		self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_PERS_MASK, value )

	def prox_interrupt_type( self, int_type ):
		# Enable four prox interrupt types among VCNL4040_PS_INT_DISABLE,
		#     VCNL4040_PS_INT_CLOSE, VCNL4040_PS_INT_AWAY, VCNL4040_PS_INT_BOTH
		# Will low the /int pin when triggering the interrupt.
		self.bit_mask( VCNL4040_PS_CONF2, UPPER, VCNL4040_PS_INT_MASK, int_type )

	def prox_logic_mode( self, enable ):
		# Enable the proximity detection logic output mode.
		# When this mode is selected, the INT pin is pulled low when an object is
		# close to the sensor (value is above high threshold) and is reset to
		# high when the object moves away (value is below low threshold).
		# See: set_prox_thresold() & prox_interrupt_type() to defines levels & detection kind
		if enable:
			self.bit_mask( VCNL4040_PS_MS, UPPER, VCNL4040_PS_MS_MASK, VCNL4040_PS_MS_ENABLE )
		else:
			self.bit_mask( VCNL4040_PS_MS, UPPER, VCNL4040_PS_MS_MASK, VCNL4040_PS_MS_DISABLE )


	def smart_persistance( self, enable ):
		# Enable smart persistance To accelerate the PS response time. Smart
		# persistence prevents the misjudgment of proximity sensing but also keeps a fast response time.
		if enable:
			self.bit_mask( VCNL4040_PS_CONF3, LOWER, VCNL4040_PS_SMART_PERS_MASK, VCNL4040_PS_SMART_PERS_ENABLE )
		else:
			self.bit_mask( VCNL4040_PS_CONF3, LOWER, VCNL4040_PS_SMART_PERS_MASK, VCNL4040_PS_SMART_PERS_DISABLE )

	def power_proximity( self, enable ):
		# Power on/off the prox sensing portion of the device
		if enable:
			self.bit_mask( VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_SD_MASK, VCNL4040_PS_SD_POWER_ON )
		else:
			self.bit_mask( VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_SD_MASK, VCNL4040_PS_SD_POWER_OFF )

	def power_ambient( self, enable ):
		# Power on/off the ALS sensing portion of the device
		if enable:
			self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_SD_MASK, VCNL4040_ALS_SD_POWER_ON )
		else:
			self.bit_mask( VCNL4040_ALS_CONF, LOWER, VCNL4040_ALS_SD_MASK, VCNL4040_ALS_SD_POWER_OFF )

	def enable_white_channel( self, enable ):
		if enable:
			self.bit_mask(VCNL4040_PS_MS, UPPER, VCNL4040_WHITE_EN_MASK, VCNL4040_WHITE_ENABLE )
		else:
			self.bit_mask(VCNL4040_PS_MS, UPPER, VCNL4040_WHITE_EN_MASK, VCNL4040_WHITE_DISABLE )


	def get_id( self ):
		return self.read_reg16( VCNL4040_ID )

	@property
	def proximity( self ):
		return self.read_reg16( VCNL4040_PS_DATA )

	@property
	def ambient( self ):
		return self.read_reg16( VCNL4040_ALS_DATA )

	@property
	def white( self ):
		return self.read_reg16( VCNL4040_WHITE_DATA )

	@property
	def is_dark( self ):
		# Returns true if the ALS value drops below the lower threshold
		int_flags = self.read_cmd_upper( VCNL4040_INT_FLAG )
		return int_flags & VCNL4040_INT_FLAG_ALS_LOW

	@property
	def is_light( self ):
		# Returns true if the prox value rises above the upper threshold
		int_flags = self.read_cmd_upper( VCNL4040_INT_FLAG )
		return int_flags & VCNL4040_INT_FLAG_ALS_HIGH

	@property
	def is_close( self ):
		# Returns true if the prox value rises above the upper threshold
		int_flags = self.read_cmd_upper( VCNL4040_INT_FLAG )
		return int_flags & VCNL4040_INT_FLAG_CLOSE

	@property
	def is_away( self ):
		# Returns true if the prox value drops below the lower threshold
		int_flags = self.read_cmd_upper( VCNL4040_INT_FLAG )
		return int_flags & VCNL4040_INT_FLAG_AWAY
