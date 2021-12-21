"""
Grove 5 Way Switch - test the EVENT MODE for Grove5Way class driver (SeeedStudio)
	ONLY for UP and CLICK buttons.

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
print( 'ONLY  UP and CLICK buttons')
print( '' )

while True:
	ev = sw.get_event()
	print( '.' )
	# print( 'has_event', ev.has_event )
	# print( ev._button[0], ev._button[1], ev._button[2], ev._button[3], ev._button[4] )
	# print( 'a,b,c,d,e', ev.a, ev.b, ev.c, ev.d, ev.e )
	# print( 'up,down,left,right,clicked', ev.up, ev.down, ev.left, ev.right, ev.click )
	if ev.has_event: # Contains an event for any of the buttons ?
		# Testing UP button
		if ev.up_events.has_event:
			print( 'UP' )
			if ev.up_events.single_click :
				print( '  +-> Single click')
			if ev.up_events.double_click :
				print( '  +-> Double click')
			if ev.up_events.long_press :
				print( '  +-> long press')
			if ev.up_events.level_changed :
				print( '  +-> level changed')
		# Testing CLICK button
		if ev.click_events.has_event:
			print( 'CLICK' )
			if ev.click_events.single_click :
				print( '  +-> Single click')
			if ev.click_events.double_click :
				print( '  +-> Double click')
			if ev.click_events.long_press :
				print( '  +-> long press')
			if ev.click_events.level_changed :
				print( '  +-> level changed')

	time.sleep(0.250)
