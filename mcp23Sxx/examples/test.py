"""
The following demo periodically toggles the level of all pins of two MCP23S17 (SPI components).
"""

from mcp23Sxx import *
from machine import SPI, Pin
import time

# PYB405: SPI Device for PYB405
spi = SPI( 2 ) # SCLK=Y6 (#23), MISO=Y7 (#21), MOSI=Y8 (#19)

# PYB405: Chip Select on SPI_CE0
cs = Pin( 'Y11', Pin.OUT ) # SPI_CE0=Y11 (#24)
cs.value( 1 )

# MCP23S17 - SPI GPIO extender
mcp = MCP23S17( spi, cs ) # default: device_id=0x00

for x in range(0, 16):
	mcp.setup(x, Pin.OUT)

print("Starting blinky on all pins (CTRL+C to quit)")
while (True):
	for gpio in range(0, 16):
		mcp.output(gpio, True )
	time.sleep(1)

	for gpio in range(0, 16):
		mcp.output(gpio, False)
	time.sleep(1)
