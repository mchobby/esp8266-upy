"""
Pyboard Micropython driver for Adafruit Motor Shield V2

Connect either X9 and X10 (I2C bus 1) or Y9 and Y10 (I2C bus 2) of the pyboard
to the SCL and SCA pins on the shield (near the pass-through servo pins).
Connect the GND and VIN pins of the pyboard to the Gnd and 5V pins of the shield
(on the same side as the motor power connector).
Also connect the VIN pin of the pyboard to the Vin pin of the shield if you do not
use an external power supply for the motors.

History:
  2020-03-22 - Meurisse D. (MCHobby)
			   support (at) mchobby.be
               Integration in esp8266-upy/adfmotors.py
			   Interface closer to Adafruit MotorShield
			   pyb module independant
			   reuse the existing pca9685 driver available at esp8266-upy repository
  2018-03-02 - Original source code
               frederic.boulanger (at) centralesupelec.fr
			   https://wdi.supelec.fr/boulanger/MicroPython/AdafruitMotorShield
			   Special thanks for the great work.
"""
import pca9685
import math    # Only needed for math.sin. Can be precomputed if math module is not available
# plateform agnostic delay millisecond  and delay microsecond function
_delay_ms = None
_delay_us = None
try:
	from pyb import delay_ms as _delay_ms
except:
	pass
if not(_delay_ms):
	try:
		from time import sleep_ms as _delay_ms
	except:
		pass
try:
	from pyb import udelay_ms as _delay_us
except:
	pass
if not(_delay_us):
	try:
		from time import sleep_us as _delay_us
	except:
		pass
if not(_delay_ms) and not(_delay_us):
	raise Exception( "Unable to resolve _delay_ms or _delay_us for the current plateform" )

# select the best _wait_ms function to do the job with the best resolution and
# accepting milliseconds with decimal parts
def __wait_with_ms( ms ):
	_delay_ms( int(ms) )
def __wait_with_us( ms ):
	_delay_us( int(ms*1000) )
_wait_ms = __wait_with_us if _delay_us else __wait_with_ms

FORWARD  = 1
BACKWARD = 2
BRAKE    = 3
RELEASE  = 4

def arduino_map(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

class MotorBase:
	""" Base class for the MotorShield / MotorWing implementation.

	 	Rely on a PCA9685 to control the various outputs. """

	def __init__( self, pca_config, i2c, address=0x60, freq=500 ):
		# pca_config contains the PCA pin definition depending on the use case.
		# See the MotorShield implemenation for more information
		self.pca     = pca9685.PCA9685( i2c, address )
		#self.pca.setFreq( freq )
		self.pca.freq( freq )
		self.pca_config = pca_config

	def get_motor( self, n ):
		""" Returns an initialized DCMotor object for Motor M1, M2, M3, M4

	 		:param n: the index of motor definition 1..4 """
		if not( n in self.pca_config['motors'] ):
			raise ValueError( 'No motor definition for %s' % n )
		return DCMotor( self.pca, self.pca_config['motors'][n] )

	def get_stepper( self, steps, n ):
		""" Returns an initialized Stepper object for S1 = M1+M2 or S2 = M3+M4

			:params steps: nbre of steps per revolution
			:params n: the index of stepper motor 1..2 """
		if not( n in self.pca_config['steppers'] ):
			raise ValueError( 'No stepper definition for %s' % n )
		return Stepper( steps, self.pca, self.pca_config['steppers'][n] )

	def get_servo( self, n ):
		""" Returns and initialize Servo object connected to the Extra PWM output

			:params n: the PWM output number (eg: 14) """
		if not( n in self.pca_config['pwms'] ):
			raise ValueError( 'No pwm definition for %s' % n )
		return Servo( self.pca, self.pca_config['pwms'][n] )

	def get_pwm( self, n ):
		""" Returns and initialize PWM object connected to the Extra PWM output

			:params n: the PWM output number (eg: 14) """
		if not( n in self.pca_config['pwms'] ):
			raise ValueError( 'No pwm definition for %s' % n )
		return PWM( self.pca, self.pca_config['pwms'][n] )

class DCMotor:
	""" A DC motor connected to two of the side connectors
		labelled M1, M2, M3 and M4 on the shield.
	"""

	def __init__(self, pca, pca_config ):
		""" Initialize a DC motor driven by PCA9685 'pca' on port 'motor' """
		self._pca = pca
		self._pwm = pca_config['pwm']
		self._in1 = pca_config['in1']
		self._in2 = pca_config['in2']

		self.__speed = 0 # 8bits speed
		self.__th  = 0 # last knwon thresold
		self.throttle( 0 ) # set in1 & in2 to low --> Stop / release

	def run( self, cmd ):
		""" run() as defined in Adafruit Motor shield """
		if cmd == FORWARD:
			self.__speed = abs( self.__speed )
			self.throttle_8bits( self.__speed )
		elif cmd == BACKWARD:
			self.__speed = -1* abs( self.__speed )
			self.throttle_8bits( self.__speed )
		elif cmd == BRAKE:
			self.brake()
		elif cmd == RELEASE:
			self.throttle( 0 )  # set in1 & in2 to low --> Stop / release

	def speed( self, value ):
		""" change the current speed """
		assert -255 <= value <= 255, "Invalid speed %s" % value
		self.__speed = value # Remember the speed
		# If we are already moving the motor --> change the motor speed
		if self.__th != 0:
			self.throttle_8bits( value )

	def throttle_8bits(self, th): # th is -255..255
		""" convert a value from the Arduino range (0-255) to PCA range (0-4095) """
		assert -255 <= th <= 255, "Invalid value %s" % th
		self.throttle( int(arduino_map(th,-255,255,-4095,4095)) )

	def throttle(self, th): # th is -4095..4095
		""" Set the throttle of this motor between -4095..4095.
			Prefer the speed() and run() functions instead of this method.

		    Negative values of 'th' make the motor run in the reverse direction
		    compared to positive values. The absolute value of 'th' varies from:
		      0: the motor is stopped, to
		      4095: the motor is at max speed.
		"""
		if th > 0: # Forward
			self._pca.duty(self._in2, 0)
			self._pca.duty(self._in1, 4095)
		elif th == 0:
			self._pca.duty(self._in2, 0)
			self._pca.duty(self._in1, 0)
		else:
			self._pca.duty(self._in1, 0)
			self._pca.duty(self._in2, 4095)
			th = -th
		self._pca.duty(self._pwm, th)
		self.__th = th # last know throttle


	def brake(self):
		""" Make the motor stop by setting the PWM to 0 while maintaining the voltage.
		    This stops the motor more quickly than juste setting the throttle to 0.
		"""
		self._pca.duty(self._in1, 4095)
		self._pca.duty(self._in2, 4095)
		self._pca.duty(self._pwm, 0)


# Number of micro steps in one step
MICROSTEPS = 16

SINGLE = 1 # fullStep()
DOUBLE = 2 # halfStep()
INTERLEAVE = 3 # waveStep()
MICROSTEP = 4 # microStep()

class Stepper:
	""" A stepper motor: stepper 1 is plugged on motors M1 and M2,
		stepper 2 is plugged on motors M3 and M4 """

	# Coil driving phases for steper motors:
	# Even phases drive only one coil.
	# Odd phases drive two coils at once.
	_PHASES = bytes([
		0b0001,
		0b0011,
		0b0010,
		0b0110,
		0b0100,
		0b1100,
		0b1000,
		0b1001
	])

	# Coil drive sine computed for one quadrant ([0, π/2])
	_DRIVESINE = tuple(round(4095*math.sin(i/MICROSTEPS*math.pi/2)) for i in range(MICROSTEPS+1))

	def __init__(self, steps, pca, pca_config):
		""" Initialiaze stepper motor 1 or 2 ('stepper') driven by PCA9685 'pca'
		"""
		self._pca = pca
		self._steps = steps # Steps per revolution
		self._rpm   = 5     # Suited RPM for rotation
		# configure the pins
		self._pwma = pca_config['a']['pwm']
		self._ain1 = pca_config['a']['in1']
		self._ain2 = pca_config['a']['in2']
		self._pwmb = pca_config['b']['pwm']
		self._bin1 = pca_config['b']['in1']
		self._bin2 = pca_config['b']['in2']
		self._drive = [0,0,0,0]
		self._drive[0] = self._ain2
		self._drive[1] = self._bin1
		self._drive[2] = self._ain1
		self._drive[3] = self._bin2
		self._phase = 0
		self._currentstep = 0
		# Activate the PWMs on the PCA9685
		self._pca.pwm( self._pwma, 0, 0 )
		self._pca.pwm( self._ain1, 0, 0 )
		self._pca.pwm( self._ain2, 0, 0 )
		self._pca.pwm( self._pwmb, 0, 0 )
		self._pca.pwm( self._bin1, 0, 0 )
		self._pca.pwm( self._bin2, 0, 0 )
		# Power up the Motor (PWMA & PWMB)
		self.power()

	@property
	def speed( self ):
		return self._rpm

	@speed.setter
	def speed( self, rpm ):
		""" Mimic adafruit setSpeed """
		self._rpm = rpm

	def step( self, steps, dir=FORWARD, style = SINGLE):
		""" Try to mimic the Adafruit step() at best """
		# Calculate the appropriate delay (in ms) to achieve the RPM
		# Decimal part allowed.
		if style in (SINGLE,DOUBLE):
			delay = 60000/(self._rpm * self._steps)
		elif style == INTERLEAVE:
			delay = (60000/2)/(self._rpm * self._steps) # Must go twice faster to keep RPM
		else:
			delay = (60000/MICROSTEPS)/(self._rpm * self._steps) # Must go MICROSTEPS time faster to keep RPM
		#print( 'delay %s ms for %s steps' % (delay,steps) )

		# direction
		if dir==BACKWARD:
			steps = -1 * steps

		if style == SINGLE:
			# Is a single coil stepping (sometimes referred to Wave Drive).
			# It drives motor by energizing one coil at the time. Saving power
			self.waveStep(steps, delay )
		elif style == DOUBLE:
			# Two coils are energized (Full Stepping).
			# This gives full torque of the motor.
			self.fullStep(steps, delay )
		elif style == INTERLEAVE:
			# It is half stepping, when coil pairs are energized simultaneously.
			# So you get double resolution but requires two half step call to
			# perform a complete step rotation
			self.halfStep(steps, delay )
		elif style == MICROSTEP:
			# Use PWM to maintain the intermediate position (the most commonly used)
			# requires MICROSTEPS calls to perform a full step
			self.microStep(steps, delay )

	def power(self):
		""" Power the PWM lines of the driver. """
		self._pca.duty(self._pwma, 4095)
		self._pca.duty(self._pwmb, 4095)

	def release(self):
		""" Shut off the power on the motor. """
		self._pca.duty(self._pwma, 0)
		self._pca.duty(self._ain1, 0)
		self._pca.duty(self._ain2, 0)
		self._pca.duty(self._pwmb, 0)
		self._pca.duty(self._bin1, 0)
		self._pca.duty(self._bin2, 0)
		self._phase = 0

 	def waveStep(self, n, delay=20):
		""" Perform n steps in wave drive mode (one coil at a time),
			waiting delay milliseconds between each step.
			A negative number of steps turn in the other direction. """
		if n == 0:
			return
		step = 1
		if n < 0:
			step = -1
			n = -n
		for i in range(n):
			# In single step mode, the phase is always even (one coil at a time)
			if self._phase % 2 != 0 :
				self._phase += step
			else:
				self._phase += 2 * step
			# Keep the phase in [0..7]
			while self._phase < 0:
				self._phase += 8
			while self._phase > 7:
				self._phase -= 8
			# Set motor drive lines.
			self._pca.duty(self._pwma, 4095)
			self._pca.duty(self._pwmb, 4095)
			for i in range(4):
				self._pca.duty(self._drive[i], 4095 * ((Stepper._PHASES[self._phase] >> i) & 1))
			_wait_ms(delay)

	def fullStep(self, n, delay=10):
		""" Perform n steps in full drive mode (two coils at a time),
			waiting delay milliseconds between each step.
			A negative number of steps turn in the other direction. """
		if n == 0:
			return
		step = 1
		if n < 0:
			step = -1
			n = -n
		for i in range(n):
			# In double step mode, the phase is always odd (two coils at a time)
			if self._phase % 2 == 0 :
				self._phase += step
			else:
				self._phase += 2 * step
			# Keep the phase in [0..7]
			while self._phase < 0:
				self._phase += 8
			while self._phase >= 8:
				self._phase -= 8
			# Set motor drive lines.
			self._pca.duty(self._pwma, 4095)
			self._pca.duty(self._pwmb, 4095)
			for i in range(4):
				self._pca.duty(self._drive[i], 4095 * ((Stepper._PHASES[self._phase] >> i) & 1))
			_wait_ms(delay)

 	def halfStep(self, n, delay=10):
		""" Perform n steps in half-step drive mode (alternate between one and two coils at a time),
			waiting delay milliseconds between each step.
			A negative number of steps turn in the other direction.
			This takes twice as many steps as wave and full steps to perform a revolution. """
		if n == 0:
			return
		step = 1
		if n < 0:
			step = -1
			n = -n
		for i in range(n):
			self._phase += step
			# Keep the phase in [0..7]
			while self._phase < 0:
				self._phase += 8
			while self._phase >= 8:
				self._phase -= 8
			# Set motor drive lines.
			self._pca.duty(self._pwma, 4095)
			self._pca.duty(self._pwmb, 4095)
			for i in range(4):
				self._pca.duty(self._drive[i], 4095 * ((Stepper._PHASES[self._phase] >> i) & 1))
			_wait_ms(delay)

	def microStep(self, n, delay=1):
		""" Perform n steps in micro-step drive mode (two coils at a time with sines in quadrature),
			waiting delay milliseconds between each step.
			A negative number of steps turn in the other direction.
			This takes MICROSTEPS times as many steps as wave and full steps to perform a revolution. """
		if n == 0:
			return
		step = 1
		if n < 0:
			step = -1
			n = -n
		for i in range(n):
			self._phase += step
			while self._phase < 0:
				self._phase += 4 * MICROSTEPS
			while self._phase >= 4 * MICROSTEPS:
				self._phase -= 4 * MICROSTEPS
			quadrant = self._phase // MICROSTEPS
			if (quadrant % 2) == 0 :
				power_a = Stepper._DRIVESINE[(quadrant + 1) * MICROSTEPS - self._phase]
				power_b = Stepper._DRIVESINE[self._phase - (quadrant * MICROSTEPS)]
			else:
				power_a = Stepper._DRIVESINE[self._phase - (quadrant * MICROSTEPS)]
				power_b = Stepper._DRIVESINE[(quadrant + 1) * MICROSTEPS - self._phase]
			# Set motor drive lines.
			self._pca.duty(self._pwma, power_a)
			self._pca.duty(self._pwmb, power_b)
			for i in range(4):
				self._pca.duty(self._drive[i], 4095 * ((Stepper._PHASES[2*quadrant+1] >> i) & 1))
			_wait_ms(delay)


class Servo:
	""" A servo motor connected to one of the 4 remaining PWM output of the shield.
		Works best if the frequency of the PCA9685 is about 50Hz. """
	def __init__(self, pca, pca_config, min_us=500, max_us=2500, range=180):
		""" Initialize a servo motor driven by PWM number 'pwm'.
			:param pca_config: contain the PWM Pin Number definition
			:param min_us: the min duty duration in microseconds to get the min and max rotation positions
			:param max_us: see min_us
			:param range: rotation range in degrees (usually 180°). """
		self._pca = pca
		self._pwm = pca_config['pwm']
		if not (0<= self._pwm <= 15):
			raise ValueError('pwm pin %s is outside the PCA9685 range!' % self._pwm )
		self._minus = min_us
		self._maxus = max_us
		self._range = range
		self._pca.duty(self._pwm, 0) # release the servo
		self._period = 1e6 / self._pca.freq()
		self._minduty = int(self._minus / (self._period / 4095))
		self._maxduty = int(self._maxus / (self._period / 4095))

	def set_duty_time(self, us):
		""" Set the duty time of the servo in microseconds. """
		self._pca.duty(self._pwm, int(us / (self._period / 4095)))

	def release(self):
		""" Release the servo (set PWM to 0). """
		self._pca.duty(self._pwm, 0)

	def angle(self, degrees): # mimic micropython Servo class
		""" Set the angle position of the servo in degrees. """
		self._pca.duty(self._pwm, int(self._minduty + (self._maxduty - self._minduty) * (degrees / self._range)))

class PWM:
	def __init__(self, pca, pca_config ):
		""" Initialize a PWM pin
			:param pca_config: contain the PWM Pin Number definition """
		self._pca = pca
		self._pwm = pca_config['pwm']
		if not (0<= self._pwm <= 15):
			raise ValueError('pwm pin %s is outside the PCA9685 range!' % self._pwm )
		# set it to LOW
		self._pca.duty( self._pwm, 0 )

	def duty_percent( self, *args, **kw ):
		self._pca.duty_percent( self._pwm, *args, **kw )

	def duty( self, *args, **kw ):
		self._pca.duty( self._pwm, *args, **kw )

	def pwm( self, *args, **kw ):
		""" see PCA9685.pwm() which waits for 'on' and 'off' arguments """
		self._pca.pwm( self._pwm, *args, **kw )
		
