# Simple test of infinite LED Pulsing
#
from ledtls import Pulse
from machine import Pin

led_pin = Pin(25,Pin.OUT)
led = Pulse( led_pin ) # pulse_ms = 2000
# led = Pulse( led_pin, pulse_ms=500 )

while True:
	# Call it as often as possible
	led.update()