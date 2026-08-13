""" HOLTEK HT1632C library for MicroPython

  DFRobot DFR0487 : Manipulate pixels on the display

* Font Repo: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
* HT1632C Repo: https://github.com/mchobby/esp8266-upy/tree/master/ht1632c

* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from ht1632c import HT1632C
from fbtext  import FBText
from font8x4 import Font8X4

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )
text_drawer = FBText( display, display.width, display.height, Font8X4() )

display.fill( 0 )
# Draw some text on the display FrameBuffer
text_drawer.text( "Hello", 0, 0, 1 ) 
# Send data to display
display.show()