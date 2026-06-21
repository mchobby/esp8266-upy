""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Draw rectangle then manipulate the display
  					brightness

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
display.rect( 1,1, display.width-2, display.height-2, 1 )
display.rect( 3,3, display.width-6, display.height-6, 1 )
# Send data to display
display.show()

while True:
	for i in range(11): # 0..10
		display.brightness=i/10
		time.sleep_ms(100)
	for i in range( 9, 0, -1 ): #9..0
		display.brightness=i/10 
		time.sleep_ms(100)