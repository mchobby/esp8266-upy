
"""
bmm150.py : MicroPython driver for the BMM150 3 axis magnetic sensor.


* Author(s):
   23 may 2021: Meurisse D. (shop.mchobby.be) - porting from Arduino code from
                https://github.com/Seeed-Studio/Grove_3_Axis_Compass_V2.0_BMM150

"""

# imports
from micropython import const
from collections import namedtuple
from time import sleep_ms

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/bmm150"

BMM150_OK = const(0)

# API error codes
BMM150_E_ID_NOT_CONFORM = const(-1)
BMM150_E_INVALID_CONFIG = const(-2)

# API warning codes
BMM150_W_NORMAL_SELF_TEST_YZ_FAIL	= const(1)
BMM150_W_NORMAL_SELF_TEST_XZ_FAIL	= const(2)
BMM150_W_NORMAL_SELF_TEST_Z_FAIL	= const(3)
BMM150_W_NORMAL_SELF_TEST_XY_FAIL	= const(4)
BMM150_W_NORMAL_SELF_TEST_Y_FAIL	= const(5)
BMM150_W_NORMAL_SELF_TEST_X_FAIL	= const(6)
BMM150_W_NORMAL_SELF_TEST_XYZ_FAIL  = const(7)
BMM150_W_ADV_SELF_TEST_FAIL	        = const(8)

# name CHIP ID & SOFT RESET VALUES
BMM150_CHIP_ID              = const(0x32)
BMM150_SET_SOFT_RESET		= const(0x82)

# POWER MODE DEFINTIONS
BMM150_NORMAL_MODE		= const(0x00)
BMM150_FORCED_MODE		= const(0x01)
BMM150_SLEEP_MODE		= const(0x03)
BMM150_SUSPEND_MODE		= const(0x04)

# PRESET MODE DEFINITIONS
BMM150_PRESETMODE_LOWPOWER      = const(0x01)
BMM150_PRESETMODE_REGULAR       = const(0x02)
BMM150_PRESETMODE_HIGHACCURACY  = const(0x03)
BMM150_PRESETMODE_ENHANCED      = const(0x04)

# Power mode settings
BMM150_POWER_CNTRL_DISABLE	= const(0x00)
BMM150_POWER_CNTRL_ENABLE	= const(0x01)

# Sensor delay time settings
BMM150_SOFT_RESET_DELAY		  = const(1)
BMM150_NORMAL_SELF_TEST_DELAY = const(2)
BMM150_START_UP_TIME		  = const(3)
BMM150_ADV_SELF_TEST_DELAY	  = const(4)

# ENABLE/DISABLE DEFINITIONS
BMM150_XY_CHANNEL_ENABLE	= const(0x00)
BMM150_XY_CHANNEL_DISABLE	= const(0x03)

# Register Address
BMM150_CHIP_ID_ADDR		    = const(0x40)
BMM150_DATA_X_LSB		    = const(0x42)
BMM150_DATA_X_MSB		    = const(0x43)
BMM150_DATA_Y_LSB		    = const(0x44)
BMM150_DATA_Y_MSB		    = const(0x45)
BMM150_DATA_Z_LSB		    = const(0x46)
BMM150_DATA_Z_MSB		    = const(0x47)
BMM150_DATA_READY_STATUS	= const(0x48)
BMM150_INTERRUPT_STATUS		= const(0x4A)
BMM150_POWER_CONTROL_ADDR	= const(0x4B)
BMM150_OP_MODE_ADDR		    = const(0x4C)
BMM150_INT_CONFIG_ADDR		= const(0x4D)
BMM150_AXES_ENABLE_ADDR		= const(0x4E)
BMM150_LOW_THRESHOLD_ADDR	= const(0x4F)
BMM150_HIGH_THRESHOLD_ADDR	= const(0x50)
BMM150_REP_XY_ADDR		    = const(0x51)
BMM150_REP_Z_ADDR		    = const(0x52)

# DATA RATE DEFINITIONS
BMM150_DATA_RATE_10HZ  = const(0x00)
BMM150_DATA_RATE_02HZ  = const(0x01)
BMM150_DATA_RATE_06HZ  = const(0x02)
BMM150_DATA_RATE_08HZ  = const(0x03)
BMM150_DATA_RATE_15HZ  = const(0x04)
BMM150_DATA_RATE_20HZ  = const(0x05)
BMM150_DATA_RATE_25HZ  = const(0x06)
BMM150_DATA_RATE_30HZ  = const(0x07)

# TRIM REGISTERS
BMM150_DIG_X1       = const(0x5D)
BMM150_DIG_Y1       = const(0x5E)
BMM150_DIG_Z4_LSB   = const(0x62)
BMM150_DIG_Z4_MSB   = const(0x63)
BMM150_DIG_X2       = const(0x64)
BMM150_DIG_Y2       = const(0x65)
BMM150_DIG_Z2_LSB   = const(0x68)
BMM150_DIG_Z2_MSB   = const(0x69)
BMM150_DIG_Z1_LSB   = const(0x6A)
BMM150_DIG_Z1_MSB   = const(0x6B)
BMM150_DIG_XYZ1_LSB = const(0x6C)
BMM150_DIG_XYZ1_MSB = const(0x6D)
BMM150_DIG_Z3_LSB   = const(0x6E)
BMM150_DIG_Z3_MSB   = const(0x6F)
BMM150_DIG_XY2      = const(0x70)
BMM150_DIG_XY1      = const(0x71)

# PRESET MODES - REPETITIONS-XY RATES
BMM150_LOWPOWER_REPXY     = const(1)
BMM150_REGULAR_REPXY      = const(4)
BMM150_ENHANCED_REPXY     = const(7)
BMM150_HIGHACCURACY_REPXY = const(23)

# PRESET MODES - REPETITIONS-Z RATES
BMM150_LOWPOWER_REPZ     = const(2)
BMM150_REGULAR_REPZ      = const(14)
BMM150_ENHANCED_REPZ     = const(26)
BMM150_HIGHACCURACY_REPZ = const(82)

# Macros for bit masking
# (MSK, None) --> Mask only
BMM150_PWR_CNTRL = (0x01, None)

# (MSK, POS)
BMM150_CONTROL_MEASURE	= ( 0x38, 0x03)
BMM150_POWER_CONTROL_BIT= (0x01, 0x00)
BMM150_OP_MODE			= (0x06, 0x01)
BMM150_ODR				= (0x38, 0x03)
BMM150_DATA_X			= (0xF8, 0x03)
BMM150_DATA_Y			= (0xF8, 0x03)
BMM150_DATA_Z			= (0xFE, 0x01)
BMM150_DATA_RHALL		= (0xFC, 0x02)
BMM150_ADV_SELF_TEST 	= (0xC0, 0x06)
BMM150_DRDY_EN		 	= (0x80, 0x07)
BMM150_INT_PIN_EN	 	= (0x40, 0x06)
BMM150_DRDY_POLARITY 	= (0x04, 0x02)
BMM150_INT_LATCH	 	= (0x02, 0x01)
BMM150_DATA_OVERRUN_INT	  = (0x80, 0x07)
BMM150_OVERFLOW_INT       = (0x40, 0x06)
BMM150_HIGH_THRESHOLD_INT = (0x38, 0x03)

BMM150_SELF_TEST          = (0x01, None)
BMM150_INT_POLARITY       = (0x01, None)
BMM150_LOW_THRESHOLD_INT  = (0x07, None)
BMM150_DRDY_STATUS        = (0x01, None)

# OVERFLOW DEFINITIONS
BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL	= const(-4096)
BMM150_ZAXIS_HALL_OVERFLOW_ADCVAL	= const(-16384)
BMM150_OVERFLOW_OUTPUT			    = const(-32768)
BMM150_NEGATIVE_SATURATION_Z        = const(-32767)
BMM150_POSITIVE_SATURATION_Z        = const(32767)
# BMM150_OVERFLOW_OUTPUT_FLOAT		0.0f

# Register read lengths
BMM150_SELF_TEST_LEN	= const(5)
BMM150_SETTING_DATA_LEN	= const(8)
BMM150_XYZR_DATA_LEN	= const(8)

# Self test selection macros
# BMM150_NORMAL_SELF_TEST   = const(0)
# BMM150_ADVANCED_SELF_TEST = const(1)

# Self test settings
# BMM150_DISABLE_XY_AXIS = const(0x03)
# BMM150_SELF_TEST_REP_Z = const(0x04)

# Advanced self-test current settings
# BMM150_DISABLE_SELF_TEST_CURRENT = const(0x00)
# BMM150_ENABLE_NEGATIVE_CURRENT   = const(0x02)
# BMM150_ENABLE_POSITIVE_CURRENT   = const(0x03)

# Normal self-test status
# BMM150_SELF_TEST_STATUS_XYZ_FAIL = const(0x00)
# BMM150_SELF_TEST_STATUS_SUCCESS  = const(0x07)

class BMM150_Mag_Data(object):
	__slot__ = [ "x", "y", "z" ]
	def __init__( self ):
		self.x=0; self.y=0; self.z=0

# bmm150 un-compensated (raw) magnetometer data
# Raw Mag X,Y,Z data & Raw Mag resistance value
class BMM150_Raw_Mag_Data(object):
	__slot__ = [ "raw_datax", "raw_datay","raw_dataz","raw_data_r" ]
	def __init__(self):
		self.raw_datax=0; self.raw_datay=0; self.raw_dataz=0
		self.raw_data_r=0

# bmm150 trim data structure
# trim int8: x1,y1,x2,y2, uint16: z1, int16: z2,z3,z4, uint8: xy1,xy2, uint16: xyz1 data
class BMM150_Trim_Registers(object):
	__slot__ = [ "dig_x1","dig_y1","dig_x2","dig_y2","dig_z1","dig_z2","dig_z3","dig_z4","dig_xy1","dig_xy2","dig_xyz1" ]
	def __init__(self):
		self.dig_x1=0; self.dig_y1=0; self.dig_x2=0; self.dig_y2=0
		self.dig_z1=0; self.dig_z2=0; self.dig_z3=0; self.dig_z4=0
		self.dig_xy1=0; self.dig_xy2=0; self.dig_xyz1=0

# bmm150 sensor settings
#	uint8: xyz_axes_control - Control measurement of XYZ axes *
#	uint8: pwr_cntrl_bit - Power control bit value
#	uint8: pwr_mode      - Power control bit value
#	uint8: data_rate     - Output Data rate value (ODR)
#	uint8: xy_rep        - XY Repetitions
#	uint8: z_rep         - Z Repetitions
#	uint8: preset_mode   - Preset mode of sensor
class BMM150_Settings(object):
	__slot__ = [ "xyz_axes_control","pwr_cntrl_bit","pwr_mode","data_rate","xy_rep","z_rep preset_mode" ]
	def __init__(self):
		self.xyz_axes_control=0; self.pwr_cntrl_bit=0; self.pwr_mode=0
		self.data_rate=0; self.xy_rep=0; self.z_rep=0; preset_mode=0

class BMM150_Error( Exception ):
	pass

def bitwise_not( value, bit_size=8 ):
	if bit_size==8:
		r = 255
	elif bit_size==16:
		r = 65535
	else:
		raise Exception( "invalid bit_size")
	return r ^ value

def set_bits( reg_data, bitname, data ):
	return ((reg_data & bitwise_not(bitname[0])) | ((data<<bitname[1]) & bitname[0] ))

def get_bits( reg_data, bitname ):
	return ((reg_data & bitname[0]) >> bitname[1])

def set_bits_pos0( reg_data, bitname, data ):
	return ((reg_data & bitwise_not(bitname[0])) | (data & bitname[0]) )

class BMM150:
	""" The BMM150 class support the main function for driving the BMM150 sensor

		:param i2c: the connected i2c bus machine.I2C
		:param address: the device address; defaults to 0x13 """


	def __init__(self, i2c, address=0x13):
		self.i2c = i2c
		self.addr = address
		self.buf1 = bytearray( 1 ) # various read buffer
		self.buf2 = bytearray(2)
		self.buf4 = bytearray(4)
		self.buf10 = bytearray(10)
		self.buf8  = bytearray( BMM150_XYZR_DATA_LEN )
		self.settings = BMM150_Settings()
		self.raw_mag_data = BMM150_Raw_Mag_Data()
		self.mag_data = BMM150_Mag_Data()
		self.trim_data = BMM150_Trim_Registers()
		self._init()

	def _init( self ):
		""" Initialize sensor """
		# Power up the sensor from suspend to sleep mode
		self.set_op_mode( BMM150_SLEEP_MODE )
		sleep_ms( BMM150_START_UP_TIME )

		# Check chip ID
		#id = self.i2c_read( BMM150_CHIP_ID_ADDR )
		self.i2c.readfrom_mem_into( self.addr, BMM150_CHIP_ID_ADDR, self.buf1 )
		if self.buf1[0] != BMM150_CHIP_ID :
			raise BMM150_Error( "id %i not conform" % self.buf1[0] )
		# Read Trim register
		self.read_trim_registers()
		# Setting the power mode as normal */
		self.set_op_mode( BMM150_NORMAL_MODE )
		# Setting the preset mode as Low power mode
		# i.e. data rate = 10Hz XY-rep = 1 Z-rep = 2
		self.set_presetmode( BMM150_PRESETMODE_LOWPOWER )
		# self.set_presetmode( BMM150_HIGHACCURACY_REPZ )
		return BMM150_OK

	# void BMM150::i2c_read(short address, uint8_t* buffer, short length) {

	def read_mag_data( self ):
		""" Read magnetometer data """
		#int16_t msb_data;
		#int8_t reg_data[BMM150_XYZR_DATA_LEN] = {0};

		#i2c_read(BMM150_DATA_X_LSB, reg_data, BMM150_XYZR_DATA_LEN);
		self.i2c.readfrom_mem_into( self.addr, BMM150_DATA_X_LSB, self.buf8 )

		# Mag X axis data
		self.buf8[0] = get_bits( self.buf8[0], BMM150_DATA_X )
		# Shift the MSB data to left by 5 bits. Multiply by 32 to get the shift left by 5 value
		msb_data = self.buf8[1] * 32 # ((int16_t)((int8_t)reg_data[1])) * 32;
		# Raw mag X axis data
		self.raw_mag_data.raw_datax = msb_data | self.buf8[0] # (int16_t)(msb_data | reg_data[0]);
		# Mag Y axis data
		self.buf8[2] = get_bits( self.buf8[2], BMM150_DATA_Y )
		# Shift the MSB data to left by 5 bits. Multiply by 32 to get the shift left by 5 value
		msb_data = self.buf8[3] * 32 # ((int16_t)((int8_t)reg_data[3])) * 32;
		# Raw mag Y axis data
		self.raw_mag_data.raw_datay = msb_data | self.buf8[2] # (int16_t)(msb_data | reg_data[2]);
		# Mag Z axis data
		self.buf8[4] = get_bits(self.buf8[4], BMM150_DATA_Z)
		# Shift the MSB data to left by 7 bits. Multiply by 128 to get the shift left by 7 value
		msb_data = self.buf8[5] * 128 # ((int16_t)((int8_t)reg_data[5])) * 128;
		# Raw mag Z axis data
		self.raw_mag_data.raw_dataz = msb_data | self.buf8[4] # (int16_t)(msb_data | reg_data[4]);
		# Mag R-HALL data
		self.buf8[6] = get_bits(self.buf8[6], BMM150_DATA_RHALL)
		self.raw_mag_data.raw_data_r = (self.buf8[7] << 6) | self.buf8[6] #(uint16_t)(((uint16_t)reg_data[7] << 6) | reg_data[6]);

		# Compensated Mag X data in int16_t format
		self.mag_data.x = self.compensate_x( self.raw_mag_data.raw_datax, self.raw_mag_data.raw_data_r )
		# Compensated Mag Y data in int16_t format
		self.mag_data.y = self.compensate_y( self.raw_mag_data.raw_datay, self.raw_mag_data.raw_data_r )
		# Compensated Mag Z data in int16_t format
		self.mag_data.z = self.compensate_z( self.raw_mag_data.raw_dataz, self.raw_mag_data.raw_data_r )

	def compensate_x( self, mag_data_x, data_rhall ):
		""" obtain the compensated magnetometer x axis data(micro-tesla) in float """
		retval = 0
		process_comp_x0 = 0 # uint16_t

		# Overflow condition check
		if mag_data_x == BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL:
			return BMM150_OVERFLOW_OUTPUT # overflow condition

		if data_rhall != 0: # Availability of valid data
			process_comp_x0 = data_rhall
		elif self.trim_data.dig_xyz1 != 0:
			process_comp_x0 = self.trim_data.dig_xyz1
		else:
			process_comp_x0 = 0

		if process_comp_x0 != 0 :
			# Processing compensation equations
			process_comp_x1 = self.trim_data.dig_xyz1 * 16384
			process_comp_x2 = int(process_comp_x1 / process_comp_x0) - 0x4000
			retval = process_comp_x2
			process_comp_x3 = retval * retval
			process_comp_x4 = self.trim_data.dig_xy2 * int(process_comp_x3 / 128)
			process_comp_x5 = self.trim_data.dig_xy1 * 128
			process_comp_x6 = retval * process_comp_x5
			process_comp_x7 = int((process_comp_x4 + process_comp_x6) / 512) + 0x100000
			process_comp_x8 = self.trim_data.dig_x2 + 0xA0
			process_comp_x9 = (process_comp_x7 * process_comp_x8) / 4096
			process_comp_x10 = mag_data_x * int(process_comp_x9)
			retval = int(process_comp_x10 / 8192)
			retval = (retval + (self.trim_data.dig_x1 * 8)) / 16
			return int(retval)

		return BMM150_OVERFLOW_OUTPUT

	def compensate_y( self, mag_data_y, data_rhall ):
		""" obtain the compensated magnetometer Y axis data(micro-tesla) in int16_t. """
		retval = 0
		process_comp_y0 = 0

		if mag_data_y == BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL :
			return BMM150_OVERFLOW_OUTPUT # Overflow condition check

		if data_rhall != 0:
			process_comp_y0 = data_rhall # Availability of valid data
		elif self.trim_data.dig_xyz1 != 0:
			process_comp_y0 = self.trim_data.dig_xyz1;
		else:
			process_comp_y0 = 0

		if process_comp_y0 == 0:
			return BMM150_OVERFLOW_OUTPUT

		# Processing compensation equations
		process_comp_y1 = (self.trim_data.dig_xyz1 * 16384) / process_comp_y0
		process_comp_y2 = int(process_comp_y1) - 0x4000
		retval = process_comp_y2
		process_comp_y3 = retval * retval
		process_comp_y4 = self.trim_data.dig_xy2 * int(process_comp_y3 / 128)
		process_comp_y5 = self.trim_data.dig_xy1 * 128
		process_comp_y6 = int( (process_comp_y4 + (retval * process_comp_y5)) / 512 )
		process_comp_y7 = self.trim_data.dig_y2 + 0xA0
		process_comp_y8 = int( ((process_comp_y6 + 0x100000) * process_comp_y7) / 4096 )
		process_comp_y9 = mag_data_y * process_comp_y8
		retval = int( process_comp_y9 / 8192 )
		retval = (retval + (self.trim_data.dig_y1 * 8)) / 16
		return int(retval)

	def compensate_z( self, mag_data_z, data_rhall):
		""" obtain the compensated magnetometer Z axis data(micro-tesla) in int16_t """
		retval = 0

		if mag_data_z == BMM150_ZAXIS_HALL_OVERFLOW_ADCVAL:
			return BMM150_OVERFLOW_OUTPUT

		if ((self.trim_data.dig_z2 != 0) and (self.trim_data.dig_z1 != 0) and
			(data_rhall != 0) and (self.trim_data.dig_xyz1 != 0)):
			# Processing compensation equations
			process_comp_z0 = data_rhall - self.trim_data.dig_xyz1
			process_comp_z1 = (self.trim_data.dig_z3 * process_comp_z0) / 4
			process_comp_z2 = (mag_data_z - self.trim_data.dig_z4) * 32768
			process_comp_z3 = int(self.trim_data.dig_z1) * (data_rhall * 2)
			process_comp_z4 = int( (process_comp_z3 + 32768) / 65536 )
			retval = int( (process_comp_z2 - process_comp_z1) / (self.trim_data.dig_z2 + process_comp_z4) )

			# saturate result to +/- 2 micro-tesla
			if retval > BMM150_POSITIVE_SATURATION_Z :
				retval =  BMM150_POSITIVE_SATURATION_Z
			elif retval < BMM150_NEGATIVE_SATURATION_Z :
				retval = BMM150_NEGATIVE_SATURATION_Z

			# Conversion of LSB to micro-tesla
			return int( retval / 16 )
		else:
			return BMM150_OVERFLOW_OUTPUT


	def set_op_mode( self, pwr_mode ):
		""" Set the Power mode """
		if pwr_mode==BMM150_NORMAL_MODE:
			# If the sensor is in suspend mode put the device to sleep mode
			self.suspend_to_sleep_mode()
			self.write_op_mode( pwr_mode )
			return
		elif pwr_mode==BMM150_FORCED_MODE:
			# If the sensor is in suspend mode put the device to sleep mode
			self.suspend_to_sleep_mode()
			self.write_op_mode( pwr_mode )
			return
		elif pwr_mode==BMM150_SLEEP_MODE:
			# If the sensor is in suspend mode put the device to sleep mode
			self.suspend_to_sleep_mode()
			self.write_op_mode( pwr_mode )
			return
		elif pwr_mode==BMM150_SUSPEND_MODE:
			# Set the power control bit to zero
			self.set_power_control_bit( BMM150_POWER_CNTRL_DISABLE )
			return

	def read_trim_registers( self ):
		""" reads the trim registers of the sensor and stores the trim values
			in the 'trim_data' of device structure """
		# uint8_t trim_x1y1[2] = {0};
		# uint8_t trim_xyz_data[4] = {0};
		# uint8_t trim_xy1xy2[10] = {0};
		# uint16_t temp_msb = 0;

		# Trim register value is read
		#i2c_read(BMM150_DIG_X1, trim_x1y1, 2);
		self.i2c.readfrom_mem_into( self.addr, BMM150_DIG_X1, self.buf2 )
		# i2c_read(BMM150_DIG_Z4_LSB, trim_xyz_data, 4);
		self.i2c.readfrom_mem_into( self.addr, BMM150_DIG_Z4_LSB, self.buf4 )
		# i2c_read(BMM150_DIG_Z2_LSB, trim_xy1xy2, 10);
		self.i2c.readfrom_mem_into( self.addr, BMM150_DIG_Z2_LSB, self.buf10 )

		#Trim data which is read is updated in the device structure
		self.trim_data.dig_x1 = self.buf2[0] # trim_x1y1[0]
		self.trim_data.dig_y1 = self.buf2[1] # trim_x1y1[1];
		self.trim_data.dig_x2 =  self.buf4[2] # (int8_t)trim_xyz_data[2];
		self.trim_data.dig_y2 =  self.buf4[3] # (int8_t)trim_xyz_data[3];
		temp_msb = self.buf10[3] << 8 # ((uint16_t)trim_xy1xy2[3]) << 8;
		self.trim_data.dig_z1 = temp_msb | self.buf10[2] # (uint16_t)(temp_msb | trim_xy1xy2[2]);
		temp_msb = self.buf10[1] << 8 # ((uint16_t)trim_xy1xy2[1]) << 8;
		self.trim_data.dig_z2 = temp_msb | self.buf10[0] # (int16_t)(temp_msb | trim_xy1xy2[0]);
		temp_msb = self.buf10[7] << 8 # ((uint16_t)trim_xy1xy2[7]) << 8;
		self.trim_data.dig_z3 = temp_msb | self.buf10[6] # (int16_t)(temp_msb | trim_xy1xy2[6]);
		temp_msb = self.buf4[1] << 8 # ((uint16_t)trim_xyz_data[1]) << 8;
		self.trim_data.dig_z4 = temp_msb | self.buf4[0] # (int16_t)(temp_msb | trim_xyz_data[0]);
		self.trim_data.dig_xy1 = self.buf10[9] # trim_xy1xy2[9];
		self.trim_data.dig_xy2 = self.buf10[8] # (int8_t)trim_xy1xy2[8];
		temp_msb = (self.buf10[5] & 0x7F) << 8 # ((uint16_t)(trim_xy1xy2[5] & 0x7F)) << 8;
		self.trim_data.dig_xyz1 = temp_msb | self.buf10[4] # (uint16_t)(temp_msb | trim_xy1xy2[4]);

	def write_op_mode( self, op_mode ):
		""" writes the op_mode value in the Opmode bits (bits 1 and 2) """
		# reg_data = self.i2c_read( BMM150_OP_MODE_ADDR )
		self.i2c.readfrom_mem_into( self.addr, BMM150_OP_MODE_ADDR, self.buf1 )
		# Set the op_mode value in Opmode bits of 0x4C
		self.buf1[0] = set_bits(self.buf1[0], BMM150_OP_MODE, op_mode)
		# self.i2c_write(BMM150_OP_MODE_ADDR, reg_data);
		self.i2c.writeto_mem( self.addr, BMM150_OP_MODE_ADDR, self.buf1 )

	def set_preset_mode( self, mode ):
		""" Set preset mode mode """
		pass

	def set_power_control_bit( self, pwrcntrl_bit ):
		""" sets/resets the power control bit """
		# Power control register 0x4B is read
		# reg_data = i2c_read(BMM150_POWER_CONTROL_ADDR);
		self.i2c.readfrom_mem_into( self.addr, BMM150_POWER_CONTROL_ADDR, self.buf1 )

		# Sets the value of power control bit
		# reg_data = BMM150_SET_BITS_POS_0(reg_data, BMM150_PWR_CNTRL, pwrcntrl_bit);
		self.buf1[0] = set_bits_pos0( self.buf1[0], BMM150_PWR_CNTRL, pwrcntrl_bit )
		#i2c_write(BMM150_POWER_CONTROL_ADDR, reg_data);
		self.i2c.writeto_mem( self.addr, BMM150_POWER_CONTROL_ADDR, self.buf1 )

	def suspend_to_sleep_mode( self ):
		""" suspend to sleep mode by setting the power control bit to 1 """
		self.set_power_control_bit( BMM150_POWER_CNTRL_ENABLE )
		# Start-up time delay of 3ms
		sleep_ms( 3 )

	def set_presetmode( self, preset_mode ):
		""" set the preset mode of the sensor """
		if preset_mode==BMM150_PRESETMODE_LOWPOWER :
			# Set the data rate x,y,z repetition for Low Power mode
			self.settings.data_rate = BMM150_DATA_RATE_10HZ
			self.settings.xy_rep = BMM150_LOWPOWER_REPXY
			self.settings.z_rep = BMM150_LOWPOWER_REPZ
			self.set_odr_xyz_rep()
		elif preset_mode==BMM150_PRESETMODE_REGULAR :
			# Set the data rate x,y,z repetition for Regular mode
			self.settings.data_rate = BMM150_DATA_RATE_10HZ
			self.settings.xy_rep = BMM150_REGULAR_REPXY
			self.settings.z_rep = BMM150_REGULAR_REPZ
			self.set_odr_xyz_rep()
		elif preset_mode==BMM150_PRESETMODE_HIGHACCURACY :
			# Set the data rate x,y,z repetition for High Accuracy mode
			self.settings.data_rate = BMM150_DATA_RATE_20HZ
			self.settings.xy_rep = BMM150_HIGHACCURACY_REPXY
			self.settings.z_rep = BMM150_HIGHACCURACY_REPZ
			self.set_odr_xyz_rep()
		elif preset_mode==BMM150_PRESETMODE_ENHANCED :
			# Set the data rate x,y,z repetition for Enhanced Accuracy mode
			self.settings.data_rate = BMM150_DATA_RATE_10HZ
			self.settings.xy_rep = BMM150_ENHANCED_REPXY
			self.settings.z_rep = BMM150_ENHANCED_REPZ
			self.set_odr_xyz_rep()
		else:
			raise BMM150_Error( 'Invalid preset_mode %i' % preset_mode )

 	def set_odr_xyz_rep( self ):
		""" sets the preset mode ODR (Output Data Rate) and repetition settings """
		# Set the ODR
		self.set_odr()
		# Set the XY-repetitions number
		self.set_xy_rep()
		# Set the Z-repetitions number
		self.set_z_rep()

	def set_xy_rep( self ):
		""" sets the xy repetition from bmm150_settings struct """
		self.buf1[0] = self.settings.xy_rep
		# i2c_write(BMM150_REP_XY_ADDR, rep_xy);
		self.i2c.writeto_mem( self.addr, BMM150_REP_XY_ADDR, self.buf1 )

	def set_z_rep( self ):
		""" sets the z repetition from bmm150_settings struct """
		self.buf1[0]  = self.settings.z_rep;
		# i2c_write(BMM150_REP_Z_ADDR, rep_z);
		self.i2c.writeto_mem( self.addr, BMM150_REP_Z_ADDR, self.buf1 )

	def set_odr( self ):
		""" Set the output data rate of the sensor from bmm150_settings struct """
		# reg_data = i2c_read(BMM150_OP_MODE_ADDR);
		self.i2c.readfrom_mem_into( self.addr, BMM150_OP_MODE_ADDR, self.buf1 )
		# Set the ODR value
		self.buf1[0] = set_bits( self.buf1[0], BMM150_ODR, self.settings.data_rate )
		#i2c_write(BMM150_OP_MODE_ADDR, reg_data);
		self.i2c.writeto_mem( self.addr, BMM150_OP_MODE_ADDR, self.buf1 )

	def soft_reset( self ):
		""" Reset all register except 0x48 """
		# reg_data = i2c_read(BMM150_POWER_CONTROL_ADDR);
		self.i2c.readfrom_mem_into( self.addr, BMM150_POWER_CONTROL_ADDR, self.buf1 )
		self.buf1[0] = self.buf1[0] | BMM150_SET_SOFT_RESET
		# i2c_write(BMM150_POWER_CONTROL_ADDR, reg_data);
		self.i2c.writeto_mem( self.addr, BMM150_POWER_CONTROL_ADDR, self.buf1 )
		sleep_ms( BMM150_SOFT_RESET_DELAY )
