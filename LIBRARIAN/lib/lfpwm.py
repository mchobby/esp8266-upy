# Low Frequency PWM Driver to control High Inertia Devices
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/lfpwm
#
#
# Compatible with:
#  * Raspberry-Pico : using the only Timer() available.
#
# July 29, 2021 - Meurisse D. (MCHobby) - initial writing
#
__version__ = '0.0.1'

from machine import Pin, Timer
from os import uname

class LowFreqPWM:
	""" Low Frequency PWM """
	_pin = None
	_period_ms = None
	_duty_ms = None
	_ton_ms = 0  # required time ON (ms) for the peripheral (eg: SSR relay)
	_toff_ms = 0 # required time OFF for the peipheral
	__tim = None # Timer for the tick() callback
	__ms = 0

	def __init__( self, pin, period, ton_ms = 0, toff_ms = 0 ):
		pin.init( Pin.OUT )
		LowFreqPWM._pin = pin
		LowFreqPWM._period_ms = period * 1000
		LowFreqPWM._ton_ms = ton_ms
		LowFreqPWM._toff_ms = toff_ms
		LowFreqPWM._duty_ms = 0 # current duty cycle in ms
		LowFreqPWM._next_duty_ms = None # desired duty_ms at NEXT PWM round (avoid rebound)
		LowFreqPWM._state = False # Start with low signal. Store pin state into variable (faster to read from memory)
		LowFreqPWM._pin.value( LowFreqPWM._state )

		LowFreqPWM.__tim = None
		LowFreqPWM.__elapsed = 0 # Nbr of ms elapsed since last reset
		self.init() # Init timer & Call back

	@property
	def period_ms( self ):
		return LowFreqPWM._period_ms

	def init( self ):
		# Init the Timer for Pico
		if uname().sysname == 'rp2':
			LowFreqPWM.__tim = Timer()
			LowFreqPWM.__tim.init( freq=100, mode=Timer.PERIODIC, callback=LowFreqPWM.tick )
		else:
			raise NotImplementedError( 'plateform %s not supported' % uname().sysname )

	def deinit( self ):
		# LowFreqPWM.__tim.callback( None ) ; not possible on rp2
		LowFreqPWM.__tim.deinit() #= Timer.init( freq=100, mode=Timer.PERIODIC,
		LowFreqPWM._pin.value( False ) # Ensure pin off

	def duty_u16( self, value ):
		assert 0 <= value <= 65535, "Invalid value"
		if value == 0: # avoids rounding issue
			duty_ms = 0
		elif value == 65535: # avoids rounding issue
			duty_ms = LowFreqPWM._period_ms
		else: # Make it proportionnal -> rounding issue
			duty_ms = int(LowFreqPWM._period_ms * value /65535)

		if duty_ms >= (LowFreqPWM._period_ms - LowFreqPWM._toff_ms):
			duty_ms = LowFreqPWM._period_ms
		if duty_ms <= (LowFreqPWM._ton_ms + LowFreqPWM._toff_ms):
			duty_ms = 0

		# If current duty cycle is 0 or MAX we can apply new setting now
		if (LowFreqPWM._duty_ms == 0) or (LowFreqPWM._duty_ms == LowFreqPWM._period_ms):
			LowFreqPWM._duty_ms = duty_ms # Minimal manipulation of shared variable
		else: # otherwise apply new settings at next PWM cycle
			LowFreqPWM._next_duty_ms = duty_ms

	def duty_ms( self, ms ):
		""" Set the duty cycle in millisecond. Prefer duty_u16() """
		assert 0 <= ms <= LowFreqPWM._period_ms
		if ms==0:
			self.duty_u16( 0 )
		elif ms==LowFreqPWM._period_ms:
			self.duty_u16( 65535 )
		else: # proportionnal
			self.duty_u16( int(65535*ms/LowFreqPWM._period_ms) )

	def duty_ratio( self, percent ):
		""" Set the duty cycle in percent. Prefer duty_u16() """
		assert 0 <= percent <= 100
		if percent==0:
			self.duty_u16( 0 )
		elif percent==100:
			self.duty_u16( 65535 )
		else: # proportionnal
			self.duty_u16( int(65535*percent/100) )

	def tick( timer ):
		# Timer callback routine
		LowFreqPWM.__elapsed += 10
		if (LowFreqPWM.__elapsed >= LowFreqPWM._duty_ms) and LowFreqPWM._state and (LowFreqPWM._duty_ms!=LowFreqPWM._period_ms):
			#print('1')
			LowFreqPWM._pin.value( False )
			LowFreqPWM._state = False
		if (LowFreqPWM.__elapsed <= LowFreqPWM._duty_ms) and not(LowFreqPWM._state):
			#print('2')
			LowFreqPWM._pin.value( True )
			LowFreqPWM._state = True
		if LowFreqPWM.__elapsed > LowFreqPWM._period_ms:
			# Apply new duty_ms ONLY when we finished a PWM cycle
			if LowFreqPWM._next_duty_ms != None:
				LowFreqPWM._duty_ms = LowFreqPWM._next_duty_ms
				LowFreqPWM._next_duty_ms = None
			LowFreqPWM.__elapsed = 0 # Restart counter... but next count of 10 ms did already started
