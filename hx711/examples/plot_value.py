# plot_value.py - tare the sensor then read_value(). Send elapse_time_ms + coma + read_value() to REPL output.
#                 Wait for a minimal value on the sensor to output data. 
#                 Script is halted when values fallback under the minimal value.
#                 Pico LED (GPIO25) Lits while logging.
#
# Ideal to plot content to spreadsheet.
#
#
# more information on  https://github.com/mchobby/esp8266-upy/tree/master/hx711 
#
from hx711_gpio import HX711
from machine import Pin
import time

MINIMAL_VALUE = 200 # Minimal value to start logging

led = Pin( 25, Pin.OUT, value=0 ) # Light LED while logging

pin_OUT = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(13, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT, gain=128)
# hx711.set_gain( 128 )   # Change the gain
# hx711.set_scale( 1 )    # Default scale is 1

hx711.tare()

# Wait for a minimal value to start logging
print( 'Wait for minimal value to start logging...' )
while True:
	if hx711.get_value() > MINIMAL_VALUE:
		break

led.on()
start = time.ticks_ms()
while True:
	# Raw value of load cell. Not scaled, no offset compensation
	#print( "read: ", hx711.read() )
	val = hx711.get_value()
	print( "%i,%i" % (time.ticks_diff( time.ticks_ms(), start ), val ) )
	# Stop is fall under minimal value
	if val < MINIMAL_VALUE:
		break
	time.sleep_ms( 200 )

led.off()
print( 'logging endWait for minimal value to start logging...' )
