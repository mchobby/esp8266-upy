"""
Grove 6 DIP Switch - test the EVENT MODE for Grove6Dip class driver (SeeedStudio)

See https://github.com/mchobby/esp8266-upy/tree/master/grove-5-way-switch

Remark: I do not have 6 DIPs module so the code has not been tested yet

"""
from machine import I2C
from grove6dip import Grove6Dip
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

sw = Grove6Dip( i2c )
sw.set_event_mode( True )
print( 'versions    :', sw.device_version() ) # return the 10 bytes of version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( 'event mode  :', 'EVENT')
print( '' )
print( 'Current State')
ev = sw.get_event()
for dip_nr in range(1, sw.switch_count+1): # 1..6
	print( 'DIP %i' % dip_nr, 'ACTIVATED' if ev.dip( dip_nr ) else 'deactivated' )
print( '' )
print( 'Now, play with the DIPs')

while True:
	ev = sw.get_event()
	#print( ev.dip(1) )

	if ev.has_event: # Contains an event for any of the buttons ?
		for dip_nr in range (1, sw.switch_count+1): # 1..6
			# Testing DIP event
			if ev.dip_events( dip_nr ).has_event:
				print( 'DIP %i' % dip_nr, 'has event' )
				# Describe the events (only level_changed applies to DIP)
				if ev.dip_events( dip_nr ).level_changed :
					print( '  +-> level changed')

				# Getting the changed state (by reading raw value)
				#    Remark: Not prove to work. A new sw.get_event() may be necessary to get updated state
				print( 'DIP %i' % dip_nr, 'ACTIVATED' if ev.dip( dip_nr ) else 'deactivated' )

	time.sleep(0.250)
