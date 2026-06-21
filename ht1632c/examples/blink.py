""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Draw rectangle then activates the blink state  					

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
display.rect( display.width-11, 1, 10, 6, 1 )
# Send data to display
display.show()

# Blink rate can only be 0 (disable) or 1..3 (enable)
# Only blink rate available is 0.25sec-ON/0.25sec-OFF blink rate
display.blink_rate=1
