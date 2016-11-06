# Using a DHT11 Humidity/Temperature sensor with ESP8266 Python
#
# Shop: http://shop.mchobby.be/product.php?id_product=708
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython
#

import machine

# DHT 11 is already supported by the MicroPython FirmWare
# It is not compatible with other I2C breakout (wired on the same bus)
import dht
d = dht.DHT11( machine.Pin(4) )

d.measure()
d.temperature()
d.humidity()
