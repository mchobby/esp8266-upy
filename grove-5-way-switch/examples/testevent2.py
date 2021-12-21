"""
Grove 5 Way Switch - test the EVENT MODE for Grove5Way class driver (SeeedStudio)
	Complete test.

See https://github.com/mchobby/esp8266-upy/tree/master/grove-5-way-switch

"""
from machine import I2C
from grove5way import Grove5Way
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

sw = Grove5Way( i2c )
sw.set_event_mode( True )
print( 'versions    :', sw.device_version() ) # return the 10 bytes of version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( 'event mode  :', 'EVENT')
print( '' )
print( 'Play with the joystick, simple/double click & long press any direction')

# Using lambda expression to associate with a tuple
text_n_test = { 'Up'     : (lambda ev : ev.up   , lambda ev : ev.up_events.has_event   , lambda ev : ev.up_events   ),
				'Down'   : (lambda ev : ev.down , lambda ev : ev.down_events.has_event , lambda ev : ev.down_events ),
				'Left'   : (lambda ev : ev.left , lambda ev : ev.left_events.has_event , lambda ev : ev.left_events ),
				'Right'  : (lambda ev : ev.right, lambda ev : ev.right_events.has_event, lambda ev : ev.right_events),
				'CLICK!' : (lambda ev : ev.click, lambda ev : ev.click_events.has_event, lambda ev : ev.click_events) }

while True:
	ev = sw.get_event()
	if ev.has_event: # Contains an event for any of the buttons ?
		for btn_name, event_tuple in text_n_test.items():
			# Testing buttons
			ev_btn, ev_btn_has_event, events_ref = event_tuple
			# Equivalent of ev.up -> get raw value
			if ev_btn(ev):
				print( btn_name, 'CLICK (raw)')
			# Equivalent of ev.up_events.has_event -> specific button has event ?
			if ev_btn_has_event(ev):
				print( btn_name, 'has event' )
				# Describe the events
				# Equivalent of ev.up_events.single_click
				if events_ref(ev).single_click :
					print( '  +-> Single click')
				if events_ref(ev).double_click :
					print( '  +-> Double click')
				if events_ref(ev).long_press :
					print( '  +-> long press')
				if events_ref(ev).level_changed :
					print( '  +-> level changed')

	time.sleep(0.250)
