# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
# In this sample we will:
# * See the screen axes (in related image)
# * Draw a hline (optimized drawing)
#
from machine import SPI,Pin
from ili934x import *

# PYBStick config (idem with PYBStick-Feather-Face)
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.erase()

# Correct positionning
lcd.pixel( 80, 130, YELLOW ) # x=80, y=130
lcd.hline( 81, 130, 20, BLUE )

# Half width of screen
lcd.hline( 0, 160, 120, GREEN )

lcd.hline( 0, 170, 240, PURPLE )
