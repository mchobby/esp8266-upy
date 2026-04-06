""" Btn tools - Button Helpers

	Domeu - Apr 6, 2026 - creation

 see https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN
"""
from machine import Pin
from timetls import TimeoutTimer
import time

DEBOUNCE_MS = 25 
CLICK_TIMEOUT = 0.250 # 500ms, Time during which an additional click is accepted.
TRIGGER_TIMEOUT = 1.000 # 1 sec, One full second before the action is "triggered"


class BtnClicks( Pin ):
	""" ClickBtn count the number of time the button was. Use pull-up resistor, IRQ and debouncing (25ms).
	    Subsequent click cannot occurs before click_timeout (250ms).
	    The number of click can be read only after the trigger_timeout (after the last click, 1sec). """
	def __init__( self, pin_nr, click_timeout=CLICK_TIMEOUT, trigger_timeout=TRIGGER_TIMEOUT ):
		super().__init__( pin_nr,  Pin.IN, Pin.PULL_UP )
		self.irq( self.__btn_callback, trigger=Pin.IRQ_RISING )
		self.__count = 0
		self.last_click = time.ticks_ms()
		self.click_timeout = click_timeout
		self.trigger_timeout = trigger_timeout 
		self.click_timer = TimeoutTimer()
		self.trigger_timer = TimeoutTimer()

	def __btn_callback( self, btn ):
		# debounce
		if time.ticks_diff( time.ticks_ms(), self.last_click ) < DEBOUNCE_MS:
			return
		# Are we below the time to accept another click
		if self.__count > 0:
			if not self. click_timer.expired:
				self.last_click = time.ticks_ms() 
				return
		else:
			# Start the capture
			self.trigger_timer.set( self.trigger_timeout )
		self.__count += 1
		self.click_timer.set( self.click_timeout ) 
		if not self.trigger_timer.expired: # if trigger not expired the we reset it
			self.trigger_timer.set( self.trigger_timeout )
		self.last_click = time.ticks_ms()

	@property
	def count( self ):
		""" Return None as long as no count detected and trigger_timeout not elapsed.
		    Once count read, it resets the internal counter. """
		if self.__count <= 0:
			return None
		if not self.trigger_timer.expired:
			return None
		_v = self.__count
		self.__count = 0
		return _v

