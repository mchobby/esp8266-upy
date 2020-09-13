"""
The following demo periodically toggles the level of all pins of two MCP23S17 (SPI components).

THIS AS NOT BEEN TESTED YET!
"""

from RPiMCP23S17 import MCP23S17
import time

# you might also want to use the parameters bus, pin_cs, or pin_reset
# to match your hardware setup
mcp1 = MCP23S17.MCP23S17(device_id=0x00)
mcp2 = MCP23S17.MCP23S17(device_id=0x01)

for x in range(0, 16):
    mcp1.setup(x, mcp1.OUT)
    mcp2.setup(x, mcp1.OUT)

print("Starting blinky on all pins (CTRL+C to quit)")
while (True):
    for x in range(0, 16):
        mcp1.digitalWrite(x, MCP23S17.MCP23S17.LEVEL_HIGH)
        mcp2.digitalWrite(x, MCP23S17.MCP23S17.LEVEL_HIGH)
    time.sleep(1)

    for x in range(0, 16):
        mcp1.digitalWrite(x, MCP23S17.MCP23S17.LEVEL_LOW)
        mcp2.digitalWrite(x, MCP23S17.MCP23S17.LEVEL_LOW)
    time.sleep(1)
