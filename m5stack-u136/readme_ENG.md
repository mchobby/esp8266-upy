Ce fichier existe également en [Français ici](readme.md)

# Using an I2C Grove BH1750FVI Ambiant Light Unit (U136/U134) with MicroPython

DLight Unit is a Digital Ambient Light Sensor. Adopts BH1750FVI sensor (I2C interface), integrates 16-bit ADC, supports wide-range LUX and high resolution (1 - 65535 LX). Compact in size, and low power consumption. Suitable for various light sensing applications.

![M5Stack u136 I2C Ambiant Light Sensor with Grove interface](docs/_static/u136.jpg)

* Support light source variations (incandescent, fluorescent, halogen, white LED, sunlight, etc)
* Wide Range LUX (1-65535 lux)

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/m5stack-u136")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/m5stack-u136
```

# Wiring

The sensor  can be powered with 3.3V or 5V power supply.

The SDA / SCL data lines are at 3.3V level.

## Ambiant Light I2C sensor with Raspberry-Pi Pico

![ALight I2C to Raspberry-Pi Pico](docs/_static/u136-to-pico.jpg)

# Test

The [dlight.py](lib/dlight.py) library must be copied on your MicroPython microcontroler.

## Reading the Ambiant Light Sensor

The [test.py](examples/test.py) script do reads the sensor value every 100ms.

``` python
from machine import I2C
from dlight import *
from time import sleep

# Pico - I2C(1) - sda=GP6, scl=GP7
i2c = I2C(1)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

ambiant = AmbiantLight(i2c)
# Set the mode
ambiant.set_mode( CONTINUOUSLY_H_RESOLUTION_MODE )
while True:
	print( 'Light: %i Lux' % ambiant.lux )
	sleep( 0.200 )
```

Please note that the mode can have the following values:
* CONTINUOUSLY_H_RESOLUTION_MODE
* CONTINUOUSLY_H_RESOLUTION_MODE
* CONTINUOUSLY_H_RESOLUTION_MODE2
* CONTINUOUSLY_L_RESOLUTION_MODE
* ONE_TIME_H_RESOLUTION_MODE
* ONE_TIME_H_RESOLUTION_MODE2
* ONE_TIME_L_RESOLUTION_MODE

Constant and behavior described in the [BH1750FVI datasheet (see detail of the product)](https://shop.mchobby.be/product.php?id_product=2444).
