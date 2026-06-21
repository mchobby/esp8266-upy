""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Draw rectangle then activates/deactivates the LEDs

* Repo: https://github.com/mchobbyMCHobby/esp8266-upy/ht1632c.git
* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from ht1632c import HT1632C
import time

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )

# top,left, width,height Color=1
display.rect( 1,1, 10, 6, 1 )
# top,left, width,height Color=1 Fill=1
display.rect( display.width-11, 1, 10, 6, 1 , 1) 
# Send data to display
display.show()

while True:
	# Switch on/off LED powering
	display.power_leds = not display.power_leds
	print( 'LEDs are %s' % ('Powered' if display.power_leds else 'Unpowered') )
	time.sleep( 5 )