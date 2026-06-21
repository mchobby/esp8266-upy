""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Manipulate pixels on the display

* Repo: https://github.com/mchobbyMCHobby/esp8266-upy/ht1632c.git
* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from ht1632c import HT1632C
from fbtext  import FBText
from font5x4 import Font5X4

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )
font = Font5X4()
text_drawer = FBText( display, display.width, display.height, font )

display.fill( 0 )
# Draw some text on the display FrameBuffer
s = "Hello world!"
w = font.text_width(s)
while True:
	for y_pos in range( 28, -w-1, -1 ):
		display.fill(0)
		text_drawer.text( s, y_pos, 2, 1 ) 
		display.show()
		time.sleep_ms(50)
