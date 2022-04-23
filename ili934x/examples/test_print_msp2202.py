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
from ili934x import *

# PYBStick config requires Bit-Banging one-way SPI for Olimex.
# MISO (S26) of standard UEXT connector is used for D/C.
# SPI must declare a MISO! So we used a unused in the project (S16 in this case) as fake pin
# spi = SPI( -1, mosi=Pin("S19", Pin.OUT), miso=Pin("S16", Pin.IN), sck=Pin("S23", Pin.OUT) )
# cs_pin = Pin("S26")
# dc_pin = Pin("S21")
# rst_pin = None

# PICO config requires Bit-Banging one-way SPI for Olimex.
# MISO (GP4) of standard UEXT is used for D/C.
# SPI must declare a MISO! So we used a unused MISO pin in the project (GP0 in this case) as fake pin
# spi = SPI( 0, mosi=Pin(7, Pin.OUT), miso=Pin(16, Pin.IN), sck=Pin(6, Pin.OUT) )
# cs_pin = Pin(5) # GP5
# dc_pin = Pin(4) # GP4 (the miso pin)
# rst_pin = None

# Pico + MSP2202 requires RESET pin to work properly
spi = SPI( 0, baudrate=40000000 ) # 40 Mhz
cs_pin = Pin(10, Pin.OUT, value=True)
dc_pin = Pin(9, Pin.OUT)
rst_pin = Pin(15, Pin.OUT, value=1)
# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.fill( color565( 20, 255, 10) ) # a shade of Green
lcd.font_name = 'veram_m15'

# Use the inner print() statement if tge driver
lcd.print( "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890" )
#lcd.color = GREEN
lcd.print( "Lorem ipsum dolor sit amet, consectetur adipiscing elit." )
#lcd.color = BLUE
lcd.print( "Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor." )
#lcd.color = YELLOW
lcd.print( "Cras elementum ultrices diam" )
