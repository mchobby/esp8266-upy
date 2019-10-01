from machine import I2C
from mcp4725 import MCP4725
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

mcp = MCP4725( i2c = i2c )
while True:
	# Make a ramp as fast as possible
	for i in range( 65535 ): # 16 bits
		mcp.value = i
