from machine import I2C, Pin
from mcp9808 import MCP9808
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
# i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# Pico
i2c=I2C(1, sda=Pin(6), scl=Pin(7) )
print( "Scan", i2c.scan() )

mcp = MCP9808( i2c=i2c, address=0x1F )
while True:
    print( "%s °C" % mcp.temperature )
    sleep( 1 )
