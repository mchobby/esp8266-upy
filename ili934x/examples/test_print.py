# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# Test the print() function available on the driver.
# The print() function relies on the FontDrawer and the font file veram_m15.bin
# (available on the FreeType_generator Project located at
# https://github.com/mchobby/freetype-generator )
#
# See also the "test_fdrawer.py" offering better performance.
#
# In this sample we will:
# * Use the font drawer on the ILI934x driver
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
lcd.font_name = 'veram_m15'

# Use the inner print() statement if tge driver
lcd.print( "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890" )
#lcd.color = GREEN
lcd.print( "Lorem ipsum dolor sit amet, consectetur adipiscing elit." )
#lcd.color = BLUE
lcd.print( "Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor." )
#lcd.color = YELLOW
lcd.print( "Cras elementum ultrices diam" )
