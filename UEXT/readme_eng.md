[Ce fichier existe également en FRANCAIS ici](readme.md)

# What's the UEXT Olimex's EcoSystem ?

[Olimex](https://www.olimex.com/) create lot of microcontroler and nano-computer boards (eg: OlinuXino). Their products are usually fitted with UEXT (IDC 10) connector that ship the following signals:
* A __3.3V power supply line__,
* An __3.3v I2C__ bus,
* An __3.3v SPI__ bus,
* An __3.3v UART__.

This connector have many-many sensor board and extension board named __UEXT Modules__ designed by Olimex (see [here @ MCHobby](https://shop.mchobby.be/fr/138-uext) or [there @ Olimex](https://www.olimex.com/Products/Modules/) ).

A large part of those UEXT Modules uses the I2C bus, which helps in using the sensor modules with ESP8266 boards since only 2 lines are needed to communicate this the module.

# UEXT connector of Olimex's ESP8266
![UEXT connector on Olimex's ESP8266](ESP8266-EVB-UEXT.jpg)

Create an instance of I2C bus on the UEXT connector with MicroPython

```
from machine import Pin, I2C

i2c = I2C( sda=Pin(2), scl=Pin(4) )
```

__Note :__ the UART line is attached on the REPL session on the Pyboard

# Use UEXT of an Olimex's ESP8266-EVB
Here is an example of wiring and usage of the UEXt ecosysteme with the [ESP8266-EVB board](https://shop.mchobby.be/fr/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html).

In this example, we use the LTR-501ALS sensor (evaluate ambiant light) with UEXT connector and a [console cable](https://shop.mchobby.be/fr/raspberry-pi-3/144-cable-usb-vers-ttl-serie-3232100001442.html) used to communicate with the ESP via the UART.

![Using the UEXT connector](mod-ltr-wiring.png)
