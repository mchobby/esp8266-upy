"""
vmeter.py : MicroPython driver for M5Stack U087, I2C based VMeter grove unit.

* Author(s):
   28 may 2021: Meurisse D. (shop.mchobby.be) - port to MicroPython
				https://github.com/m5stack/M5-ProductExampleCodes/blob/master/Unit/V_Meter_Unit
"""

__version__ = "0.0.2.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u087"

from micropython import const
import time
import struct

ADS115_ADDR = const(0x49)
EEPROM_ADDR = const(0x53)

BUS_DELAY_MS = 10 # Avoids I2C bus to HANG because of too much consecutive reading

ADS1115_RA_CONVERSION = const( 0x00 )
ADS1115_RA_CONFIG     = const( 0x01 )

# Resolution en mV/unit of ADS1115
ADS1115_MV_6144       =  0.187500
ADS1115_MV_4096       =  0.125000
ADS1115_MV_2048       =  0.062500 # default
ADS1115_MV_1024       =  0.031250
ADS1115_MV_512        =  0.015625
ADS1115_MV_256        =  0.007813

VOLTMETER_MEASURING_DIR = -1

ADS1115_MUX_P0N1 = const( 0x00 ) # voltmeter only support

ADS1115_COMP_MODE_HYSTERESIS  = const( 0x00 ) # default
ADS1115_COMP_MODE_WINDOW      = const( 0x01 )

ADS1115_MODE_CONTINUOUS    = const( 0x00 )
ADS1115_MODE_SINGLESHOT    = const( 0x01 ) # default

VOLTMETER_PRESSURE_COEFFICIENT = 0.015918958

VOLTMETER_PAG_6144_CAL_ADDR = const( 208 )
VOLTMETER_PAG_4096_CAL_ADDR = const( 216 )
VOLTMETER_PAG_2048_CAL_ADDR = const( 224 )
VOLTMETER_PAG_1024_CAL_ADDR = const( 232 )
VOLTMETER_PAG_512_CAL_ADDR  = const( 240 )
VOLTMETER_PAG_256_CAL_ADDR  = const( 248 )

VOLTMETER_FILTER_NUMBER = const( 10 )

# typedef enum
PAG_6144 = const( 0x00 ) # 6.144 V = Gain = 2/3
PAG_4096 = const( 0x01 ) # 4.096 V - Gain = 1
PAG_2048 = const( 0x02 ) # 2.048 V - Gain = 2 (DEFAULT)
PAG_1024 = const( 0x03 ) # 1.024 V - Gain = 4
PAG_512  = const( 0x04 )   # 0.512 V - Gain = 8
PAG_256  = const( 0x05 )   # 0.256 V - Gain = 16

VOLTMETER_GAINS = [ PAG_6144, PAG_4096, PAG_2048, PAG_1024, PAG_512, PAG_256 ]

# | PAG      | Max Input Voltage(V) |
# | PAG_6144 |        128           |
# | PAG_4096 |        64            |
# | PAG_2048 |        32            |
# | PAG_512  |        16            |
# | PAG_256  |        8             |
#  MCHobby: for PAG_1024 I did use the PAG_512 max voltage
MAX_VOLTAGE = { PAG_6144 : 128, PAG_4096: 64, PAG_2048: 32, PAG_1024:16, PAG_512: 16, PAG_256: 8 }

# typedef enum  voltmeterRate_t, Number of sample per second
RATE_8   = const( 0x00 ) # 8 Samples per Second
RATE_16  = const( 0x01 )
RATE_32  = const( 0x02 )
RATE_64  = const( 0x03 )
RATE_128 = const( 0x04 ) # default
RATE_250 = const( 0x05 )
RATE_475 = const( 0x06 )
RATE_860 = const( 0x07 )

VOLTMETER_RATES = [ RATE_8, RATE_16, RATE_32, RATE_64, RATE_128, RATE_250, RATE_475, RATE_860 ]
RATE_SPS = { RATE_8 : 8, RATE_16 : 16, RATE_32 : 32, RATE_64 : 64, RATE_128 : 128, RATE_250 : 250, RATE_475 : 475, RATE_860 : 860 }

# typedef enum voltmeterMode_t
SINGLESHOT = ADS1115_MODE_SINGLESHOT
CONTINUOUS = ADS1115_MODE_CONTINUOUS

VOLTMETER_MODE = [ SINGLESHOT, CONTINUOUS ]

class Voltmeter:
	def __init__(self, i2c, ads1115_addr=0x49, eeprom_addr=0x53 ):
		self.i2c = i2c
		self._ads1115_addr = ads1115_addr
		self._eeprom_addr = eeprom_addr

		# Buffer
		self.buf2 = bytearray(2) # should be removed
		self.buf1 = bytearray(1)
		self.buf3 = bytearray(3)

		self.set_gain( PAG_2048 )
		self.set_rate( RATE_128 )
		self.set_mode( SINGLESHOT )

		# Public member
		self.resolution = self.__get_resolution( self._gain ) # Final resolution in mV
		self.cover_time = self.__get_cover_time( self._rate ) # ms required for the ADS1115 to perform a sample
		self.adc_raw    = 0 # int16_t
		self.calibration_factor = 1.0

	def __read_u16( self, addr, reg, signed=False ):
		time.sleep_ms(BUS_DELAY_MS)
		self.buf1[0] = reg
		self.i2c.writeto( addr, self.buf1 )
		time.sleep_ms(BUS_DELAY_MS)
		self.i2c.readfrom_into( addr, self.buf2 )
		val = (self.buf2[0] << 8) | self.buf2[1]
		if signed:
			#return val if val < 32768 else val - 65536
			return struct.unpack('>h', self.buf2 )[0]
		else:
			return val

	def __write_u16( self, addr, reg, value ):
		self.buf3[0] = reg
		self.buf3[1] = value >> 8
		self.buf3[2] = value & 0xff
		self.i2c.writeto( addr, self.buf3)


	def __get_resolution( self, gain, adc_only=False ): # float
		# global resolution depend on resistor bridge configuration.
		# On regular VMeter: the VOLTMETER_PRESSURE_COEFFICIENT is involved.
		# On hacked VMeter: the resistor bridge is removed so coefficient is
		#                   exactly 1. So we do read pure adc voltage.
		mv = 0
		if gain==PAG_6144:
			mv = ADS1115_MV_6144
		elif gain==PAG_4096:
			mv = ADS1115_MV_4096
		elif gain==PAG_2048:
			mv = ADS1115_MV_2048
		elif gain==PAG_1024:
			mv = ADS1115_MV_1024
		elif gain==PAG_512:
			mv = ADS1115_MV_512
		elif gain==PAG_256:
			mv = ADS1115_MV_256
		else:
			mv = ADS1115_MV_256

		if adc_only:
			return mv
		else:
			return mv / VOLTMETER_PRESSURE_COEFFICIENT

	def __get_cover_time( self, rate ): # uint16
		""" ms required for the ADS1115 to perform a sample """
		if rate==RATE_8:
			return int(1000 / 8)
		elif rate==RATE_16:
			return int(1000 / 16)
		elif rate==RATE_32:
			return int(1000 / 32)
		elif rate==RATE_64:
			return int(1000 / 64)
		elif rate==RATE_128:
			return int(1000 / 128)
		elif rate==RATE_250:
			return int(1000 / 250)
		elif rate==RATE_475:
			return int(1000 / 475)
		elif rate==RATE_860:
			return int(1000 / 860)
		else:
			return int(1000 / 128)

	def __get_pga_eeprom_addr( self, gain): # uint8_t
		if gain==PAG_6144:
			return VOLTMETER_PAG_6144_CAL_ADDR
		elif gain==PAG_4096:
			return VOLTMETER_PAG_4096_CAL_ADDR
		elif gain==PAG_2048:
			return VOLTMETER_PAG_2048_CAL_ADDR
		elif gain==PAG_1024:
			return VOLTMETER_PAG_1024_CAL_ADDR
		elif gain==PAG_512:
			return VOLTMETER_PAG_512_CAL_ADDR
		elif gain==PAG_256:
			return VOLTMETER_PAG_256_CAL_ADDR
		else:
			return 0x00

	@property
	def sample_rate( self ):
		# Rate in SPS
		return RATE_SPS[self._rate]

	@property
	def max_voltage( self ):
		# Max voltage (V) depends on the current gain
		return MAX_VOLTAGE[self._gain]

	def set_gain( self, gain ):
		# Set ADC gain, this have impact on the resolution and Max_voltage
		time.sleep_ms(BUS_DELAY_MS)
		reg_value = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONFIG )

		reg_value &= (0xFFFF ^ (0b0111 << 9))
		reg_value |= (gain << 9)

		time.sleep_ms(BUS_DELAY_MS)
		self.__write_u16( self._ads1115_addr, ADS1115_RA_CONFIG, reg_value)

		self._gain = gain
		self.resolution = self.__get_resolution( gain )

		hope, actual = self.__readCalibrationFromEEPROM( gain ) #, &hope, &actual)) {
		self.calibration_factor = hope / actual


	def set_rate( self, rate ):
		#uint16_t reg_value = 0;
		time.sleep_ms(BUS_DELAY_MS)
		reg_value = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONFIG ) #, &reg_value);

		reg_value &= (0xFFFF ^ (0b0111 << 5))
		reg_value |= (rate << 5)

		time.sleep_ms(BUS_DELAY_MS)
		self.__write_u16( self._ads1115_addr, ADS1115_RA_CONFIG, reg_value )

		self._rate = rate
		self.cover_time = self.__get_cover_time( rate )


	def set_mode( self, mode ):
		time.sleep_ms(BUS_DELAY_MS)
		reg_value = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONFIG )

		reg_value &= (0xFFFF ^ (0b0001 << 8))
		reg_value |= (mode << 8)

		time.sleep_ms(BUS_DELAY_MS)
		self.__write_u16( self._ads1115_addr, ADS1115_RA_CONFIG, reg_value);
		self._mode = mode


	def get_voltage( self, calibration=True, adc_only=False ): # float
		# adc_only : read ADC voltage (do not taking care of voltage divider...
		#			 just the ADC input voltage)
		# return the value in mV
		if adc_only:
			return self.__get_resolution(self._gain, adc_only=True) * self.get_conversion() * VOLTMETER_MEASURING_DIR
		else:
			# Read VMeter module input (we can use the resolution taking care of resistor divider bridge)
			if calibration:
				return self.resolution * self.calibration_factor * self.get_conversion() * VOLTMETER_MEASURING_DIR
			else:
				return self.resolution * self.get_conversion() * VOLTMETER_MEASURING_DIR

	@property
	def voltage( self ):
		return self.get_voltage() / 1000 # Return as volts

	@property
	def adc_mv( self ):
		return self.get_voltage( adc_only=True ) # Return as milliVolts

	def get_conversion( self, timeout=125): # int16_t
		if self._mode == SINGLESHOT:
			self.start_single_conversion()
			time.sleep_ms( self.cover_time )
			_time = time.ticks_ms() + timeout
			while (_time > time.ticks_ms()) and self.is_in_conversion():
				time.sleep_ms(10)

		return self.get_adc_raw()


	def get_adc_raw( self ): # int16_t
		self.adc_raw = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONVERSION, signed=True )
		return self.adc_raw


	def is_in_conversion( self ):
		time.sleep_ms(BUS_DELAY_MS)
		value = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONFIG )
		return True if (value & (1 << 15)) else False


	def start_single_conversion( self ):
		time.sleep_ms(BUS_DELAY_MS)
		reg_value = self.__read_u16( self._ads1115_addr, ADS1115_RA_CONFIG )

		reg_value |= (0x01 << 15)

		time.sleep_ms(BUS_DELAY_MS)
		self.__write_u16( self._ads1115_addr, ADS1115_RA_CONFIG, reg_value)


	def eeprom_read( self, address, buff ): # third parameter was 'len'
		time.sleep_ms(BUS_DELAY_MS)
		self.i2c.readfrom_mem_into( self._eeprom_addr, address, buff )

	#bool EEPORMWrite(uint8_t address, uint8_t* buff, uint8_t len);
	# See https://github.com/m5stack/M5-ProductExampleCodes/blob/master/Unit/V_Meter_Unit/voltmeter/voltmeter.cpp

	def set_calibration( self, voltage, actual): # int8_t, uint16_t
		# Defined in the prototype but not implemented in the CPP
		pass


	def __saveCalibrationToEEPROM( gain, hope, actual): # voltmeterGain_t gain, int16_t hope, int16_t actual. Returns bool
		pass
		# See https://github.com/m5stack/M5-ProductExampleCodes/blob/master/Unit/V_Meter_Unit/voltmeter/voltmeter.cpp


	def __readCalibrationFromEEPROM( self, gain ):
		# Returns (hope, actual) from EEPROM data readed for a given gain
		addr = self.__get_pga_eeprom_addr( gain )
		buf8 = bytearray(8)
		for i in range(8):
			buf8[i] = 0

		hope = 1
		actual = 1
		self.eeprom_read( addr, buf8 )

		xor_result = 0x00
		for i in range(5):
			xor_result ^= buf8[i]

		if xor_result != buf8[5]:
			raise Exception( 'Invalid XOR for gain %i @ eeprom addr %i' %(gain, addr) )

		hope = (buf8[1] << 8) | buf8[2]
		actual = (buf8[3] << 8) | buf8[4]
		return (hope,actual)
