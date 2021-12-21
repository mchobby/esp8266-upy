"""
Grove 5 Way Switch - test the RAW MODE for Grove5Way class driver (SeeedStudio)

See https://github.com/mchobby/esp8266-upy/tree/master/grove-5-way-switch

"""
from machine import I2C
from grove5way import Grove5Way
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

sw = Grove5Way( i2c )
print( 'versions    :', sw.device_version() ) # return the 10 bytes of version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( 'event mode  :', 'RAW')

# Using lambda expression to associate a test on event object with the
# text to display.
text_n_test = { 'Up'     : lambda ev : ev.up,
				'Down'   : lambda ev : ev.down,
				'Left'   : lambda ev : ev.left,
				'Right'  : lambda ev : ev.right,
				'CLICK!' : lambda ev : ev.click }

while True:
	ev = sw.get_event()
	print( '.' )
	# print( 'has_event', ev.has_event )
	# print( 'a,b,c,d,e', ev.a, ev.b, ev.c, ev.d, ev.e )
	# print( 'up,down,left,right,clicked', ev.up, ev.down, ev.left, ev.right, ev.click )
	if ev.has_event:
		# Smart way to test ev.up(), ev.down, ...
		for text, test in text_n_test.items():
			if test( ev ):
				print( text )
	time.sleep(0.250)
