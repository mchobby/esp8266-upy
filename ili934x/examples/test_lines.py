# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
# In this sample we will:
# * See the screen axes (in related image)
# * Draw arbitrary lines
#
from machine import SPI,Pin
from ili934x import *

# PYBStick config (idem with PYBStick-Feather-Face)
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

# Raspberry-Pi Pico
# spi = SPI( 0 )
# cs_pin = Pin(5) # GP5
# dc_pin = Pin(3) # GP3
# rst_pin = None

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.erase()

colors = [NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE, LIGHTGREY,
		DARKGREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE, ORANGE,
		GREENYELLOW ]
color_count = len( colors )

for y in range( lcd.height//3 ):
	lcd.line( 0,0, lcd.width, y*3, colors[y % color_count] )

for x in range( lcd.width//3 ):
	lcd.line( 0,0, lcd.width-(x*3), lcd.height, colors[x % color_count] )
