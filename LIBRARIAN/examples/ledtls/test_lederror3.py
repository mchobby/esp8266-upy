# Test of infinite LED error display until an external condition is meet.
#
# Use the LEDError callback to check if external condition is meet
#
from ledtls import LedError
from machine import Pin
import time

led_pin = Pin(25,Pin.OUT)

def exit_error_cb( obj ):
	# exits after 20 seconds
	return time.ticks_diff( time.ticks_ms(), start ) > 20_000
led = LedError( led_pin, exit_cb=exit_error_cb )

print( "Start Led Error display")
start = time.ticks_ms()
led.set( error_count=3 )
print( "Finished" )
