"""
The following demo periodically toggles the level of all pins of two MCP23S17 (SPI components).

THIS AS NOT BEEN TESTED YET!
"""

from mcp23Sxx import MCP23S17
from machine import Pin
import time

# you might also want to use the parameters bus, pin_cs, or pin_reset
# to match your hardware setup
mcp1 = MCP23S17(device_id=0x00)
mcp2 = MCP23S17(device_id=0x01)

for x in range(0, 16):
    mcp1.setup(x, Pin.OUT)
    mcp2.setup(x, Pin.OUT)

print("Starting blinky on all pins (CTRL+C to quit)")
while (True):
    for x in range(0, 16):
        mcp1.output(x, True)
        mcp2.output(x, True)
    time.sleep(1)

    for x in range(0, 16):
        mcp1.output(x, False)
        mcp2.output(x, False)
    time.sleep(1)
