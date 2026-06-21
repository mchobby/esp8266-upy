""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Manipulate pixels on the display

* Repo: https://github.com/mchobbyMCHobby/esp8266-upy/ht1632c.git
* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from ht1632c import HT1632C

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )

# Light all LEDs Color=1
display.fill( 1 )
# Light Off x=1 (second row), y=0 (first row), color=0
display.pixel( 1, 0, 0) 
# Light Off bottom right pixel
display.pixel( 23, 7, 0)
# Send data to display
display.show()