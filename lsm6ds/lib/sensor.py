#
# Ported from Adafruit_Sensor
#
# see https://github.com/adafruit/Adafruit_Sensor/blob/master/Adafruit_Sensor.h

from micropython import const

# Not ported to Python:
# sensors_vec_t
# sensors_color_t 

# Constants
SENSORS_GRAVITY_EARTH = 9.80665 # Earth's gravity in m/s^2
SENSORS_GRAVITY_MOON  = 1.6     # The moon's gravity in m/s^2
SENSORS_GRAVITY_SUN   = 275.0   # The sun's gravity in m/s^2
SENSORS_GRAVITY_STANDARD = SENSORS_GRAVITY_EARTH
SENSORS_MAGFIELD_EARTH_MAX = 60.0 # Maximum magnetic field on Earth's surface
SENSORS_MAGFIELD_EARTH_MIN = 30.0 # Minimum magnetic field on Earth's surface
SENSORS_PRESSURE_SEALEVELHPA = 1013.25 # Average sea level pressure is 1013.25 hPa
SENSORS_DPS_TO_RADS = 0.017453293 # Degrees/s to rad/s multiplier
SENSORS_RADS_TO_DPS = 57.29577793 # Rad/s to degrees/s  multiplier
SENSORS_GAUSS_TO_MICROTESLA = const(100) # Gauss to micro-Tesla multiplier


# Sensor Types
SENSOR_TYPE_ACCELEROMETER = const(1) # Gravity + linear acceleration
SENSOR_TYPE_MAGNETIC_FIELD = const(2)
SENSOR_TYPE_ORIENTATION = const(3)
SENSOR_TYPE_GYROSCOPE = const(4)
SENSOR_TYPE_LIGHT = const(5)
SENSOR_TYPE_PRESSURE = const(6)
SENSOR_TYPE_PROXIMITY = const(8)
SENSOR_TYPE_GRAVITY = const(9)
SENSOR_TYPE_LINEAR_ACCELERATION = const(10) # Acceleration not including gravity
SENSOR_TYPE_ROTATION_VECTOR = const(11)
SENSOR_TYPE_RELATIVE_HUMIDITY = const(12)
SENSOR_TYPE_AMBIENT_TEMPERATURE = const(13)
SENSOR_TYPE_OBJECT_TEMPERATURE = const(14)
SENSOR_TYPE_VOLTAGE = const(15)
SENSOR_TYPE_CURRENT = const(16)
SENSOR_TYPE_COLOR = const(17)
SENSOR_TYPE_TVOC = const(18)
SENSOR_TYPE_VOC_INDEX = const(19)
SENSOR_TYPE_NOX_INDEX = const(20)
SENSOR_TYPE_CO2 = const(21)
SENSOR_TYPE_ECO2 = const(22)
SENSOR_TYPE_PM10_STD = const(23)
SENSOR_TYPE_PM25_STD = const(24)
SENSOR_TYPE_PM100_STD = const(25)
SENSOR_TYPE_PM10_ENV = const(26)
SENSOR_TYPE_PM25_ENV = const(27)
SENSOR_TYPE_PM100_ENV = const(28)
SENSOR_TYPE_GAS_RESISTANCE = const(29)
SENSOR_TYPE_UNITLESS_PERCENT = const(30)
SENSOR_TYPE_ALTITUDE = const(31)


class SensorT: # sensor_t
	""" Sensor details : structure used to describe basic information about a specific sensor. """
	def __init__( self ):
		self.clear()

	def clear( self ):
		self.name      = "Undefined" # sensor name (12 chars)
		self.version   = -1 # version of the hardware + driver 
		self.sensor_id = -1 # unique sensor identifier 
		self.type      = -1 # this sensor's type (ex. SENSOR_TYPE_LIGHT) 
		self.max_value = 0  # float, maximum value of this sensor's value in SI units
		self.min_value = 0  # float. minimum value of this sensor's value in SI units
		self.resolution= 0  # float. smallest difference between two values reported by this sensor
		self.min_delay = 0  # float. minimum delay in microseconds between events. zero = not a constant rate


class Vector3DAdapter:
	def __init__( self, owner ):
		self.owner = owner

	@property
	def x( self ):
		return self.owner.data[0]

	@x.setter
	def x( self, value ):
		self.owner.data[0] = value

	@property
	def y( self ):
		return self.owner.data[1]

	@y.setter
	def y( self, value ):
		self.owner.data[1] = value

	@property
	def z( self ):
		return self.owner.data[2]

	@z.setter
	def z( self, value ):
		self.owner.data[2] = value

class SensorEvent: 
	""" Equivalent of sensors_event_t """
	def __init__(self):
		self.data = [0.0, 0.0, 0.0, 0.0]
		self.clear()
		self.__acc = None # Acceleration 3DVector Adapter
		self.__mag = None # Magnetic 3DVector Adapter
		self.__gyro= None # Gyroscope 3DVector Adapter
		self.__orientation = None

	def clear( self ):
		self.version   = 0 
		self.sensor_id = 0 #  unique sensor identifier 
		self.type      = -1 # sensor type
		self.reserved0 = 0 # reserved 
		self.timestamp = 0 # time is in milliseconds 
		self.data[0] = 0.0
		self.data[1] = 0.0
		self.data[2] = 0.0
		self.data[3] = 0.0 # Raw data 
		
	@property
	def acceleration( self ): 
		""" Returns the data as an acceleration vector  
		   sensors_vec_t : acceleration values are in meter per second per second (m/s^2) """
		if self.__acc == None:
			self.__acc = Vector3DAdapter( self )
		return self.__acc

	@property
	def magnetic( self ):
		""" Returns the data as an  magnetic vector values are in micro-Tesla (uT)
		    sensors_vec_t """
		if self.__mag == None:
			self.__mag = Vector3DAdaoter( self )
		return self.__mag

	@property
	def orientation( self ):
		""" Returns the data as an orientation values are in degrees
		    sensors_vec_t """
		if self.__orientation == None:
			self.__orientation = Vector3DAdapter( self )
		return self.__orientation

	@property
	def gyro( self ):
	        """ Returns the data as  gyroscope values are in rad/s. 
		    sensors_vec_t """
		if self.__gyro == None:
			self.__gyro = Vector3DAdapter( self )
		return self.__gyro

	@property
	def temperature( self ):
		"""  temperature is in degrees centigrade (Celsius, float) """
		return self.data[0]

	@temperature.setter
	def temperature( self, value ):
		self.data[0] = value

	@property
	def distance( self ):
		""" distance in centimeters (float) """
		return self.data[0]

	@property
	def light( self ):
		""" light in SI lux units (float)"""
		return self.data[0]

	@property
	def pressure( self ):
		""" light in SI lux units (float) """
		return self.data[0]

	@property
	def relative_humidity( self ):
		""" relative humidity in percent (float) """
		return self.data[0]

	@property
	def current( self ):
		""" current in milliamps (mA, float) """
		return self.data[0]

	@property
	def voltage( self ):
		""" voltage in volts (V, float) """
		return self.data[0]

	@property
	def tvoc( self ):
		""" Total Volatile Organic Compounds, in ppb (float) """
		return self.data[0]

	@property
	def voc_index( self ):
		""" VOC (Volatile Organic Compound) index where 100 is normal (unitless, float) """
		return self.data[0]

	@property
	def nox_index( self ): 
		"""  NOx (Nitrogen Oxides) index where 1 is normal (unitless, float) """
		return self.data[0]

	@property 
	def CO2( self ):
		""" Measured CO2 in parts per million (ppm, float) """
		return self.data[0]

	@property
	def eCO2( self ):
		""" equivalent/estimated CO2 in parts per million (ppm estimated from some other measurement, float) """
		return self.data[0]

	@property
	def pm10_std( self ):
		""" Standard Particulate Matter <=1.0 in parts per million (ppm,float) """
		return self.data[0]

	@property 
	def pm25_std( self ):
		""" Standard Particulate Matter <=2.5 in parts per million (ppm,float) """
		return self.data[0]

	@property
	def pm100_std( self ):
		""" Standard Particulate Matter <=10.0 in parts per million (ppm,float) """
		return self.data[0]

	@property
	def pm10_env( self ):
		""" Environmental Particulate Matter <=1.0 in parts per million (ppm, float) """
		return self.data[0]

	@property 
	def pm25_env( self ):
		""" Environmental Particulate Matter <=2.5 in parts per million (ppm, float) """
		return self.data[0]

	@property
	def pm100_env( self ):
		""" Environmental Particulate Matter <=10.0 in parts per million (ppm, float) """
		return self.data[0]

	@property
	def gas_resistance( self ):
		""" Proportional to the amount of VOC particles in the air (Ohms, float) """
		return self.data[0]

	@property 
	def unitless_percent( self ):
		""" Percentage, unit-less (%, float) """
		return self.data[0]

	@property
	def color( self ):
		"""  color in RGB component values (sensors_color_t) """
		raise NotImplementedError
		return None

	@property
	def altitude( self ):
		""" Distance between a reference datum and a point or object, in meters (float). """
		return self.data[0]


class Sensor:
        def __init__( self, parent ):
		""" Reference to a parent objet """
                self.parent = parent 

	def get_event( self, sensor_event ):
		""" MUST BE OVERRIDE BY DESCENDANT """
		return 0

	def get_sensor( self, sensor_t ):
		""" MUST BE OVERRIDE BY DESCENDANT """
		return 0

	def print_sensor_details( self ):
		sensor = SensorT()
		self.get_sensor( sensor )
		print( "------------------------------------" )
		print( "Sensor: %s" % sensor.name )
		if sensor.type == SENSOR_TYPE_ACCELEROMETER:
		        label = "Acceleration (m/s2)"
		elif sensor.type == SENSOR_TYPE_MAGNETIC_FIELD:
		        label = "Magnetic (uT)"
		elif sensor.type == SENSOR_TYPE_ORIENTATION:
		        label = "Orientation (degrees)"
		elif sensor.type == SENSOR_TYPE_GYROSCOPE:
		        label = "Gyroscopic (rad/s)"
		elif sensor.type == SENSOR_TYPE_LIGHT:
		        label = "Light (lux)"
		elif sensor.type == SENSOR_TYPE_PRESSURE:
		        label = "Pressure (hPa)"
		elif sensor.type == SENSOR_TYPE_PROXIMITY:
		        label = "Distance (cm)"
		elif sensor.type == SENSOR_TYPE_GRAVITY:
		        label = "Gravity (m/s2)"
		elif sensor.type == SENSOR_TYPE_LINEAR_ACCELERATION:
		        label = "Linear Acceleration (m/s2)"
		elif sensor.type == SENSOR_TYPE_ROTATION_VECTOR:
		        label = "Rotation vector"
		elif sensor.type == SENSOR_TYPE_RELATIVE_HUMIDITY:
		        label = "Relative Humidity (%)"
		elif sensor.type == SENSOR_TYPE_AMBIENT_TEMPERATURE:
        		label = "Ambient Temp (C)"
		elif sensor.type == SENSOR_TYPE_OBJECT_TEMPERATURE:
		        label = "Object Temp (C)"
		elif sensor.type == SENSOR_TYPE_VOLTAGE:
		        label = "Voltage (V)"
		elif sensor.type == SENSOR_TYPE_CURRENT:
		        label = "Current (mA)"
		elif sensor.type == SENSOR_TYPE_COLOR:
		        label = "Color (RGBA)"
		elif sensor.type == SENSOR_TYPE_TVOC:
		        label = "Total Volatile Organic Compounds (ppb)"
		elif sensor.type == SENSOR_TYPE_VOC_INDEX:
		        label = "Volatile Organic Compounds (Index)"
		elif sensor.type == SENSOR_TYPE_NOX_INDEX:
		        label = "Nitrogen Oxides (Index)"
		elif sensor.type == SENSOR_TYPE_CO2:
		        label = "Carbon Dioxide (ppm)"
		elif sensor.type == SENSOR_TYPE_ECO2:
		        label = "Equivalent/estimated CO2 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM10_STD:
		        label = "Standard Particulate Matter 1.0 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM25_STD:
		        label = "Standard Particulate Matter 2.5 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM100_STD:
		        label = "Standard Particulate Matter 10.0 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM10_ENV:
		        label = "Environmental Particulate Matter 1.0 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM25_ENV:
		        label = "Environmental Particulate Matter 2.5 (ppm)"
		elif sensor.type == SENSOR_TYPE_PM100_ENV:
		        label = "Environmental Particulate Matter 10.0 (ppm)"
		elif sensor.type == SENSOR_TYPE_GAS_RESISTANCE:
		        label = "Gas Resistance (ohms)"
		elif sensor.type == SENSOR_TYPE_UNITLESS_PERCENT:
		        label = "Unitless Percent (%)"
		elif sensor.type == SENSOR_TYPE_ALTITUDE:
		        label = "Altitude (m)"
		else:
			label = "Undefined!"
		print( "Type: %s" % label )

 		print( "Driver Ver: %s" % sensor.version )
		print( "Unique ID: %s" % sensor.sensor_id )
		print( "Min Value: %s" % sensor.min_value )
		print( "Max Value: %s " % sensor.max_value )
		print( "Resolution: %s" % sensor.resolution )
		print( "------------------------------------" )
