# Simple test of infinite LED error display
#
from ledtls import LedError
from machine import Pin

led_pin = Pin(25,Pin.OUT)
led = LedError( led_pin )

led.set( error_count=3 )
while True:
	# Call it as often as possible
	led.update()