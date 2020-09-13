"""
  The following demo based on test_piface.py for the PiFace-Digital interface.
  It uses a PYBStick + HAT-FACE (SPI1 + CE0 on S24)

  Reads multiples inputs at once.
"""

from mcp23Sxx import *
from machine import SPI, Pin
import time

# PYBStick / PYBStick-HAT-FACE
spi = SPI( 1, phase=0, polarity=0, baudrate=400000 ) # SCLK=S23, MISO=S21, MOSI=S19

# PYBStick / PYBStick-HAT-FACE
cs = Pin( 'S24', Pin.OUT, value=True ) # SPI_CE0=S24

# MCP23S17 - SPI GPIO extender
mcp = MCP23S17( spi, cs ) # default: device_id=0x00

# GPB0..GPB7 as input
for x in range(0, 8):
	mcp.setup(x, Pin.OUT)

d1 = {0:True,1:False,2:True,3:False,4:True,5:False,6:True,7:False}
d2 = {0:False,1:True,2:False,3:True,4:False,5:True,6:False,7:True}
for iter in range( 10 ):
	print( '---[ %i ]--- Write GPIO 8,9,10,11,12,13,14,15 ----' % iter )
	print( mcp.output_pins( d1 ) )
	time.sleep(1)
	print( mcp.output_pins( d2 ) )
	time.sleep(1)
print("That s all Folks")
