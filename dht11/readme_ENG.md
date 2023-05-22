[Ce fichier existe aussi en FRANCAIS](readme.md)

# Measure humidity and temperature with DHT11 under MicroPython

Warning: the DHT11 is a entry range sensor offering a very limited accuracy.
The sensor only use the SDA pin of the I2C bus.

* Shop: [DHT11](http://shop.mchobby.be/product.php?id_product=708)
* Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

# Wiring

![Wiring a DHT11](docs/_static/dht11_bb.jpg)

# Testing

```
import machine

# The DHT 11 is already supported in the MicroPython Firmware.
# You cannot wire aother I2C breakout on the same I2C bus.
import dht
d = dht.DHT11( machine.Pin(4) )

d.measure()
d.temperature()
d.humidity()
```

This will produce the following results

![Resultats](docs/_static/dht11_webrepl.jpg)
