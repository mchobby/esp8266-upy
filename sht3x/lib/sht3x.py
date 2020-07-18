"""

	based on DFRobot Arduino code for SHT31-F. See https://wiki.dfrobot.com/SHT31-F%20Digital%20Temperature%20and%20Humidity%20Sensor%20SKU:%20SEN0332
"""
from time import sleep_ms
import struct

SHT3X_CMD_READ_SERIAL_NUMBER           =  0x3780 # Read the chip serial number
SHT3X_CMD_FETCH_DATA				   =  0xE000
SHT3X_CMD_GETDATA_H_CLOCKENABLED       =  0x2C06 # Measurement:high repeatability
SHT3X_CMD_GETDATA_M_CLOCKENABLED       =  0x2C0D # Measurement: medium repeatability
SHT3X_CMD_GETDATA_L_CLOCKENABLED       =  0x2C10 # Measurement: low repeatability

SHT3X_CMD_SETMODE_H_FREQUENCY_HALF_HZ  =  0x2032 # Measurement: periodic 0.5 mps, high repeatability
SHT3X_CMD_SETMODE_M_FREQUENCY_HALF_HZ  =  0x2024 # Measurement: periodic 0.5 mps, medium
SHT3X_CMD_SETMODE_L_FREQUENCY_HALF_HZ  =  0x202F # Measurement: periodic 0.5 mps, low repeatability
SHT3X_CMD_SETMODE_H_FREQUENCY_1_HZ     =  0x2130 # Measurement: periodic 1 mps, high repeatability
SHT3X_CMD_SETMODE_M_FREQUENCY_1_HZ     =  0x2126 # Measurement: periodic 1 mps, medium repeatability
SHT3X_CMD_SETMODE_L_FREQUENCY_1_HZ     =  0x212D # Measurement: periodic 1 mps, low repeatability
SHT3X_CMD_SETMODE_H_FREQUENCY_2_HZ     =  0x2236 # Measurement: periodic 2 mps, high repeatability
SHT3X_CMD_SETMODE_M_FREQUENCY_2_HZ     =  0x2220 # Measurement: periodic 2 mps, medium repeatability
SHT3X_CMD_SETMODE_L_FREQUENCY_2_HZ     =  0x222B # Measurement: periodic 2 mps, low repeatability
SHT3X_CMD_SETMODE_H_FREQUENCY_4_HZ     =  0x2334 # Measurement: periodic 4 mps, high repeatability
SHT3X_CMD_SETMODE_M_FREQUENCY_4_HZ     =  0x2322 # Measurement: periodic 4 mps, medium repeatability
SHT3X_CMD_SETMODE_L_FREQUENCY_4_HZ     =  0x2329 # Measurement: periodic 4 mps, low repeatability
SHT3X_CMD_SETMODE_H_FREQUENCY_10_HZ    =  0x2737 # Measurement: periodic 10 mps, high repeatability
SHT3X_CMD_SETMODE_M_FREQUENCY_10_HZ    =  0x2721 # Measurement: periodic 10 mps, medium
SHT3X_CMD_SETMODE_L_FREQUENCY_10_HZ    =  0x272A # Measurement: periodic 10 mps, low repeatability
SHT3X_CMD_GETDATA                      =  0xE000 # Readout measurements for periodic mode

SHT3X_CMD_STOP_PERIODIC_ACQUISITION_MODE = 0x3093
SHT3X_CMD_SOFT_RESET                     = 0x30A2 # Soft reset
SHT3X_CMD_HEATER_ENABLE                  = 0x306D # Enabled heater
SHT3X_CMD_HEATER_DISABLE                 = 0x3066 # Disable heater
SHT3X_CMD_READ_STATUS_REG                = 0xF32D # Read status register
SHT3X_CMD_CLEAR_STATUS_REG               = 0x3041 # Clear status register

SHT3X_CMD_READ_HIGH_ALERT_LIMIT_SET      = 0xE11F # Read alert limits, high set
SHT3X_CMD_READ_HIGH_ALERT_LIMIT_CLEAR    = 0xE114 # Read alert limits, high clear
SHT3X_CMD_READ_LOW_ALERT_LIMIT_CLEAR     = 0xE109 # Read alert limits, low clear
SHT3X_CMD_READ_LOW_ALERT_LIMIT_SET       = 0xE102 # Read alert limits, low set
SHT3X_CMD_WRITE_HIGH_ALERT_LIMIT_SET     = 0x611D # Write alert limits, high set
SHT3X_CMD_WRITE_HIGH_ALERT_LIMIT_CLEAR   = 0x6116 # Write alert limits, high clear
SHT3X_CMD_WRITE_LOW_ALERT_LIMIT_CLEAR    = 0x610B # Write alert limits, low clear
SHT3X_CMD_WRITE_LOW_ALERT_LIMIT_SET      = 0x6100 # Write alert limits, low set

MODE_PERIODIC = 0 # cycle measurement mode
MODE_ONE_SHOT = 1 # single measurement mode

# There are 3 repeatabilities to choose: low, medium and high. The higher repeatability, the more accurate data.
REPEATABILITY_HIGH   = 0 # In high repeatability mode, the humidity repeatability is 0.10%RH, the temperature repeatability is 0.06°C*/
REPEATABILITY_MEDIUM = 1 # In medium repeatability mode, the humidity repeatability is 0.15%RH, the temperature repeatability is 0.12°C*/
REPEATABILITY_LOW    = 2 # In low repeatability mode, the humidity repeatability is0.25%RH, the temperature repeatability is 0.24°C*/

MEASUREFREQ_HZ5 = 0 # 0.5 Hz
MEASUREFREQ_1HZ = 1
MEASUREFREQ_2HZ = 2
MEASUREFREQ_4HZ = 3
MEASUREFREQ_10HZ = 4

class ShtError( Exception ):
	pass

class CrcError( ShtError ):
	pass

class CmdError( ShtError ):
	""" Issued when the last command returns an error """
	pass

class NotReady( ShtError ):
	""" Data not yet ready in Periodic acquisition mode """
	pass

class StatusRegister:
	# Container class for the SHT register
	def __init__(self):
		self.reset()

	def reset( self ):
		""" Reset registers to default values """
		# See status_register.txt in /docs
		self.writeDataChecksumStatus = True # True: Last write failed (invalid CRC)
		self.commandStatus = True           # True = Last command error
		self.reserved0 = 2                  # Bit 2-3
		self.systemResetDetected = True		# Reset detected (Hard, Soft, supply fail)
		self.reserved1 = 5                  # Bit 0-9
		self.temperatureAlert = True
		self.humidityAlert = True
		self.reserved2 = True
		self.heaterStatus = True			# Heater is On or Off
		self.reserved3 = True
		self.alertPendingStatus = True

	def decode( self, data ):
		""" data is the resulting buffer for SHT3X_CMD_READ_STATUS_REG """
		self.reset() # re-init values
		val = (data[0]<<8) | data[1]
		self.writeDataChecksumStatus = (val & 1) > 0
		self.commandStatus = (val & 2) > 0
		self.systemResetDetected = (val & 16) > 0
		self.temperatureAlert = (val & 1024) > 0
		self.humidityAlert = (val & 2048) > 0
		self.heaterStatus = (val & 8192) > 0
		self.alertPendingStatus = (val & 32768) > 0

class SHT3x:
	""" Driver to read the SHT3x temperature and humidity sensor """
	def __init__( self, i2c, address=0x45 ):
		self.i2c = i2c
		self.address = address
		self.status_reg = StatusRegister()
		self.buf2 = bytearray( 2 )
		self.buf3 = bytearray( 3 ) # 2 bytes + 1 CRC
		self.buf6 = bytearray( 6 )

		self.measurement_mode = MODE_ONE_SHOT

		self._temp = None # Last converted temp
		self._rh   = None # Last converted humidity


	def write_command( self, cmd ):
		# 0x3780 -> bytes( [0x37, 0x80] )
		sleep_ms(1)
		self.i2c.writeto( self.address, struct.pack( ">H", cmd ) )

	def check_crc( self, data ):
		crc = 0xFF
		""" compute CRC of 2 bytes in the data buffer """
		for data_counter in range(2): # 0..1
			crc = crc ^ data[data_counter]
			for bit in range(8): # 0..7
				if (crc & 0x80) == 0x80:
					crc = ((crc << 1) & 0xFF) ^ 0x31
				else:
					crc = (crc << 1) & 0xFF # keept only 8 bits
		return crc

	@property
	def is_periodic( self ):
		""" Is periodic measurement mode ? or one-shot mode """
		return self.measurement_mode == MODE_PERIODIC

	@property
	def serial_number( self ):
		""" Read the serial number """
		self.write_command( SHT3X_CMD_READ_SERIAL_NUMBER )
		sleep_ms( 1 )
		self.i2c.readfrom_into( self.address, self.buf6 )
		if self.check_crc(self.buf6[0:2]) != self.buf6[2]:
			raise CrcError()
		if self.check_crc(self.buf6[3:5]) != self.buf6[5]:
			raise CrcError()
		r = self.buf6[0]
		r = (r << 8) | self.buf6[1]
		r = (r << 8) | self.buf6[3]
		r = (r << 8) | self.buf6[4]
		return r

	def update_status_reg( self, check_cmd_error=False ):
		""" Reread status register and update self.status_reg """
		retry = 10
		while retry > 0:
			self.write_command( SHT3X_CMD_READ_STATUS_REG )
			sleep_ms(1)
			self.i2c.readfrom_into( self.address, self.buf3 )
			if self.check_crc(self.buf3[0:2]) == self.buf3[2] :
		 		break # Great a Correct CRC
			retry -= 1

		if retry == 0:
			raise CrcError('fails to read status!')

		self.status_reg.decode( self.buf3 )
		if check_cmd_error:
			if self.status_reg.commandStatus == True:
				raise CmdError('Last command not processed!')

	def clear_status_reg( self ):
		""" Clear the status register on the SHT """
		self.write_command( SHT3X_CMD_CLEAR_STATUS_REG )
		sleep_ms( 10 )

	@property
	def alert_state( self ):
		""" Check if an alert was raised for Temperature or humidity """
		sleep_ms( 1 )
		self.update_status_reg()
		return self.status_reg.humidityAlert or self.status_reg.temperatureAlert


	def soft_reset( self ):
		self.write_command( SHT3X_CMD_SOFT_RESET )
		sleep_ms(1)
		self.update_status_reg( check_cmd_error=True ) # Update status_reg

		return  self.status_reg.systemResetDetected

	def pin_reset( self ):
		""" Perform an hadware reset """
		raise  NotImplementedError

	def heater( self, enabled=None ):
		""" change the heather status or read its state (when enabled=None). """
		if enabled==True:
			self.write_command( SHT3X_CMD_HEATER_ENABLE )
		elif enabled==False:
			self.write_command( SHT3X_CMD_HEATER_DISABLE )
		sleep_ms(1)
		self.update_status_reg( check_cmd_error=True )

		return self.status_reg.heaterStatus

	def _convert_temp( self, data ):
		r = (data[0] << 8) | data[1]
		return ((175.0 * r) / 65535.0) - 45.0

	def _convert_rh( self, data ):
		r = data[0]
		r = (r << 8) | data[1]
		return 100.0 * (r / 65535.0)

	def read_all( self, repeatability ):
		""" Read temperature and humidity """
		if repeatability==REPEATABILITY_HIGH:
			self.write_command( SHT3X_CMD_GETDATA_H_CLOCKENABLED )
		elif repeatability==REPEATABILITY_MEDIUM:
			self.write_command(SHT3X_CMD_GETDATA_M_CLOCKENABLED)
		elif repeatability==REPEATABILITY_LOW:
			self.write_command(SHT3X_CMD_GETDATA_L_CLOCKENABLED)
		elif self.is_periodic: # Read the data in periodic mode
			self.write_command( SHT3X_CMD_FETCH_DATA )

		sleep_ms(15)
		try:
			self.i2c.readfrom_into( self.address, self.buf6 )
		except OSError as err:
			# Asking to early in periodic capture will conduct
			# to ENODEV error (errcode 19)
			if (19 in err.args) and (self.is_periodic):
				raise NotReady()
			else:
				raise # reraise error

		# Temp
		if self.check_crc( self.buf6[0:2] ) != self.buf6[2]:
			raise CrcError()
		# Humidity
		if self.check_crc( self.buf6[3:5] ) != self.buf6[5]:
			raise CrcError()

		self._temp = self._convert_temp( self.buf6[0:2] )
		self._rh   = self._convert_rh( self.buf6[3:5] )
		return (self._temp, self._rh)

	@property
	def temperature( self ):
		""" Just read temperature. Use tmp_rh to obtain both data in one
		    operation (needed for periodic read) """
		if self.measurement_mode == MODE_ONE_SHOT:
			self.read_all(REPEATABILITY_HIGH)
		else:
			self.read_all( None ) # Just Fetch Data (in PERIODIC_MODE)
		return self._temp

	@property
	def humidity( self ):
		""" Just read Humidity. Use tmp_rh to obtain both data in one
		    operation (needed for periodic read) """
		if self.measurement_mode == MODE_ONE_SHOT:
			self.read_all(REPEATABILITY_HIGH)
		else:
			self.read_all( None ) # Just Fetch Data (in PERIODIC_MODE)
		return self._rh

	@property
	def tmp_rh( self ):
		""" Return temperature & relative Humidity in one pass """
		if self.measurement_mode == MODE_ONE_SHOT:
			return self.read_all(REPEATABILITY_HIGH)
		else:
			return self.read_all( None ) # Just Fetch Data (in PERIODIC_MODE)


	def start_periodic_mode( self, measure_freq, repeatability ):
		assert measure_freq in (MEASUREFREQ_HZ5, MEASUREFREQ_1HZ, MEASUREFREQ_2HZ, MEASUREFREQ_4HZ, MEASUREFREQ_10HZ)
		assert repeatability in (REPEATABILITY_HIGH, REPEATABILITY_MEDIUM, REPEATABILITY_LOW)
		# cmd[5][3]
		cmd = [ [SHT3X_CMD_SETMODE_H_FREQUENCY_HALF_HZ,SHT3X_CMD_SETMODE_M_FREQUENCY_HALF_HZ,SHT3X_CMD_SETMODE_L_FREQUENCY_HALF_HZ],
				[SHT3X_CMD_SETMODE_H_FREQUENCY_1_HZ,SHT3X_CMD_SETMODE_M_FREQUENCY_1_HZ,SHT3X_CMD_SETMODE_L_FREQUENCY_1_HZ],
				[SHT3X_CMD_SETMODE_H_FREQUENCY_2_HZ,SHT3X_CMD_SETMODE_M_FREQUENCY_2_HZ,SHT3X_CMD_SETMODE_L_FREQUENCY_2_HZ],
				[SHT3X_CMD_SETMODE_H_FREQUENCY_4_HZ,SHT3X_CMD_SETMODE_M_FREQUENCY_4_HZ,SHT3X_CMD_SETMODE_L_FREQUENCY_4_HZ],
				[SHT3X_CMD_SETMODE_H_FREQUENCY_10_HZ,SHT3X_CMD_SETMODE_M_FREQUENCY_10_HZ,SHT3X_CMD_SETMODE_L_FREQUENCY_10_HZ ] ]
		self.measurement_mode = MODE_PERIODIC
		self.write_command( cmd[measure_freq][repeatability] )
		sleep_ms( 1 )
		self.update_status_reg( check_cmd_error=True )
		return True

	def stop_periodic_mode( self ):
		self.measurement_mode = MODE_ONE_SHOT
		self.write_command( SHT3X_CMD_STOP_PERIODIC_ACQUISITION_MODE )
		sleep_ms(1)
		self.update_status_reg( check_cmd_error=True )
		return True
