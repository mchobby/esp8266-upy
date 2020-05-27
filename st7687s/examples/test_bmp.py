# Read the mpy.bmp file and show it on the DFR0529 2.2" round screen (128x18px)
# using st7687s driver.
#
# Rendering takes 38sec and may be optimized by PyPassing the Display class.
#
# Also use the bmp.py image reader from https://github.com/mchobby/esp8266-upy/blob/master/FILEFORMAT/imglib/bmp.py
#
# See tutorial @ https://github.com/mchobby/esp8266-upy/tree/master/st7687s
#
# Author: Meurisse D. for MCHobby (shop.mchobby.be)
#
from machine import Pin, SPI
from st7687s import ST7687S_Latch
from display import *
from bmp import BmpReader # Reader use almost no memory

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
disp.set_origin( 0, 0 ) # force axis origin @ top-left corner (instead of screen center)

# Convert RGB888 to RGB565
def rgb24_to_rgb16( r,g,b ):
	""" Convert a RGB888 value to RGB565 """
	return (  ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) )

# Open the image file
filename = 'mpy.bmp'
print( "Open %s" % filename )
f = open( filename, "rb" )

# Use the reader to extract the pixel data
bmp = BmpReader( f )

start = time.ticks_ms()
# Transfert the data to memory buffer
for line in range( bmp.height ):
	bmp.seek_pix( (0,line) )
	for col in range(bmp.width):
		disp.pixel( (col, line), rgb24_to_rgb16(*bmp.read_pix()) )
f.close()

#--- Fill Screen ---
print( "Drawing tooks %i ms" % (time.ticks_ms()-start))

print( "That's all folks" )
