# lsm6ds.py - implementation of LSM6DSOX to MicroPython
#
# Ported from Adafruit library for Arduino
# https://github.com/adafruit/Adafruit_LSM6DS 
#
from micropython import const
import time, struct
from sensor import SENSOR_TYPE_AMBIENT_TEMPERATURE, SENSOR_TYPE_ACCELEROMETER, SENSOR_TYPE_GYROSCOPE
from sensor import SENSORS_DPS_TO_RADS, SENSORS_GRAVITY_STANDARD, SensorEvent, Sensor

__version__ = '0.1.0'

LSM6DS_FUNC_CFG_ACCESS = const( 0x1 ) # Enable embedded functions register
LSM6DS_INT1_CTRL  = const( 0x0D ) # Interrupt control for INT 1
LSM6DS_INT2_CTRL  = const( 0x0E ) # Interrupt control for INT 2
LSM6DS_WHOAMI     = const( 0x0F ) # Chip ID register
LSM6DS_CTRL1_XL   = const( 0x10 ) # Main accelerometer config register
LSM6DS_CTRL2_G    = const( 0x11 ) # Main gyro config register
LSM6DS_CTRL3_C    = const( 0x12 ) # Main configuration register
LSM6DS_CTRL8_XL   = const( 0x17 ) # High and low pass for accel
LSM6DS_CTRL10_C   = const( 0x19 ) # Main configuration register
LSM6DS_WAKEUP_SRC = const( 0x1B ) # Why we woke up
LSM6DS_STATUS_REG = const( 0X1E ) # Status register
LSM6DS_OUT_TEMP_L = const( 0x20 ) # First data register (temperature low)
LSM6DS_OUTX_L_G   = const( 0x22 ) # First gyro data register
LSM6DS_OUTX_L_A   = const( 0x28 ) # First accel data register
LSM6DS_STEPCOUNTER= const( 0x4B ) # 16-bit step counter
LSM6DS_TAP_CFG    = const( 0x58 ) # Tap/pedometer configuration
LSM6DS_WAKEUP_THS = const( 0x5B ) # Single and double-tap function threshold register
LSM6DS_WAKEUP_DUR = const( 0x5C ) # Free-fall, wakeup, timestamp and sleep mode duration
LSM6DS_MD1_CFG    = const( 0x5E ) # Functions routing on INT1 register

# lsm6ds_data_rate_t
LSM6DS_RATE_SHUTDOWN = const(0)
LSM6DS_RATE_12_5_HZ  = const(1)
LSM6DS_RATE_26_HZ    = const(2)
LSM6DS_RATE_52_HZ    = const(3)
LSM6DS_RATE_104_HZ   = const(4)
LSM6DS_RATE_208_HZ   = const(5)
LSM6DS_RATE_416_HZ   = const(6)
LSM6DS_RATE_833_HZ   = const(7)
LSM6DS_RATE_1_66K_HZ = const(8)
LSM6DS_RATE_3_33K_HZ = const(9)
LSM6DS_RATE_6_66K_HZ = const(10)

# lsm6ds_accel_range_t
LSM6DS_ACCEL_RANGE_2_G = const(0)
LSM6DS_ACCEL_RANGE_16_G= const(1)
LSM6DS_ACCEL_RANGE_4_G = const(2)
LSM6DS_ACCEL_RANGE_8_G = const(3)

# lsm6ds_gyro_range_t
LSM6DS_GYRO_RANGE_125_DPS  = const(0b0010)
LSM6DS_GYRO_RANGE_250_DPS  = const(0b0000)
LSM6DS_GYRO_RANGE_500_DPS  = const(0b0100)
LSM6DS_GYRO_RANGE_1000_DPS = const(0b1000)
LSM6DS_GYRO_RANGE_2000_DPS = const(0b1100)
ISM330DHCX_GYRO_RANGE_4000_DPS = const(0b0001)

# lsm6ds_hp_filter_t
LSM6DS_HPF_ODR_DIV_50  = const(0)
LSM6DS_HPF_ODR_DIV_100 = const(1)
LSM6DS_HPF_ODR_DIV_9   = const(2)
LSM6DS_HPF_ODR_DIV_400 = const(3)

class LSM6DS_ERROR( Exception ):
	pass

class LSM6DS_Temp( Sensor ):
	def __init__( self, lsm_parent ):
		super().__init__( lsm_parent )
		self._sensor_id = 0x6D0

	@property
	def lsm_parent( self ):
		return self.parent

	def get_event( self, event ):
		# event: sensors_event_t
                self.lsm_parent._read() 
                self.lsm_parent.fill_temp_event( event, time.ticks_ms() )

	def get_sensor( self, sensor ):
		# sensor : sensor_t
		sensor.clear()

		sensor.name = "LSM6DS_T"
		sensor.version = 1
		sensor.sensor_id = self._sensor_id
		sensor.type = SENSOR_TYPE_AMBIENT_TEMPERATURE
		sensor.min_delay = 0
		sensor.min_value = -40
		sensor.max_value = 85
		sensor.resolution = 1 # not a great sensor 


class LSM6DS_Accelerometer( Sensor ):
        def __init__( self, lsm_parent ):
                super().__init__( lsm_parent )
                self._sensor_id = 0x6D1

        def get_event( self, event ): 
                # event: sensors_event_t
		self.lsm_parent._read()
		self.lsm_parent.fill_accel_event( event, time.ticks_ms() )

        def get_sensor( self, sensor ):
                # sensor : sensor_t
		sensor.clear()

		sensor.name = "LSM6DS_A"
		sensor.version = 1
		sensor.sensor_id = self._sensor_id
		sensor.type = SENSOR_TYPE_ACCELEROMETER
		sensor.min_delay = 0
		sensor.min_value = -156.9064 #  -16g = 156.9064 m/s^2
		sensor.max_value = 156.9064  # 16g = 156.9064 m/s^2
		sensor.resolution = 0.061    # 0.061 mg/LSB at +-2g


class LSM6DS_Gyro( Sensor ):
        def __init__( self, lsm_parent ):
                super().__init__( lsm_parent )
                self._sensor_id = 0x6D2

        def get_event( self, event ): 
                # event: sensors_event_t
                self.lsm_parent._read()
		self.lsm_parent.fill_gyro_event( event, time.ticks_ms() )

        def get_sensor( self, sensor ):
                # sennsor : sensor_t
                sensor.clear()
		sensor.name =  "LSM6DS_G"
		sensor.version = 1
		sensor.sensor_id = self._sensor_id
		sensor.type = SENSOR_TYPE_GYROSCOPE
		sensor.min_delay = 0
		sensor.min_value = -34.91 # -2000 dps -> rad/s (radians per second) 
		sensor.max_value = +34.91
		sensor.resolution = 7.6358e-5  # 4.375 mdps -> rad/s 

class LSM6DS:
	def __init__( self, i2c, address, whoami ):
		self.i2c = i2c
		self.addr = address
		self.whoami = whoami # The expected CHIP_ID to be read
		self.accel_range_buffered = None
		self.gyro_range_buffered = None

		self.accel_addr = None
                self.gyro_addr  = None
                self.temp_addr  = None

		self.temperature_sensitivity = 256.0 # Temp sensor sensitivity in LSB/degC
		self.temp_sensor = None
		self.gyro_sensor = None
		self.accel_sensor= None
		
		# _read storage of data 
		self.gyroX = None
		self.gyroY = None
		self.gyroZ = None
		self.accX  = None
		self.accY  = None
		self.accZ  = None
		self.temperature = None

		self.buf1 = bytearray(1)
		self.buf14 = bytearray(14)

		# see Adafruit_LSM6DS.h for more
		self._init( address )

	def _init( self, address ):
		# Enable accelerometer with 104 Hz data rate, 4G
		self.set_accel_datarate(LSM6DS_RATE_104_HZ)
		self.set_accel_range(LSM6DS_ACCEL_RANGE_4_G)

		# Enable gyro with 104 Hz data rate, 2000 dps
		self.set_gyro_datarate(LSM6DS_RATE_104_HZ)
		self.set_gyro_range(LSM6DS_GYRO_RANGE_2000_DPS)

		time.sleep_ms(10)

		# delete objects if sensor is reinitialized
		if self.temp_sensor != None:
			del (self.temp_sensor)
		if self.accel_sensor != None:
			del( self.accel_sensor)
		if self.gyro_sensor!=None:
			del( self.gyro_sensor)

		self.temp_sensor = LSM6DS_Temp(self)
		self.accel_sensor = LSM6DS_Accelerometer(self)
		self.gyro_sensor = LSM6DS_Gyro(self)

		return False

	def _read( self ):
		# get raw readings
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_OUT_TEMP_L, self.buf14 )
		rawTemp,rawGyroX,rawGyroY,rawGyroZ,rawAccX,rawAccY,rawAccZ = struct.unpack( '<hhhhhhh', self.buf14 ) # signed int16
		self.temperature = (rawTemp / self.temperature_sensitivity) + 25.0

		gyro_scale = 1 # range is in milli-dps per bit!
		if self.gyro_range_buffered==ISM330DHCX_GYRO_RANGE_4000_DPS:
			gyro_scale = 140.0
		elif self.gyro_range_buffered==LSM6DS_GYRO_RANGE_2000_DPS:
			gyro_scale = 70.0
		elif self.gyro_range_buffered==LSM6DS_GYRO_RANGE_1000_DPS:
			gyro_scale = 35.0
		elif self.gyro_range_buffered==LSM6DS_GYRO_RANGE_500_DPS:
			gyro_scale = 17.50
		elif self.gyro_range_buffered==LSM6DS_GYRO_RANGE_250_DPS:
			gyro_scale = 8.75
		elif self.gyro_range_buffered==LSM6DS_GYRO_RANGE_125_DPS:
			gyro_scale = 4.375

		self.gyroX = rawGyroX * gyro_scale * SENSORS_DPS_TO_RADS / 1000.0
		self.gyroY = rawGyroY * gyro_scale * SENSORS_DPS_TO_RADS / 1000.0
		self.gyroZ = rawGyroZ * gyro_scale * SENSORS_DPS_TO_RADS / 1000.0

		accel_scale = 1 # range is in milli-g per bit!
		if self.accel_range_buffered==LSM6DS_ACCEL_RANGE_16_G:
			accel_scale = 0.488
		elif self.accel_range_buffered==LSM6DS_ACCEL_RANGE_8_G:
			accel_scale = 0.244
		elif self.accel_range_buffered==LSM6DS_ACCEL_RANGE_4_G:
			accel_scale = 0.122
		elif self.accel_range_buffered==LSM6DS_ACCEL_RANGE_2_G:
			accel_scale = 0.061

		self.accX = rawAccX * accel_scale * SENSORS_GRAVITY_STANDARD / 1000
		self.accY = rawAccY * accel_scale * SENSORS_GRAVITY_STANDARD / 1000
		self.accZ = rawAccZ * accel_scale * SENSORS_GRAVITY_STANDARD / 1000


	def reset( self ):
		""" Software reset """
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL3_C, self.buf1 )
		value = self.buf1[0] | 0b00000001 # Set the reset bit
		self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL3_C, self.buf1 )

		# Wait the component to switch off its reset bit
		while (value & 0b00000001)==0b00000001:
			time.sleep_ms(1)
                	self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL3_C, self.buf1 )
                	value = self.buf1[0] & 0b00000001 # read the reset bit

	def chip_id( self ):
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_WHOAMI, self.buf1 )
		return self.buf1[0]

	def set_accel_datarate( self, data_rate ):
		# One of the LSM6DS_RATE_xxx constant
		# see lsm6ds_data_rate_t in Arduino lib
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL1_XL, self.buf1 )
		val = self.buf1[0] & 0x0F
		self.buf1[0] = val | (data_rate<<4)
		self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL1_XL, self.buf1 )

	def get_accel_datarate( self ):
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL1_XL, self.buf1 )
		val = self.buf1[0] & 0xF0
		return val>>4

	def set_accel_range( self, new_range ):
		# One of the LSM6DS_ACCEL_RANGE_xxx constant
		# see lsm6ds_accel_range_t in Arduino lib
                self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL1_XL, self.buf1 )
                val = self.buf1[0] & 0b11110011
                self.buf1[0] = val | (new_range<<2)
                self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL1_XL, self.buf1 )
		self.accel_range_buffered = new_range

	def get_accel_range( self ):
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL1_XL, self.buf1 )
		val = self.buf1[0] & 0b00001100
		return val >> 2

        def set_gyro_datarate( self, data_rate ):
                # One of the LSM6DS_RATE_xxx constant
                # see lsm6ds_data_rate_t in Arduino lib
                self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL2_G, self.buf1 )
                val = self.buf1[0] & 0x0F
                self.buf1[0] = val | (data_rate<<4)
                self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL2_G, self.buf1 )

	def get_gyro_datarate( self ):
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL2_G, self.buf1 ) 
		val = self.buf1[0] & 0xF0
		return val >> 4

        def set_gyro_range( self, new_range ):
                # One of the LSM6DS_GYRO_RANGE_xxx constant
                # see lsm6ds_gyro_range_t in Arduino lib
                self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL2_G, self.buf1 )
                val = self.buf1[0] & 0xF0
                self.buf1[0] = val | new_range
                self.i2c.writeto_mem( self.addr,  LSM6DS_CTRL2_G, self.buf1 )
                self.gyro_range_buffered = new_range

	def get_gyro_range( self ):
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_CTRL2_G, self.buf1 )
		val = self.buf1[0] & 0x0F
		return val

	def config_int1 ( self, drdy_temp, drdy_g, drdy_xl, step_detect=False, wakeup=False ):
		""" Enables and disables the data ready interrupt on INT 1. """
		# drdy_temp : true to output the data ready temperature interrupt
		# drdy_g : true to output the data ready gyro interrupt
		# drdy_xl : true to output the data ready accelerometer interrupt
		# step_detect : true to output the step detection interrupt (default off)
		# wakeup : true to output the wake up interrupt (default off)
		
		# Ensure we have binary value
		drdy_temp = 0b1 if drdy_temp else 0b0
		drdy_g = 0b1 if drdy_g else 0b0
		drdy_xl = 0b1 if drdy_xl else 0b0
		step_detect = 0b1 if step_detect else 0b0
		wakeup = 0b1 if wakeup else 0b0
		# Update register
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_INT1_CTRL, self.buf1 )
		value = self.buf1[0] & 0b01111000
		self.buf1[0] = value | (step_detect << 7) | (drdy_temp << 2) | (drdy_g << 1) | drdy_xl
		self.i2c.writeto_mem( self.addr, LSM6DS_INT1_CTRL, self.buf1 )

		self.i2c.readfrom_mem_into( self.addr, LSM6DS_MD1_CFG, self.buf1 )
		self.buf1[0] = self.buf1[0] | 0b00100000 # Wake-Up bit
		self.i2c.writeto_mem( self.addr, LSM6DS_MD1_CFG, self.buf1 )

	def config_int2 ( self, drdy_temp, drdy_g, drdy_xl ):
                """ Enables and disables the data ready interrupt on INT 2. """
		# drdy_temp : true to output the data ready temperature interrupt
		# drdy_g : true to output the data ready gyro interrupt
		# drdy_xl : true to output the data ready accelerometer interrupt

		# Ensure we have binary value
		drdy_temp = 0b1 if drdy_temp else 0b0
		drdy_g = 0b1 if drdy_g else 0b0
		drdy_xl = 0b1 if drdy_xl else 0b0

		# Update register
		self.i2c.readfrom_mem_into( self.addr, LSM6DS_INT2_CTRL, self.buf1 )
		value = self.buf1[0] & 0b11111000
		self.buf1[0] = value | (drdy_temp << 2) | (drdy_g << 1) | drdy_xl
		self.i2c.writeto_mem( self.addr, LSM6DS_INT2_CTRL, self.buf1 ) 


	def get_event( self, accel, gyro, temp ): # all  sensors_event_t
		t = time.ticks_ms()
		self._read()

		# use helpers to fill in the events
		self.fill_accel_event(accel, t)
		self.fill_gyro_event(gyro, t)
		self.fill_temp_event(temp, t)
		return True


	def fill_temp_event(self, temp, timestamp ): # sensors_event_t
		temp.clear()
		# ?? temp->version = sizeof(sensors_event_t);
		temp.sensor_id = self._sensorid_temp
		temp.type = SENSOR_TYPE_AMBIENT_TEMPERATURE
		temp.timestamp = timestamp
		temp.temperature = self.temperature


	def fill_gyro_event( self, gyro, timestamp):
		gyro.clear()
		gyro.version = 1
		gyro.sensor_id = self._sensorid_gyro
		gyro.type = SENSOR_TYPE_GYROSCOPE
		gyro.timestamp = timestamp
		gyro.gyro.x = self.gyroX
		gyro.gyro.y = self.gyroY
		gyro.gyro.z = self.gyroZ


	def fill_accel_event( self, accel, timestamp):
		accel.clear()
		accel.version = 1
		accel.sensor_id = self._sensorid_accel
		accel.type = SENSOR_TYPE_ACCELEROMETER
		accel.timestamp = timestamp
		accel.acceleration.x = self.accX
		accel.acceleration.y = self.accY
		accel.acceleration.z = self.accZ


LSM6DSOX_CHIP_ID = const(0x6C) # LSM6DSOX default device id from WHOAMI
LSM6DSOX_FUNC_CFG_ACCESS = const(0x1) # Enable embedded functions register
LSM6DSOX_PIN_CTRL = const(0x2) # Pin control register
LSM6DSOX_INT1_CTRL = const(0x0D) # Interrupt enable for data ready
LSM6DSOX_CTRL1_XL = const(0x10) # Main accelerometer config register
LSM6DSOX_CTRL2_G = const(0x11) # Main gyro config register
LSM6DSOX_CTRL3_C = const(0x12) # Main configuration register
LSM6DSOX_CTRL9_XL = const(0x18) # Includes i3c disable bit

LSM6DSOX_MASTER_CONFIG = const(0x14) # I2C Master config; access must be enabled with  bit SHUB_REG_ACCESS
# is set to '1' in FUNC_CFG_ACCESS (01h).

class LSM6DSOX( LSM6DS ):
	def __init__( self, i2c, address, whoami ):
		super().__init__( i2c, address, whoami )

		#see Adafruit_ISM330DHCX.cpp _init() for more


	def _init( self, address ): # Address is sensor_id
		if self.chip_id() != self.whoami:
			raise LSM6DS_ERROR( 'Invalid chip ID %s, %s expected!' % (self.chip_id(), self.whoami) )

		self.accel_addr = address
                self.gyro_addr  = address+1
                self.temp_addr  = address+2

		self.reset()

		# Disable I3C
		self.i2c.readfrom_mem_into( self.addr, LSM6DSOX_CTRL9_XL, self.buf1 )
		self.buf1[0] = self.buf1[0] | 0b00000010
		self.i2c.writeto_mem( self.addr, LSM6DSOX_CTRL9_XL, self.buf1 )

		# call base class _init()
		super()._init( address )

		return True
