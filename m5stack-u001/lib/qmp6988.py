"""
qmp6988.py : MicroPython driver for M5Stack U001-C, Atmospheric pressure
             QMP6988 I2C sensor.
* Author(s):
   23 aug 2022: Meurisse D. (shop.mchobby.be) - port to MicroPython
	https://github.com/m5stack/M5-DLight
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u001"

from micropython import const
import time
import struct


QMP6988_SLAVE_ADDRESS_L = const(0x70)
QMP6988_SLAVE_ADDRESS_H = const(0x56)

# QMP6988_U16_t unsigned short
# QMP6988_S16_t short
# QMP6988_U32_t unsigned int
# QMP6988_S32_t int
# QMP6988_U64_t unsigned long long
# QMP6988_S64_t long long

QMP6988_CHIP_ID = const(0x5C)

QMP6988_CHIP_ID_REG     = const(0xD1)
QMP6988_RESET_REG       = const(0xE0) # Device reset register
QMP6988_DEVICE_STAT_REG = const(0xF3) # Device state register
QMP6988_CTRLMEAS_REG    = const(0xF4) # Measurement Condition Control Register
# data
QMP6988_PRESSURE_MSB_REG    = const(0xF7) # Pressure MSB Register
QMP6988_TEMPERATURE_MSB_REG = const(0xFA) # Temperature MSB Reg

# compensation calculation */
QMP6988_CALIBRATION_DATA_START = const(0xA0) # QMP6988 compensation coefficients
QMP6988_CALIBRATION_DATA_LENGTH = const(25)

#define SHIFT_RIGHT_4_POSITION 4
#define SHIFT_LEFT_2_POSITION  2
#define SHIFT_LEFT_4_POSITION  4
#define SHIFT_LEFT_5_POSITION  5
#define SHIFT_LEFT_8_POSITION  8
#define SHIFT_LEFT_12_POSITION 12
#define SHIFT_LEFT_16_POSITION 16

# power mode */
QMP6988_SLEEP_MODE  = const(0x00)
QMP6988_FORCED_MODE = const(0x01)
QMP6988_NORMAL_MODE = const(0x03)

QMP6988_CTRLMEAS_REG_MODE__POS = const(0)
QMP6988_CTRLMEAS_REG_MODE__MSK = const(0x03)
QMP6988_CTRLMEAS_REG_MODE__LEN = const(2)

# oversampling
QMP6988_OVERSAMPLING_SKIPPED = const(0x00)
QMP6988_OVERSAMPLING_1X      = const(0x01)
QMP6988_OVERSAMPLING_2X      = const(0x02)
QMP6988_OVERSAMPLING_4X      = const(0x03)
QMP6988_OVERSAMPLING_8X      = const(0x04)
QMP6988_OVERSAMPLING_16X     = const(0x05)
QMP6988_OVERSAMPLING_32X     = const(0x06)
QMP6988_OVERSAMPLING_64X     = const(0x07)

QMP6988_CTRLMEAS_REG_OSRST__POS = const(5)
QMP6988_CTRLMEAS_REG_OSRST__MSK = const(0xE0)
QMP6988_CTRLMEAS_REG_OSRST__LEN = const(3)

QMP6988_CTRLMEAS_REG_OSRSP__POS = const(2)
QMP6988_CTRLMEAS_REG_OSRSP__MSK = const(0x1C)
QMP6988_CTRLMEAS_REG_OSRSP__LEN = const(3)

# filter
QMP6988_FILTERCOEFF_OFF = const(0x00)
QMP6988_FILTERCOEFF_2   = const(0x01)
QMP6988_FILTERCOEFF_4   = const(0x02)
QMP6988_FILTERCOEFF_8   = const(0x03)
QMP6988_FILTERCOEFF_16  = const(0x04)
QMP6988_FILTERCOEFF_32  = const(0x05)

QMP6988_CONFIG_REG             = const(0xF1) # IIR filter co-efficient setting Register*/
QMP6988_CONFIG_REG_FILTER__POS = const(0)
QMP6988_CONFIG_REG_FILTER__MSK = const(0x07)
QMP6988_CONFIG_REG_FILTER__LEN = const(3)

SUBTRACTOR = const(8388608)

class QMP6988_CALI_DATA_T:
	def __init__(self):
		self.COE_a0  =0 # s32
		self.COE_a1  =0 # s16
		self.COE_a2  =0 # s16
		self.COE_b00 =0 # s32
		self.COE_bt1 =0 # s16
		self.COE_bt2 =0 # s16
		self.COE_bp1 =0 # s16
		self.COE_b11 =0 # s16
		self.COE_bp2 =0 # s16
		self.COE_b12 =0 # s16
		self.COE_b21 =0 # s16
		self.COE_bp3 =0 # s16


# _qmp6988_cali_data = QMP6988_CALI_DATA_T()

class QMP6988_FK_DATA_T:
	def __ini__(self):
		self.a0 = 0.0 # float
		self.b00= 0.0 # float
		# floats
		self.a1 = 0.0
		self.a2 = 0.0
		self.bt1= 0.0
		self.bt2= 0.0
		self.bp1= 0.0
		self.b11= 0.0
		self.bp2= 0.0
		self.b12= 0.0
		self.b21= 0.0
		self.bp3= 0.0

 # _qmp6988_fk_data = QMP6988_FK_DATA_T()

class QMP6988_IK_DATA_T:
	def __ini__(self):
		self.a0  = 0.0 # s32
		self.b00 = 0.0 # s32
		self.a1 = 0.0 # s32
		self.a2 = 0.0 # s32
		# s64²
		self.bt1 = 0.0
		self.bt2 = 0.0
		self.bp1 = 0.0
		self.b11 = 0.0
		self.bp2 = 0.0
		self.b12 = 0.0
		self.b21 = 0.0
		self.bp3 = 0.0

# _qmp6988_ik_data = QMP6988_IK_DATA_T()

class QMP6988_DATA_T:
	def __init__(self):
		self.slave = 0 # uint8_t
		self.chip_id = 0 # uint8_t
		self.power_mode = 0 # uint8_t
		self.temperature = 0.0
		self.pressure = 0.0
		self.altitude = 0.0
		self.qmp6988_cali = QMP6988_CALI_DATA_T()
		self.ik = QMP6988_IK_DATA_T()

_qmp6988_data = QMP6988_DATA_T()

class QMP6988:
	def __init__( self, i2c, addr=0x70 ):
		self.i2c = i2c
		self.addr = addr
		self.data = QMP6988_DATA_T()
		self.buf1 = bytearray(1)
		self.buf6 = bytearray(6)

		# Init()
		self.device_check()
		# rely on PowerOnReset
		# self.reset()
		print( 'get_calibration_data')
		self.get_calibration_data()
		self.set_power_mode( QMP6988_NORMAL_MODE )
		self.set_filter( QMP6988_FILTERCOEFF_4 )
		self.set_oversampling_p( QMP6988_OVERSAMPLING_8X )
		self.set_oversampling_t(QMP6988_OVERSAMPLING_1X)
		print("init done")

	# read calibration data from otp
	def get_calibration_data( self ): # int
		# BITFIELDS temp_COE;
		#   uint8_t a_data_uint8_tr[QMP6988_CALIBRATION_DATA_LENGTH] = {0};
		a_data_uint8_tr = bytearray( QMP6988_CALIBRATION_DATA_LENGTH )
		self.i2c.readfrom_mem_into( self.addr, QMP6988_CALIBRATION_DATA_START, a_data_uint8_tr )

		self.data.qmp6988_cali.COE_a0 = ((a_data_uint8_tr[18] << 12) |
			(a_data_uint8_tr[19] << 4) | (a_data_uint8_tr[24] & 0x0f)) << 12
		self.data.qmp6988_cali.COE_a0 = (self.data.qmp6988_cali.COE_a0 & 0xFFFFFFFF) >> 12

		self.data.qmp6988_cali.COE_a1 = (a_data_uint8_tr[20] << 8) | a_data_uint8_tr[21]
		self.data.qmp6988_cali.COE_a2 = ((a_data_uint8_tr[22]) << 8) | a_data_uint8_tr[23]

		self.data.qmp6988_cali.COE_b00 = ((a_data_uint8_tr[0] << 12) | (a_data_uint8_tr[1] << 4) | ((a_data_uint8_tr[24] & 0xf0) >> 4)) << 12
		self.data.qmp6988_cali.COE_b00 = (self.data.qmp6988_cali.COE_b00 & 0xFFFFFFFF) >> 12
		self.data.qmp6988_cali.COE_bt1 = (a_data_uint8_tr[2] << 8) | a_data_uint8_tr[3]
		self.data.qmp6988_cali.COE_bt2 = (a_data_uint8_tr[4] << 8) | a_data_uint8_tr[5]
		self.data.qmp6988_cali.COE_bp1 = (a_data_uint8_tr[6] << 8) | a_data_uint8_tr[7]
		self.data.qmp6988_cali.COE_b11 = (a_data_uint8_tr[8] << 8) | a_data_uint8_tr[9]
		self.data.qmp6988_cali.COE_bp2 = (a_data_uint8_tr[10] << 8) | a_data_uint8_tr[11]
		self.data.qmp6988_cali.COE_b12 = (a_data_uint8_tr[12] << 8) | a_data_uint8_tr[13]
		self.data.qmp6988_cali.COE_b21 = (a_data_uint8_tr[14] << 8) | a_data_uint8_tr[15]
		self.data.qmp6988_cali.COE_bp3 = (a_data_uint8_tr[16] << 8) | a_data_uint8_tr[17]


		self.data.ik.a0  = self.data.qmp6988_cali.COE_a0   # 20Q4
		self.data.ik.b00 = self.data.qmp6988_cali.COE_b00  # 20Q4

		self.data.ik.a1 = 3608  * self.data.qmp6988_cali.COE_a1 - 1731677965 # 31Q23
		self.data.ik.a2 = 16889 * self.data.qmp6988_cali.COE_a2 - 87619360 # 30Q47

		self.data.ik.bt1 = 2982   * self.data.qmp6988_cali.COE_bt1 + 107370906 # 28Q15
		self.data.ik.bt2 = 329854 * self.data.qmp6988_cali.COE_bt2 + 108083093 # 34Q38
		self.data.ik.bp1 = 19923  * self.data.qmp6988_cali.COE_bp1 + 1133836764 # 31Q20
		self.data.ik.b11 = 2406   * self.data.qmp6988_cali.COE_b11 + 118215883 # 28Q34
		self.data.ik.bp2 = 3079   * self.data.qmp6988_cali.COE_bp2 - 181579595 # 29Q43
		self.data.ik.b12 = 6846   * self.data.qmp6988_cali.COE_b12 + 85590281 # 29Q53
		self.data.ik.b21 = 13836  * self.data.qmp6988_cali.COE_b21 + 79333336 # 29Q60
		self.data.ik.bp3 = 2915   * self.data.qmp6988_cali.COE_bp3 + 157155561 # 28Q65

	# QMP6988_S32_t getPressure02e(qmp6988_ik_data_t* ik, QMP6988_S32_t dp, QMP6988_S16_t tx);
	def get_pressure02e( self, ik, dp, tx):
		# QMP6988_S32_t ret;
		# QMP6988_S64_t wk1, wk2, wk3;

		# wk1 = 48Q16, bit size
		wk1 = (ik.bt1 * tx)      # 28Q15+16-1=43 (43Q15)
		wk2 = (ik.bp1 * dp) >> 5 # 31Q20+24-1=54 (49Q15)
		wk1 += wk2               # 43,49->50Q15
		wk2 = (ik.bt2 * tx) >> 1 # 34Q38+16-1=49 (48Q37)
		wk2 = (wk2 * tx) >> 8    # 48Q37+16-1=63 (55Q29)
		wk3 = wk2                # 55Q29
		wk2 = (ik.b11 * tx) >> 4 # 28Q34+16-1=43 (39Q30)
		wk2 = (wk2 * dp) >> 1    # 39Q30+24-1=62 (61Q29)
		wk3 += wk2               # 55,61->62Q29
		wk2 = (ik.bp2 * dp)>> 13 # 29Q43+24-1=52 (39Q30)
		wk2 = (wk2 * dp) >> 1    # 39Q30+24-1=62 (61Q29)
		wk3 += wk2               # 62,61->63Q29
		wk1 += wk3 >> 14         # Q29 >> 14 -> Q15
		wk2 = ik.b12 * tx        # 29Q53+16-1=45 (45Q53)
		wk2 = (wk2 * tx) >> 22   # 45Q53+16-1=61 (39Q31)
		wk2 = (wk2 * dp) >> 1    # 39Q31+24-1=62 (61Q30)
		wk3 = wk2                # 61Q30
		wk2 = (ik.b21 * tx)>> 6  # 29Q60+16-1=45 (39Q54)
		wk2 = (wk2 * dp) >> 23   # 39Q54+24-1=62 (39Q31)
		wk2 = (wk2 * dp) >> 1    # 39Q31+24-1=62 (61Q20)
		wk3 += wk2               # 61,61->62Q30
		wk2 = (ik.bp3 * dp)>> 12 # 28Q65+24-1=51 (39Q53)
		wk2 = (wk2 * dp) >> 23   # 39Q53+24-1=62 (39Q30)
		wk2 = wk2 * dp           # 39Q30+24-1=62 (62Q30)
		wk3 += wk2               # 62,62->63Q30
		wk1 += wk3 >> 15         # Q30 >> 15 = Q15
		wk1 = wk1 // 32767
		wk1 = wk1 >> 11          # Q15 >> 7 = Q4
		wk1 += ik.b00            # Q4 + 20Q4
		# wk1 >>= 4; // 28Q4 -> 24Q0
		return wk1

	#QMP6988_S16_t convTx02e(qmp6988_ik_data_t* ik, QMP6988_S32_t dt);
	def convTx02e( self, ik, dt):
		# QMP6988_S16_t ret;
		# QMP6988_S64_t wk1, wk2;

		# wk1: 60Q4 // bit size
		wk1 = (ik.a1 * dt)       # 31Q23+24-1=54 (54Q23)
		wk2 = (ik.a2 * dt) >> 14 # 30Q47+24-1=53 (39Q33)
		wk2 = (wk2 * dt) >> 10   # 39Q33+24-1=62 (52Q23)
		wk2 = int((wk1 + wk2) / 32767) >> 19 # 54,52->55Q23 (20Q04)
		return ((ik.a0 + wk2) >> 4 ) & 0xFFFF # 21Q4 -> 17Q0 (QMP6988_S16_t)

	def reset( self ): # SoftwareReset
		self.buf1[0] = 0xe6
		self.i2c.writeto_mem(self.addr, QMP6988_RESET_REG, self.buf1 ) # This line completely stuck the I2C bus
		time.sleep_ms( 20 )
		self.buf1[0] = 0x00
		self.i2c.writeto_mem(self.addr, QMP6988_RESET_REG, self.buf1 )


	def device_check( self ):
		self.i2c.readfrom_mem_into( self.addr, QMP6988_CHIP_ID_REG, self.buf1 )
		self.data.chip_id = self.buf1[0]
		if self.data.chip_id != QMP6988_CHIP_ID:
			raise Exception('Invalid Chip_ID %s @ addr %s !' % (hex(seld.data.chip_id),hex(self.addr)) )

	def calc_altitude( self, pressure, temp ):
		pass


	@property
	def pressure( self ): # float, calc_pressure
		#uint8_t err = 0;
		#QMP6988_U32_t P_read, T_read;
		#QMP6988_S32_t P_raw, T_raw;
		#uint8_t a_data_uint8_tr[6] = {0};
		#QMP6988_S32_t T_int, P_int;

		# press
		# err = readData(slave_addr, QMP6988_PRESSURE_MSB_REG, a_data_uint8_tr, 6);
		self.i2c.readfrom_mem_into( self.addr, QMP6988_PRESSURE_MSB_REG, self.buf6 )

		P_read = (self.buf6[0] << 16) | (self.buf6[1] << 8) | self.buf6[2]
		P_raw  = P_read - SUBTRACTOR
		T_read = (self.buf6[3] << 16) | (self.buf6[4] << 8) | self.buf6[5]
		T_raw  = T_read - SUBTRACTOR
		T_int               = self.convTx02e( self.data.ik, T_raw )
		P_int               = self.get_pressure02e(self.data.ik, P_raw, T_int )
		self.data.temperature = T_int / 256.0
		self.data.pressure    = P_int / 16.0
		return self.data.pressure


 	def set_power_mode( self, power_mode ):
		self.data.power_mode = power_mode
		# readData(slave_addr, QMP6988_CTRLMEAS_REG, &data, 1);
		self.i2c.readfrom_mem_into( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		data = self.buf1[0] & 0xFC
		if power_mode == QMP6988_SLEEP_MODE:
			data = data | 0x00
		elif power_mode == QMP6988_FORCED_MODE:
			data = data | 0x01
		elif power_mode == QMP6988_NORMAL_MODE:
			data = data | 0x03

		self.buf1[0] = data
		self.i2c.writeto_mem( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		time.sleep_ms(20)

	def set_filter(self, filter): # unsigned char
		self.buf1[0] = filter & 0x03
		self.i2c.writeto_mem( self.addr, QMP6988_CONFIG_REG, self.buf1 )
		time.sleep_ms( 20 )

	def set_oversampling_p( self, oversampling_p ): # unsigned char
		self.i2c.readfrom_mem_into( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		data = self.buf1[0] & 0xE3
		self.buf1[0] = data | (oversampling_p << 2)
		self.i2c.writeto_mem( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		time.sleep_ms( 20 )

	def set_oversampling_t( self, oversampling_t ):
		self.i2c.readfrom_mem_into( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		data = self.buf1[0] & 0x1F
		self.buf1[0] = data | (oversampling_t << 5)
		self.i2c.writeto_mem( self.addr, QMP6988_CTRLMEAS_REG, self.buf1 )
		time.sleep_ms( 20 )

	# uint8_t writeReg(uint8_t slave, uint8_t reg_add, uint8_t reg_dat);
	# uint8_t readData(uint16_t slave, uint8_t reg_add, unsigned char* Read, uint8_t num);
