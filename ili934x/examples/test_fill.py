# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
# In this sample we will:
# * See the screen axes (in related image)
# * Draw a single pixel
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
# Compose a color
red = color565(255,0,0)
# Fill the screen
lcd.fill( red )
