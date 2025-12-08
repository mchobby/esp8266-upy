# Infinite LED Pulsing - 
#  * change the cycle after 10 seconds
#  * exit the loop after 20 seconds
#
from ledtls import Pulse
from machine import Pin
import time

led_pin = Pin(25,Pin.OUT)
led = Pulse( led_pin, pulse_ms=1500 )

print( "Start pulsing")
_changed = False
_start = time.ticks_ms()
while True:
	if not(_changed) and (time.ticks_diff( time.ticks_ms(), _start )>10_000):
		print( "Change Pulse rate")
		_changed = True
		led.pulse_ms = 750
	if time.ticks_diff( time.ticks_ms(), _start )>20_000:
		print( "Exit loop")
		break;
	# Call it as often as possible
	led.update()

print("That s all Folks!")