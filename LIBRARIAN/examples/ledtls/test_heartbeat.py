# Simple test of infinite HeartBeat
#
from ledtls import HeartBeat
from machine import Pin

led_pin = Pin(25,Pin.OUT)
led = HeartBeat( led_pin ) # 50ms every 2 seconds
#led = HeartBeat( led_pin, lit_ms=50, pause_ms=200 )

while True:
	# Call it as often as possible
	led.update()