# Test display of text on
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

disp.clear( )
disp.text_fg = DISPLAY_WHITE # set text color to white
disp.text_bg = DISPLAY_BLACK # set text background to black
disp.text_size = 1
disp.set_cursor( (-45,-30) )
disp.print("Is this running")
disp.text_size = 2 			 # 2 * text size, default text size: 6 * 8
disp.set_cursor( (-64,-10) ) # set text position to center (in absolute position)
disp.print("MicroPython")
disp.text_size = 3 			 # 2 * text size, default text size: 6 * 8
disp.set_cursor( (-10,25) )   # set text position to center (in absolute position)
disp.print("?")
