# Display the error for a while then RESET it
# * Display LED Error for 10 seconds
# * Stop the demonstration after 20 seconds
#
from ledtls import LedError
from machine import Pin
import time

led_pin = Pin(25,Pin.OUT)
led = LedError( led_pin )

print( "Starting LED error" )
led.set( error_count=3 )
start = time.ticks_ms()
_resets = False
while True:
	# Call it as often as possible
	led.update()
	# Reset the error after 10 seconds
	if (_resets==False) and (time.ticks_diff(time.ticks_ms(),start)>10_000):
		print( "RESET led error" )
		_resets=True
		led.reset()
	# Exit the loop() after 20 seconds
	if time.ticks_diff(time.ticks_ms(),start)>20_000:
		print( "Exit the loop()" )
		break;

print( "That's all folks!" )