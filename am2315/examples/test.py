# Using AM2315 I2C temperature/humidity sensor (ADA2315) with ESP8266 under MicroPython
#
# Shop: http://shop.mchobby.be/product.php?id_product=932
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from am2315 import *
from machine import I2C, Pin

# Do not use the standard pin 5 for SCL because it corrupt the boot sequence
# when using an external power supply
# 
i2c = I2C( sda=Pin(4), scl=Pin(2), freq=20000 )

a = AM2315( i2c = i2c )

def show_values():
    if a.measure():
       print( a.temperature() )
       print( a.humidity() )

# Two consecutives read are sometime needed to properly update
# the readed values.
show_values()
time.sleep( 1 )
show_values()

