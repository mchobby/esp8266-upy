# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# This use the font file veram_m15.bin available on the FreeType_generator Project
# located at https://github.com/mchobby/freetype-generator
#
# In this sample we will:
# * Use the font drawer on the ILI934x driver, This approach is quite slower
#   compare to the print() function because is draws to the LCD pixel per pixel
#
from machine import SPI,Pin
from ili934x import *
from fdrawer import *


# PYBStick config (idem with PYBStick-Feather-Face)
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.erase()
lcd.rect( 2,2, lcd.width-4, lcd.height-4, WHITE )

fd = FontDrawer( frame_buffer=lcd, font_name='veram_m15' )
fd.color = GREEN
fd.print_str( "Font Demo", 10, 10 )

fd.print_char( "#", 10, 50 )
