# Mesure de lumière avec Adafruit TSL2561 (ADA439) et ESP8266 MicroPython

* Shop: [Adafruit BMP180 (ADA1603)](http://shop.mchobby.be/product.php?id_product=397)
* Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from tsl2561 import *
from machine import I2C, Pin

# Do not use the standard pin 5 for SCL because it corrupt the boot sequence
# when using an external power supply
# 
i2c = I2C( sda=Pin(4), scl=Pin(2), freq=20000 )

tsl = TSL2561( i2c )
# Read the sensor.
#   This will automatically activate the sensor (which take some time)
#   perform the reading then deactive the sensor.
#   May return a value like 6.815804 Lux
print( tsl.read() )

# Note: you can call active(True/False) to manually
# handle the activation of the sensor.

# You can change the gain and the integration time
# * Gain can be 1 or 16
# * Integration_time 0 or 13 or 101 or 402 (0=manual)
tsl.gain( 16 )
tsl.integration_time( 402 )

# You can also configure AutoGain selection
# but you cannot have a manual integation time
tsl.integration_time( 402 )
print( tsl.read(autogain=True) )


