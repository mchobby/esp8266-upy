# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# Test the print() function available on the driver ON Olimex's 2.8" TFT display
#
# The print() function relies on the FontDrawer and the font file veram_m15.bin
# (available on the FreeType_generator Project located at
# https://github.com/mchobby/freetype-generator )
#
# See also the "test_fdrawer.py" offering better performance.
#
# In this sample we will:
# * Use the font drawer on the ILI934x driver
#
from machine import SPI
from machine import Pin
from ili9488 import *

# Pico + ILI9488 requires RESET pin to work properly
spi = SPI( 1, baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(9, Pin.OUT, value=1 )
dc_pin = Pin(12, Pin.OUT )
rst_pin = Pin(13, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=480, r=0)
lcd.fill( color565( 30, 35, 128) ) # a shade of blue
print( "Assign font")
lcd.font_name = 'veram_m15'
print( "font loaded")
lcd.print("123")
# Use the inner print() statement if tge driver
#lcd.print( "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890" )
#lcd.color = GREEN
#lcd.print( "Lorem ipsum dolor sit amet, consectetur adipiscing elit." )
#lcd.color = BLUE
#lcd.print( "Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor." )
#lcd.color = YELLOW
#lcd.print( "Cras elementum ultrices diam" )

print( "That all done")
