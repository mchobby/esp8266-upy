from machine import I2C
from mcp4725 import MCP4725
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

mcp = MCP4725( i2c = i2c )
# Set the output to VDD/2 (so 3.3/2 = 1.65V)
# Value is 16 bits, 0 to 65535
mcp.value = int(65535/2)
print( "Output @ 1.65v")
