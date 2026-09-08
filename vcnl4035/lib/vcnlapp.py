""" vcnlapp.py - MicroPython High level application library for Vishay VCNL4035 Proximity sensor

   REQUIRES breakout board must HAVE VCNL4035 + 3x IR LEDs in order to detect SWIPE.

   * Interrupt Pin must be wired to GP0
   * Green LED on GPIO 25 : toggle/blink while data acquisition
   * Red LED on GPIO 15 : turn ON when data acquisition started and switch OFF when reset

* Source   :  https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

11 Apr 2026 - domeu -creation

 remarks: 
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""

import micropython, time
from machine import Pin
from vcnl4035 import VCNL4035
from vcnldefs import *
from stat import RingStatistic,Statistic,linear_regression
from timetls import TimeoutTimer

# Main Loop debugging
LOOP_DEBUG = False
# Make calc_gesture_recognition displaying debug message
SWIPES_DEBUG = False
# Noise Debugging
NOISE_DEBUG = False
# Make calc_zx_data & orb displaying debug message
ZX_DEBUG = False
# Make cal_gesture_recognition displaying debug message
GESTURE_DEBUG = False # Show calculation result
GESTURE_DATA_DEBUG = False # Show the captured ZX_Data


# Recognized Gesture
GESTURE_NONE = const(0)
GESTURE_PUSH = const(1)
GESTURE_SWIPE_LEFT = const(2)
GESTURE_SWIPE_RIGHT = const(3)

# Gesture flags Structure
class gesture_flags_t():
	def __init__(self):
		# All uint8
		self.noise_canc_enable = True
		self.zx_enable = True
		self.zx_smooth_enable = True
		self.orb_detect_enable = True
		self.gesture_recognition_enable = True
		self.data_ready = True
		self.zx_data_ready = True
		self.orb_data_ready = True
		self.gesture_recognition_data_ready = False
		self.orb_status = True
		self.activity_status = True
		self.orb_data_cnt = 0
		self.orb_data_cnt_limit = 0


# ZX Calculation Coeffecents 
class zx_coeff_t():
	def __init__( self ):
		# all parameter are double precision (8 bytes)
		self.A_1 = 1   # Left  & Right LED
		self.B_1 = 0   #    left_dist = [ (raw[1]+B_1)^k_1 ]*A_1
		self.k_1 = 2   #    right_dist = .. raw[2]
		self.A_2 = -1  # x calculation
		self.k_2 = 0.5   #    x = ( left_dist^k_2 - right_dist^k2 )*A_2
		self.A_3 = 0.001   # Z calculation
		self.B_3 = 0.3   #    [( |x|^k_3 * B_3 ) + left_dist + right_dist ]*A_3
		self.k_3 = 0.5


# Orbital Coordinates 
class orb_cord_t():
	def __init__(self):
		# all int16 (signed)
		self.center_z_max = 40000
		self.center_z_min = 0
		self.center_x_max = 70
		self.center_x_min = -100
		self.side_z_max = 40000
		self.side_z_min = 0
		self.side_x_max = +500
		self.side_x_min = -500
		self.center_IRED_max = 1000 # every value below 1000 will be rejected

# Definition and states related to VCNL4035_App_Swipes.cpp
GESTURE_TIMEOUT_SEC  = 2
GESTURE_COLLECT_SIZE = 20 # Ring Buffer of raw data acquired
class GestureMachine():
	""" Read Statistic & Gesture Buffer are TWO DISTINCT thing """
	STATE_RESET = 0 # Data collection reset (because of time out)
	STATE_COLLECT = 1 # Currently collecting data (not timeout reached,see )
	STATE_COMPUTE = 2 # Gesture detected (must be acquired by user code)

	def __init__( self ):
		self.state = GestureMachine.STATE_RESET
		self.data_points = [] # list of (z,x) points
		self.timeout = TimeoutTimer()
		self.recognized = GESTURE_NONE # last gesture identified by calc_gesture_recognition()

	def clear( self ):
		self.state_machine = GestureMachine.STATE_RESET
		self.data_points.clear()
		# Call reset event

	def append( self, zx ):
		self.timeout.setTimer( GESTURE_TIMEOUT_SEC )
		self.data_points.append( zx )

	def zx_dev( self ):
		# Returns the standard deviation on Z & X
		zstat = Statistic()
		xstat = Statistic()
		for z,x in self.data_points:
			zstat.append(z)
			xstat.append(x)
		return zstat.std_dev, xstat.std_dev

	def regression( self ):
		# return the linear regression on z collection & x collection
		# See vcnl4035-ZX-axis.jpg
		x_values = [x for z,x in self.data_points]
		z_values = [z for z,x in self.data_points]
		indexes  = [i for i in range(len(self.data_points))]
		return linear_regression( indexes, z_values ) + linear_regression( indexes, x_values )

	@property
	def count( self ):
		return len( self.data_points )

		
		

# VCNL4035 Application Modes (VCNL4035_APP_MODES)
APP_ACTIVE = const(0)
APP_SLEEP = const(1)

class VCNL4035Application( VCNL4035 ):
	def __init__( self, i2c, int_pin, address=0x60, mode=VCNL4035_MODES.GESTURE ):
		""" :param int_pin: interrupt Pin, will be reconfigured as Input will Pull_UP """
		super().__init__( i2c, address, mode )
		# Initialize & register IRQ Pin
		self.set_int_pin( int_pin )
		# Last sensor data
		#  update with sensor_data.clear() ; sensor_data.extend( new_data )
		self.sensor_data = [0,0,0] 
		# Noise Variables
		self.gesture_noise = [0,0,0] # uint16
		# Parameter Variables
		self.gesture_flags = gesture_flags_t()
		self.current_mode = None #APP_ACTIVE
		self.prev_mode = None # APP_ACTIVE
		self.gesture_activity_threshold = 0 # uint16
		self.gesture_std_threshold = 25 # Minimum Std Deviation 
		# Callbacks 
		self.on_data_collect  = None # when Gesture data collect
		self.on_start_collect = None # When new data collect starts 
		self.on_reset_collect = None # When data collect get resets
		# Raw VCNL Data
		#  uint16_t sensor_data[3];
		self.left_stat  = RingStatistic( length=5 ) # Statistic()
		self.right_stat = RingStatistic( length=5 ) # Statistic()
		# ZX Related
		self.z_value = 0 # int16
		self.x_value = 0 # int16
		self.zx_coeff = zx_coeff_t()
		self.zx_min_threshold = 0 # uint8
		# Gesture Recognition Related (Used In VCNL_4035_App_Swipes.cpp) */
		self.swipe_speed = 0 # int16
		self.sample_skip = 3 # int
		self.std_trigger = 25 # standard deviation trigger
		#self.gesture_timeout_limit = 1000 # uint16 Not Implemented Yet
		# Orbital Related 
		self.orb_cord = orb_cord_t()
		self.orb_cord_leaving = orb_cord_t()
		self.gesture = GestureMachine()


	# === Operational ===
	def mainloop(self):
		if self.current_mode != self.prev_mode:
			print("switch current_mode to %s" % ("APP_Active" if self.current_mode==APP_ACTIVE else "APP_SLEEP",) )
			if self.current_mode == APP_ACTIVE:
				#self.setGestureMode() # ancestor call
				super().init( VCNL4035_MODES.GESTURE )
				self.set_ps_trigger()   # ancestor call
			else: # APP_SLEEP
				#setPSMode();
				super().init( VCNL4035_MODES.PROXIMITY )
				self.read_int_flags() # ancestor call
			self.prev_mode = self.current_mode

		# Which mainloop to execute ?
		if self.current_mode == APP_ACTIVE:
			self.__active_loop()
		else: # APP_SLEEP
			self.__sleep_loop()

	def __active_loop(self):
		""" Run for APP_ACTIVE mode """
		_data = self.wait_data( timeout_ms = 300 ) # Was 2 sec
		# print( "_data", _data )
		if _data==None:
			# Restart the data collection process
			if LOOP_DEBUG:
				print( "Restart data collect" )
			self.left_stat.clear()
			self.right_stat.clear()
			self.read_int_flags()
			time.sleep_ms(10)
			self.set_ps_trigger()
			return
		# copy the values to sensor_data
		self.sensor_data = [] # need to create an instance
		for item in _data:
			self.sensor_data.append( item )
		if ZX_DEBUG:
			print( "\033[H" ) # Move Home
			print( "___sensor_data", self.sensor_data, "          " )
		# Subtract noise from sensor_data
		if self.gesture_flags.noise_canc_enable:
			self.subtract_gesture_noise()

		# Check if data is in the active range
		a = self.sensor_data[0] > self.gesture_activity_threshold
		b = self.sensor_data[1] > self.gesture_activity_threshold
		c = self.sensor_data[2] > self.gesture_activity_threshold
		self.gesture_flags.activity_status = (a or b or c)

		# Calculate ZX cordinate
		if self.gesture_flags.zx_enable:
			left_data = self.sensor_data[2] # original is [0]
			right_data = self.sensor_data[1] # Original is [2]
			if self.gesture_flags.zx_smooth_enable:
				# Smooth the raw data
				self.left_stat.append( left_data )
				self.right_stat.append( right_data )
				left_data = self.left_stat.mean
				right_data = self.right_stat.mean
			if ZX_DEBUG:
				print( "stat count", self.left_stat.count )

			if not self.calc_zx_data( left_data, right_data ):
                                # Set orb status low if we go out of range
                                self.gesture_flags.orb_data_cnt = 0
                                self.gesture_flags.orb_status = False
			else:
				self.gesture_flags.zx_data_ready = True
				# Orb Detection
				if self.gesture_flags.orb_detect_enable:
					# Check if we are coming/leaving and within the orbital range
					if self.calc_orb(self.z_value, self.x_value):
						if ZX_DEBUG:
							print( "Calc_orb = True" )                            
						self.gesture_flags.orb_data_ready = True
						if self.gesture_flags.orb_data_cnt < self.gesture_flags.orb_data_cnt_limit:
							self.gesture_flags.orb_data_cnt += 1
						else:
							self.gesture_flags.orb_status = True
					else:
						if ZX_DEBUG:
							print( "Calc_orb = False" )
						if self.gesture_flags.orb_data_cnt > 0:
							self.gesture_flags.orb_data_cnt -= 1
						else:
							self.gesture_flags.orb_status = False
					if ZX_DEBUG:
						print( "orb_data_cnt =", self.gesture_flags.orb_data_cnt, "         " )
						print( "orb_status =", self.gesture_flags.orb_status, "        " )

		# Detect Valid Gestures
		if self.gesture_flags.gesture_recognition_enable and self.calc_gesture_recognition():
			self.gesture_flags.gesture_recognition_data_ready = True

		# Set data ready flag
		self.gesture_flags.data_ready = True

		# print("In Active loop: data_ready_flag = %s, sensor_data = %r" % (self.gesture_flags.data_ready,self.sensor_data) )

		# Restart the data collection process
		self.read_int_flags()
		self.set_ps_trigger()

	def __sleep_loop(self):
		""" Run for APP_SLEEP mode """
                raise NotImplementedError()

	def calc_gesture_noise(self, number_of_readings):
		""" :param number_of_readings: uint8_t """
		if number_of_readings <= 0:
			return

		gn_f0 = 0.0
		gn_f1 = 0.0
		gn_f2 = 0.0
		#super().init( VCNL4035_MODES.GESTURE )
		self.read_int_flags()
		time.sleep_ms(10)
		self.set_ps_trigger()

		self.read_int_flags()
		for i in range( number_of_readings ):
			if NOISE_DEBUG:
				print( "Evaluate Noise %i / %i" % (i,number_of_readings) )
			data = self.wait_data() # Interrupt driven

			gn_f0 += data[0] / number_of_readings
			gn_f1 += data[1] / number_of_readings
			gn_f2 += data[2] / number_of_readings
			self.read_int_flags()
			self.set_ps_trigger()

		self.gesture_noise[0] = gn_f0 # LDR1
		self.gesture_noise[1] = gn_f1 # LDR2
		self.gesture_noise[2] = gn_f2 # LDR3

	@property
	def gesture_noise_LDR1( self ):
		return self.gesture_noise[0]
	@property
	def gesture_noise_LDR2( self ):
		return self.gesture_noise[1]
	@property
	def gesture_noise_LDR3( self ):
		return self.gesture_noise[2]

	def calc_zx_data(self, left_data, right_data):
		""" Evaluate zx coordinate and update self.x_value & self.z_value.
		    Returns False when out of range, otherwise x_value & z_value are updated
		    :param left_data: left sensor data
		    :param right_data: right sensor data """

		if not( (left_data > self.zx_min_threshold) and (right_data > self.zx_min_threshold) ):
			return False
		left_dis = 0
		right_dis = 0
		x = 0
		z = 0
		if ZX_DEBUG:
			print( "calc_zx: left_data, right_data", left_data, right_data )
		# Range To Distance
		left_dis  = left_data + self.zx_coeff.B_1
		left_dis  = self.zx_coeff.A_1 * pow(left_dis, self.zx_coeff.k_1)
		right_dis = right_data + self.zx_coeff.B_1
		right_dis = self.zx_coeff.A_1 * pow(right_dis, self.zx_coeff.k_1)
		if ZX_DEBUG:
			print( "calc_zx: left_dis, right_dis", left_dis, right_dis, '         ' ) 
		# X Cordinate (Circle Intersection)
		x = pow(left_dis, self.zx_coeff.k_2) - pow(right_dis, self.zx_coeff.k_2)
		x = self.zx_coeff.A_2 * x
		self.x_value = int(x) # <<< stored value, maybe negative
		if ZX_DEBUG:
			print( "calc_zx: x_value", self.x_value, '          ' ) 
		
		# Z Cordinate
		z = self.zx_coeff.B_3 * pow( abs(x), self.zx_coeff.k_3 )
		z += (left_dis + right_dis)
		z *= self.zx_coeff.A_3
		self.z_value = int(z) # <<< stored value
		if ZX_DEBUG:
			print( "calc_zx: z_value, x_value", self.z_value, self.x_value, '     '  )
		return True


	def calc_orb(self, z, x): 
		""" Calculate if we are in the orb based on our current location 
		    calculate the orbital coordinate of the movement.

		    Returns False when out of range
		    :param z: z coordinate of movement (int16)
                    :param x: x coordinate of movement (int16) """
		if self.gesture_flags.orb_status:
			return self.check_orb( self.orb_cord_leaving, z, x )
		return self.check_orb( self.orb_cord, z, x )


	def check_orb(self, limits, z, x):
		""" return True/False 
		    :param limit: orb_cord_t()
		    :param Z: int16
		    :param X: int16 """
		if self.sensor_data[0] <= limits.center_IRED_max :
			return False

		if (x < limits.center_x_max) and (x > limits.center_x_min) and \
			(z < limits.center_z_max) and (z > limits.center_z_min):
			return True

		if (x < limits.side_x_max) and (x > limits.side_x_min):
			if (z < limits.side_z_max) and (z > limits.side_z_min):
				return True
		return False


	def calc_gesture_recognition(self): # return uint8
		""" return True/1 (uint8) when new gesture results data are ready """
		# See VCNL4035_App_Swipes.cpp
		# rely on self.gesture_machine for data storage
		if self.gesture.state == GestureMachine.STATE_RESET:
			self.gesture.clear()
			# OK, let's start data capture
			if self.is_zx_data_ready:
				zx = self.zx_data()
				self.gesture.append( zx )
				self.gesture.state = GestureMachine.STATE_COLLECT
				if self.on_start_collect:
					self.on_start_collect(self)
				#if GESTURE_DATA_DEBUG:
				#	print( "State: %i, zx_data: %r" % (self.gesture.state, zx) )		
				return False

		elif self.gesture.state == GestureMachine.STATE_COLLECT:
			if  self.gesture.timeout.expired:
				self.gesture.clear()
				self.gesture.state = GestureMachine.STATE_RESET
				if self.on_reset_collect:
					self.on_reset_collect(self)
				if GESTURE_DEBUG:
					print( "State: %i, RESET because expired" % (self.gesture.state) )		
				return False
			elif self.is_zx_data_ready:
				zx = self.zx_data()
				self.gesture.append( zx )
				if self.on_data_collect:
					self.on_data_collect(self)
				#if GESTURE_DATA_DEBUG:
				#	print( "State: %i, zx_data: %r" % (self.gesture.state, zx) )		

				if self.gesture.count >= GESTURE_COLLECT_SIZE:
					# It is time to decode the content
					self.gesture.state = GestureMachine.STATE_COMPUTE
				return False


		elif self.gesture.state == GestureMachine.STATE_COMPUTE:
			_r = GESTURE_NONE
			# It is time to detect the gesture from data
			if GESTURE_DEBUG:
				print( "State: %i, compute data: %r" % (self.gesture.state, self.gesture.data_points) )
			# StdDeviation on Z & X
			z_dev, x_dev = self.gesture.zx_dev()
			mz,bz, mx, bx = self.gesture.regression() # Linear regression, see vcnl4035-ZX-axis.jpg
			if GESTURE_DEBUG:
				print( "State: %i, z_dev & x_dev: %s, %s" % (self.gesture.state, z_dev, x_dev) )
				print( "State: %i, mZ & bZ : %s, %s" % (self.gesture.state, mz, bz) )
				print( "State: %i, mX & bX : %s, %s" % (self.gesture.state, mx, bx) )
			# Claculate the possible Gesture
			if (z_dev > (3*x_dev)) and (abs(mx)<25):
				_r = GESTURE_PUSH
			elif (x_dev > self.gesture_std_threshold) and (z_dev > self.gesture_std_threshold):
				if bx>200:
					_r = GESTURE_SWIPE_LEFT
				elif bx<-200:
					_r = GESTURE_SWIPE_RIGHT
			self.gesture.recognized = _r # Returning True will set gesture_recognition_data_ready to True

			if self.on_reset_collect:
				self.on_reset_collect(self)
			# Go to reset
			if GESTURE_DEBUG:
				print( "State: %i, RESET after compute" % (self.gesture.state) )
			self.gesture.state = GestureMachine.STATE_RESET

			# Return True when gesture detected otherwise False
			return _r != GESTURE_NONE






	def subtract_gesture_noise(self):
		""" Substract the gesture noise from self.sensor_data """
		for idx in range(3):
			self.sensor_data[idx] -= self.gesture_noise[idx]
			if self.sensor_data[idx] < 0:
				self.sensor_data[idx] = 0


	# === Checks ===
	@property
	def is_gesture_activity( self ): # bool
		""" Activity loop detected sensor_value over the gesture thresold """
		return self.gesture_flags.activity_status

	@property
	def is_zx_data_ready( self ): # bool
		if self.gesture_flags.zx_data_ready:
			self.gesture_flags.zx_data_ready = False
			return True
		return False

	@property
	def is_orb_data_ready( self ): # bool
		if self.gesture_flags.orb_data_ready:
			self.gesture_flags.orb_data_ready = False
			return True
		return False

	@property
	def is_gesture_recognition_data_ready( self ): # bool
		if self.gesture_flags.gesture_recognition_data_ready:
			self.gesture_flags.gesture_recognition_data_ready = False
			return True
		return False

        @property
	def is_data_ready( self ): # bool
		""" Activity loop get completed """
		if self.gesture_flags.data_ready:
			self.gesture_flags.data_ready = False
			return True
		return False

	# === Gets ===
	def zx_data(self):
		""" returns a tuple with (Z, X) data """
                return (self.z_value, self.x_value)

	def getGestureRecognitionData( self, delay_samples ):
		""" :param delay_samples: int16* """
                raise NotImplementedError()

	# === Settings ===
	@property
	def gesture_noise_subtract( self ):
		return self.gesture_flags.noise_canc_enable==True

	@gesture_noise_subtract.setter
	def gesture_noise_subtract(self, enable):
		""" :param state: boolean/uint8 """
                self.gesture_flags.noise_canc_enable = True if enable else False


	def sleep_mode( self ):
		self.current_mode = APP_SLEEP

	def active_mode( self ):
                self.current_mode = APP_ACTIVE
	
	@property
	def zx_enable( self ):
		return self.gesture_flags.zx_enable

	@zx_enable.setter
	def zx_enable( self, enable):
                self.gesture_flags.zx_enable = enable

	@property
	def zx_smooth( self ):
		return self.gesture_flags.zx_smooth_enable

	@zx_smooth.setter
	def zx_smooth( self, value ):
		self.zx_smooth_enable = value

	@property
	def orb_detect( self ):
		return self.gesture_flags.orb_detect_enable

	@orb_detect.setter
	def orb_detect( self, enable ):
		self.gesture_flags.orb_detect_enable = enable

	@property
	def gesture_recognition( self ):
		return self.gesture_flags.gesture_recognition_enable

	@gesture_recognition.setter
	def gesture_recognition( self, enable ):
		self.gesture_flags.gesture_recognition_enable = enable
