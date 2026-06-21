""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Manipulate pixels on the display

* Repo: https://github.com/mchobbyMCHobby/esp8266-upy/ht1632c.git
* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from ht1632c import HT1632C
from fbtext import FBText
from font8x4 import Font8X4
import time

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )
text_drawer = FBText( display, display.width, display.height, Font8X4() )

while True:
	for y_pos in range( 8, -9, -1 ):
		display.fill( 0 )
		text_drawer.text( "Hello", 0, y_pos, 1 ) 
		display.show()
		time.sleep_ms(50)

	time.sleep( 0.5 )

	for x_pos in range( 25, -26, -1 ):
		display.fill( 0 )
		text_drawer.text( "World", x_pos, 0, 1 ) 
		display.show()
		time.sleep_ms(50)

	time.sleep( 0.1 )
