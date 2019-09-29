[Ce fichier existe aussi en FRANCAIS](readme.md)

# Measure light with the Adafruit TSL2591 (ADA1980) and MicroPython

This sensor is capable to measure the light intensity from 188µLux et 88,000+ Lux.

![TSL2591 from Adafruit Industrie (ADA1980)](docs/_static/TSL2591-LUX-SEN-02.jpg)
This sensor contains 2 diodes allowing to capture the full light spectrum and the infrared spectrum, wich allows to work with visible light (like human eye).

This sensor is very close from the TSL2561 but offer a very wide measure range  (and have a different interface). It offers a dynamic range of 600,000,000:1!

The main difference with the TSL2561 is that TSL2591 address cannot be modified!

# Wiring

## MicroPython Pyboard

![TSL2591 to MicroPython Pyboard](docs/_static/tsl2591-to-pyboard.jpg)

## Feather ESP8266 under  MicroPython

![TSL2591 to Feather ESP8266 under MicroPython](docs/_static/tsl2591-to-feather-esp8266.jpg)

# Testing

To use this sensor, you need to install the `tsl2591.py` library on the MicroPython board.

The following test code make light intensity reads and show the results (in Lux).

```
from machine import I2C
from tsl2591 import TSL2591

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

tsl = TSL2591( i2c = i2c )
print( "%s lux" % tsl.lux )
```

Using a higher integration time and higher gain allows to obtain a much precise result  (mostly when there is very few light).

```
from machine import I2C
from tsl2591 import *

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Warning: unappropriate integration time (or gain) manipulation can lead
# to completely wrong resultat.
tsl = TSL2591( i2c = i2c )
# tsl.gain =  GAIN_HIGH # x428
# tsl.integration_time = INTEGRATIONTIME_400MS
print( "%s lux" % tsl.lux )
print( "Infrared level (0-65535): %s" % tsl.infrared )
print( "Visible light (0-2147483647): %s" % tsl.visible )
print( "Full spectrum (0-2147483647): %s (visible+IR)" % tsl.full_spectrum )

```

# Ressource and sources
* Source: [MicroPython-adafruit-bundle](https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers) (Adafruit, GitHub)

## Luminosité vs Lux
* 0.002 lux : Nuit par temps clair sans lune.
* 0.2 lux : Minimum de lumière que doit produire un éclairage d'urgence (AS2293).
* 0.5 lux 	Pleine lune par temps clair.
* 3.4 lux : Limite crépusculaire (sombre) au couché du soleil en zone urbaine.
* 50 lux : Eclairage d'un living room
* 80 lux : Eclairage des toilette/Hall
* 100 lux : Journée très sombre/temps très couvert.
* 300 - 500 lux : Levé du soleil, luminosité par temps clair. Zone de bureau correctement éclairée.
* 1,000 lux : Temps couvert; Eclairage typique d'un studio TV
* 10,000 - 25,000 lux : Pleine journée (pas de soleil direct)
* 32,000 - 130,000 lux : Soleil direct

## Adresse I2C
The default addresses are 0x29 et 0x28__ (yes, the both).

## The INT pin
La broche INT is a sensor output that can be configured to send a signal when the light level changes. Check the datasheet for mode informations.

# Where to buy
* [Adafruit TSL2591 (ADA1980)](https://shop.mchobby.be/product.php?id_product=1599) @ MC Hobby
* [Adafruit TSL2591 (ADA1980)](http://shop.mchobby.be/product.php?id_product=238) @ Adafruit
