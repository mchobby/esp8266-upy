from machine import I2C
from tsl2591 import TSL2591

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2) 
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

tsl = TSL2591( i2c = i2c )
print( "%s lux" % tsl.lux )
