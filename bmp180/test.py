# Using Adafruit BMP180 breakout (ADA1603) with ESP8266 Python
#
# Shop: http://shop.mchobby.be/product.php?id_product=397
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from bmp180 import BMP180
from machine import I2C, Pin

# Do not use the standard pin 5 for SCL because it corrupt the boot sequence
# when using an external power supply
# 
i2c = I2C( sda=Pin(4), scl=Pin(2), freq=20000 )

bmp180 = BMP180( i2c )

# 0 lowest accuracy, fastest  - 3 highest accuracy, slowest
bmp180.oversample_sett = 2 

# pressure at sea level (in millibar * 100)
bmp180.baseline = 101325

def show_values():
    # temperature on the BMP
    temp = bmp180.temperature
    print( "Temperature: %.2f deg.Celcius" % temp )

    p = bmp180.pressure
    print( "pressure: %.2f mbar" % (p/100) )
    print( "pressure: %.2f hPa" % (p/100) )

    # Altitude can be calculeted from the difference of pression 
    # between the sea and "here"
    altitude = bmp180.altitude
    print( "altitude: %.2f m" % altitude )

show_values()
