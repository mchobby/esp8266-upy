# Test the DFR0529 2.2" round screen (128x18px) using st7687s driver
#
# See tutorial @ https://github.com/mchobby/esp8266-upy/tree/master/st7687s
#
# Author: Meurisse D. for MCHobby (shop.mchobby.be)
#
from machine import Pin, SPI
from st7687s import ST7687S_Latch
from display import *
from time import sleep

# Color management -> from COLORS/colortls.py
def rgb24_to_rgb16( r,g,b ):
	""" Convert a RGB888 value to RGB565 """
	return (  ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) )

# Define the needed PINs
# Pyboard:
SPI_BUS = 2
CS  = "X1"
RS  = "X3" # Mode commande
WR  = "X4"
LCK = "Y5"

spi = SPI( SPI_BUS, polarity=0, phase=0) # mode 0: CPOL=0, CPHA=0
cs = Pin(CS, Pin.OUT ) # Disable slave
rs = Pin(RS, Pin.OUT ) # Command mode
wr = Pin(WR, Pin.OUT )
lck= Pin(LCK,Pin.OUT )

lcd = ST7687S_Latch( spi, cs,  rs, wr, lck)
disp = Display( lcd, 128, 128 ) # Display offers drawing right in the display's BufferMemory

#--- Switch on/off the LCD ---
for i in range(5):
	lcd.turn_on(False)
	sleep(0.4)
	lcd.turn_on(True)
	sleep(0.4)

#--- Fill Screen ---
disp.clear( rgb24_to_rgb16(255,0,0) ) # Red

print( "Part 1" )
disp.clear( 0x0000 ) # Black
disp.circle( (0, 0), 20, DISPLAY_GREEN) # draw circle at (0, 0) and radius = 20
disp.rect ( (-20,-30) , 40, 60, DISPLAY_CYAN ) # draw rectangle at (-20, -30), width = 40, height = 60
disp.line ( (-64,-64) , (64,64), DISPLAY_RED);  # draw line at (-64, -64) to (64, 64)
for y in range(-64,64,3):
	disp.line( (-64,64), (64,y), DISPLAY_PINK )
disp.hline( (-64, 0), 128, DISPLAY_WHITE)   # draw horizontal line at (-64, 0), length = 128
disp.vline( (0, -64), 128, DISPLAY_WHITE)   # draw vertical line at (0, -128), length = 128

print( "Part 2" )
disp.clear( DISPLAY_LIGHTGREY )
disp.triangle( (-20,-50), (0,0), (50,20), DISPLAY_ORANGE ) #draw triangle with 3 point coordinates (-20, -50), (0, 0), (50, 20)
disp.circle( (0, 0) , 20, DISPLAY_GREEN) # draw circle at (0, 0) and radius = 20
disp.fill_circle( (0,0) , 20, DISPLAY_GREEN)
disp.fill_rect( (-20,-20), 40, 40, DISPLAY_CYAN) # (-20, -30), width = 40, height = 60
disp.fill_triangle( (-20,-50), (-20,0), (50,20), DISPLAY_ORANGE )
