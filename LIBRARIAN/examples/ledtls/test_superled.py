# Using the SuperLED class to change the
# LED blinking mode every 10 seconds
#
from ledtls import SuperLed
from machine import Pin, idle
import time

led_pin = Pin(25,Pin.OUT)
led = SuperLed( led_pin ) 

def update_10sec( info ):
	# just perform led updates during 10 seconds
	global led
	print( info )
	start = time.ticks_ms()
	while time.ticks_diff( time.ticks_ms(), start )<10_000:
		led.update()
		idle()


# Standard Heatbeat
led.heartbeat()
update_10sec('heartbeat std')
led.handler.lit_ms = 100 # Handler is a HeartBeat instance
led.handler.pause_ms = 750
update_10sec('heartbeat 100ms / 750ms')
led.pulse()
update_10sec('Pulse Std')
led.handler.pulse_ms = 500
update_10sec('Pulse 500ms')
led.error( error_count= 4 )
update_10sec('Error count 4')
time.sleep(1)

print('return to GPIO control')
led.on()
time.sleep(2)
led.off()
print('That s all Folks!')