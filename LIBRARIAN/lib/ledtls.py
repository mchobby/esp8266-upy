""" LED tools - some led management tool

	Domeu - Dec 2, 2025 - creation
"""
from micropython import const
from machine import idle, PWM, Pin
from math import sin, pi
import time

class LedError:
	""" Show an error code on a single LED. """

	# States
	ALERT = const(1)
	POST_ALERT = const(2)
	SHOW_CODE = const(3)
	PAUSE = const(4)

	POST_ALERT_MS = 1000 # 2 sec
	PAUSE_MS = 2000

	def __init__( self, pin, owner=None, exit_cb=None ):
		""" pin : initialized Pin object to get control of.
		    owner : optional object reference (may be useful when using exit_cb callback
		    exit_cb != None : Error flashing is BLOCKING callee until exit_cb(self) return True
		    exit_cb == None : Error flashing is NOT blocking. Call update() as often as posibble to trigger the Error display """
		self.pin = pin
		self.pin.value( False )
		self.error_count = 0
		self.exit_cb = exit_cb

		self.states = [(LedError.ALERT,self.play_alert),(LedError.POST_ALERT,self.play_post_alert),(LedError.SHOW_CODE,self.play_show_code),(LedError.PAUSE,self.play_pause)]
		self.state_current = None
		self.state_start = 0


	def set( self, error_count ): 
		""" Initialize the Error Count animation (or reset if when set to 0 """
		if error_count==0:
			self.reset()
			return

		self.error_count = error_count
		self.state_current = LedError.ALERT
		self.state_start = time.ticks_ms()

		if self.exit_cb!=None: # Blocking error display
			while self.exit_cb(self)!=True:
				self.update()
				idle()

	def reset( self ):
		self.error_count=0
		self.pin.value( False )
		self.state_current = None
		self.state_start = time.ticks_ms()

	def update( self ):
		""" IF not using exit_cb param THEN callee is responsible to update as often as possible """
		# Make the flash display and take care if the required pause before next error code occurence.
		def next_state( state ):
			for i in range( len(self.states) ):
				if self.state_current == self.states[i][0]:
					if (i+1) < len(self.states):
						return self.states[i+1][0]
					else:
						return self.states[0][0]

		if self.state_current == None:
			return
		for _state, _cb in self.states:
			if _state==self.state_current:
				_r = _cb()
				if _r:
					# Select Next State
					self.state_current=next_state(self.state_current)
					self.state_start=time.ticks_ms()

	def play_alert(self):
		for i in range(20):
			self.pin.toggle()
			time.sleep_ms(50)
		self.pin.value(0)
		return True # Task complete

	def play_post_alert(self):
		return time.ticks_diff(time.ticks_ms(),self.state_start) > LedError.POST_ALERT_MS

	def play_show_code(self):
		for i in range( self.error_count ):
			self.pin.on()
			time.sleep_ms( 250 )
			self.pin.off()
			time.sleep_ms( 250 )
		# Task is complete
		return True 

	def play_pause(self):
		return time.ticks_diff(time.ticks_ms(),self.state_start) > LedError.PAUSE_MS
		

class HeartBeat:
	""" Show an heartbeat on the LED """
	LIT_MS = 50
	PAUSE_MS = 2_000

	def __init__( self, pin, lit_ms=None, pause_ms=None ):
		""" pin : initialized Pin object to get control of """
		self.pin = pin
		self.pin.value( False )
		self.lit_ms = lit_ms if lit_ms!=None else HeartBeat.LIT_MS
		self.pause_ms = pause_ms if pause_ms!=None else HeartBeat.PAUSE_MS
		self.pause_start = time.ticks_ms()

	def reset( self ):
		self.pin.off()

	def update( self ):
		# Just update the heart beat
		if time.ticks_diff( time.ticks_ms(), self.pause_start )>self.pause_ms:
			self.pin.on()
			time.sleep_ms( self.lit_ms )
			self.pin.off()
			self.pause_start = time.ticks_ms()

class Pulse:
	""" Show a pulsing led """
	CYCLE_MS = 2000

	def __init__( self, pin, pulse_ms=None ):
		""" cycle_ms, time from pulsing from off->on->off """
		self.pin = pin
		self.pwm = PWM( pin )
		self._cycle_ms = pulse_ms if pulse_ms!=None else Pulse.CYCLE_MS
		self.rad_per_ms = pi / self._cycle_ms
		self.pwm.freq( 50 )
		self.pwm.duty_u16( 0 )
		self.start = time.ticks_ms()

	def reset( self ):
		self.pwm.duty_u16( 0 )

	def update( self ):
		_diff = time.ticks_diff(time.ticks_ms(),self.start)
		_diff_remain = _diff % self._cycle_ms # from 0 -> cycle_ms
		# FROM   0-->cycle_ms  TO   0-->180 degree
		_diff_rad = _diff_remain * self.rad_per_ms 
		_duty_u16 = int( sin(_diff_rad)*65535 )
		if  _duty_u16<0: 
			_duty_u16 = 0
		elif _duty_u16>65535:
			_duty_u16 = 65535
		self.pwm.duty_u16( _duty_u16 )

	@property
	def pulse_ms( self ):
		return self._cycle_ms

	@pulse_ms.setter
	def pulse_ms( self, value ):
		assert 250<=value<=5000
		self._cycle_ms = value
		self.rad_per_ms = pi / self._cycle_ms

class SuperLed:
	""" LED supporting multiple control mode (GPIO, HEARTBEAT, PULSE, ERROR) """
	# Various mode of the superled
	GPIO = const(1)
	HEARTBEAT = const(2)
	PULSE = const(3)
	ERROR = const(4)

	def __init__(self, pin ):
		self.pin = pin
		self.__handler = None # SubClass handling the functionnality
		self.pin.off()

	def release_handler( self ):
		if self.__handler==None:
			return
		self.__handler.reset()		
		self.__handler = None
		self.pin.init(Pin.OUT) # disable PWM mode if any

	@property
	def handler(self):
		""" Offer a direct access to underlaying object (Pulse,ErrorLed,HeartBeat) """
		if self.__handler==None:
			return self.pin # we control a GPIO
		else:
			return self.__handler

	@property 
	def mode( self ):
		""" Identify the current mode running the SuperLed """
		if self.__handler==None:
			return SuperLed.GPIO
		elif isinstance( self.__handler, LedError ):
			return SuperLed.ERROR
		elif isinstance( self.__handler, HeartBeat ):
			return SuperLed.HEARTBEAT
		elif isinstance( self.__handler, Pulse ):
			return SuperLed.PULSE
		raise Exception( "Handler instance undefined! Mode cannot be resolved!")

	def update( self ):
		if self.__handler==None: # is this a simplpe GPIO?
			return
		self.__handler.update()

	# PIN GPIO management

	def on( self ):
		""" Switch to GPIO mode and set the value """
		if self.mode != SuperLed.GPIO:
			self.release_handler()
			self.pin.init( Pin.OUT )
		self.pin.on()

	def off( self ):
		""" Switch to GPIO mode and set the value """
		if self.mode != SuperLed.GPIO:
			self.release_handler()
			self.pin.init( Pin.OUT )
		self.pin.off()

	def value( self, value ):
		""" Switch to GPIO mode and set the value """
		if value:
			self.on()
		else:
			self.off()

	# PIN Advanded Feature

	def error( self, error_count ):
		if self.mode==SuperLed.ERROR:			
			self.__handler.set( error_count )
		else: 
			self.release_handler()
			self.__handler = LedError( self.pin )
			self.__handler.set( error_count )

	def heartbeat( self, lit_ms=None, pause_ms=None ):
		if self.mode==SuperLed.HEARTBEAT:
			if lit_ls!=None:
				self.__handler.lit_ms = lit_ms
			if pause_ms!=None:
				self.__handler.pause_ms = pause_ms
		else:
			self.release_handler()
			# Creatte New Instance
			self.__handler = HeartBeat( self.pin, lit_ms, pause_ms )

	def pulse( self, cycle_ms=None ):
		if self.mode==SuperLed.PULSE:
			if cycle_ms!=None:
				self.__handler.cycle_ms = cycle_ms
		else:
			self.release_handler()
			self.__handler = Pulse( self.pin, cycle_ms )
