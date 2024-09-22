
# test.py - tare the sensor then read() the raw value and read_value() the IIR Low-pass Filter raw value. 
#           The interesting value is get_value() that can later be used with scale and get_units.
# 
# This script is a good starting point to learn values returned by the sensor.
#
#
# more information on  https://github.com/mchobby/esp8266-upy/tree/master/hx711 
#
from hx711_gpio import HX711
from machine import Pin
import time

pin_OUT = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(13, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT, gain=128)
# hx711.set_gain( 128 )   # default gain is 128 (or 64)
# hx711.set_scale( 1 )    # Default scale is 1

hx711.tare()
while True:
	print( "---------------------------------" )
	# Raw value of load cell. Not scaled, no offset compensation
	print( "read: ", hx711.read() )
	print( "get_value: ", hx711.get_value() )
	time.sleep_ms( 500 )
