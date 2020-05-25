# Test execution speed of fill_screen and optimized clear on
#    DFR0529 2.2" round screen (128x18px) using st7687s driver
#
# See tutorial @ https://github.com/mchobby/esp8266-upy/tree/master/st7687s
#
# Author: Meurisse D. for MCHobby (shop.mchobby.be)
#
from machine import Pin, SPI
from st7687s import ST7687S_Latch
from display import *
import time

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

#--- Fill Screen ---
start = time.ticks_ms()
disp.fill_screen( DISPLAY_RED )
print( "fill_screen tooks %i ms" % (time.ticks_ms()-start))

#--- Optimized version ---
start = time.ticks_ms()
disp.clear( color=DISPLAY_WHITE )
print( "clear tooks %i ms" % (time.ticks_ms()-start))

print( "That's all folks" )
