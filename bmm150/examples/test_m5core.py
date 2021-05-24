"""  BMM150 3 axis magnetic sensor - M5Stack Stack Gray example.

   Based on M5Stack example:
   https://github.com/m5stack/M5Stack/blob/master/examples/Basics/bmm150/bmm150.ino
"""

from machine import I2C, Pin
import bmm150
import math
import time

# Create I2C bus on M5Stack core
i2c = I2C( sda=Pin(21), scl=Pin(22) )
# BMM150 is used at address 0x10 on M5Stack Core
bmm = bmm150.BMM150( i2c, address=0x10 )
print( 'initialized' )

#TODO still requires code portage from bmm150.ino
