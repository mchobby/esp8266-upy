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

def dump_font_buffer( lcd ):
	print( "Dump Font framebuffer" )
	for x in range( lcd.width ):
		v = ''
		for y in range( lcd.font.font.height ):
			v = ('X' if lcd.font.fb.pixel(x,y) else '.') +v

		if len(v.replace('.',''))==0:
			iEmpty += 1
		else:
			iEmpty = 0

		if iEmpty == 5:
			print( 'skipping empty lines')
		if iEmpty > 5:
			continue
		print( v )


# Pico + ILI9488 requires RESET pin to work properly
spi = SPI( 0, miso=Pin.board.GP4, mosi=Pin.board.GP7, sck=Pin.board.GP6, baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(5, Pin.OUT, value=1 )
dc_pin = Pin(3, Pin.OUT )
rst_pin = Pin(2, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=480, r=3)
lcd.fill( color565( 30, 35, 128) ) # a shade of blue
print( "Assign font")
lcd.font_name = 'veram_m15'
print( "font loaded")

# Using default colot (WHITE)
lcd.print("123")
# Dump Font framebuffer
# dump_font_buffer( lcd )

lcd.hline( 0, lcd.height//2, lcd.width, WHITE )

# Use the inner print() statement if tge driver
lcd.print( "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890" )
lcd.color = GREEN
lcd.print( "Lorem ipsum dolor sit amet, consectetur adipiscing elit." )
lcd.color = BLUE
lcd.print( "Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor." )
lcd.color = YELLOW
lcd.print( "Cras elementum ultrices diam" )

print( "That all done")
