"""
  The following demo define the input / output for the PiFace-Digital interface.
  It uses a PYBStick + HAT-FACE (SPI1 + CE0 on S24)

  PiFace has been used for developping and testing the MCP23S017 driver
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

# GPA0..GPA7 as output
for x in range(0, 8):
	mcp.setup(x, Pin.OUT)

# GPB0..GPB7 as input
for x in range(8, 16):
	mcp.setup(x, Pin.IN)

print("Starting blinky output pins")
for gpio in range(0, 8):
	mcp.output(gpio, LEVEL_HIGH ) # LEVEL_HIGH = 1
	time.sleep(1)
	mcp.output(gpio, LEVEL_LOW ) # LEVEL_HIGH = 1

dic = {}
for iter in range( 10 ):
	print( '---[ %i ]----------------------' % iter )
	for gpio in range(8, 16):
		dic["io%s" % gpio] = mcp.input(gpio)
	print(  ", ".join( ["%s=%s" % (kv[0],kv[1]) for kv in dic.items()] ) )
	time.sleep(1)
