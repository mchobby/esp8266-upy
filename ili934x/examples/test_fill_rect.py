# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
# In this sample we will:
# * See the screen axes (in related image)
# * Draw arbitrary lines
#
from machine import SPI,Pin
from ili934x import *
import urandom

# PYBStick config (idem with PYBStick-Feather-Face)
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.erase()

colors = [NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE, LIGHTGREY,
		DARKGREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE, ORANGE,
		GREENYELLOW ]
color_count = len( colors )

for i in range(100):
	lcd.fill_rect( urandom.randint(0,lcd.width-1), urandom.randint(0,lcd.height-1),
				urandom.randint(1,50), urandom.randint(1,50),
				colors[urandom.randint(0,color_count-1)] )
