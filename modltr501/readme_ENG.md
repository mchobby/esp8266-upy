[Ce fichier existe également en FRANCAIS](readme.md)

# Use the Ambiant light level sensor LTR-501ALS d'Olimex under MicroPython

The Olimex module do use the LTR-501ALS to read luminosity (light intensity) from 0.01 to 64.000 Lux (64K lux) as well as proximity detector (up to 10cm). With its UEXT connector, the MOD-LTR-501ALS is quite easy to wire on your microcontroler.

![Board MOD-LTR-501ALS](docs/_static/mod-LTR-501ALS.png)

The MOD-LTR-501ALS module feature
* A __I2C bus connectivity__
* Ambiant light level sampling, Proximity detection (up to 10cm)
* An UEXT connector for strong and reliable connexion

# About ESP8266-EVB under MicroPython
Before to use this module, it will be necessary to flash the MicroPython firmware onto the ESP8266.

You can read the steps on our [ESP8266-EVB](https://wiki.mchobby.be/index.php?title=ESP8266-DEV) tutorial (on MCHobby's WIKI, French).


## UEXT connector

On the ESP8266-EVB, the UEXT connector does ship UART, SPI, I2C buses as well as 3.3V power. The UEXT pins to ESP8266 GPIO are described in the following picture.

![UEXT connector](docs/_static/ESP8266-EVB-UEXT.jpg)

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/modltr501")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/modltr501
```

## Library details

__Note__: the library is based on the nice Arduino library produce by Olimex for Arduino.

The `ltr501.py` library offers the following features:

__Membres:__
* `data_ready` : Indicates if the sensor do have some sample ready to read. Return a list with the kind of data available. DR_LUX for luminosity data, DR_PROXIMITY for proximity information.
* `lux` : Read the luminosity value. Returns a (ALS_0, ALS_1) tuple with two ADC values (visible light, infrared light).  
* `proximity` : Read the value comming from proximity sensor. Return a (raw_value, distance_cm) tuple.

__Methods:__
* `who_am_i()` : Component identification LTR-501ALS. Should be 0x80
* `init(...)`  : initialize the sensor with defaults.


__init(...) method__:

`def init( lux_range )`:

Called from the constructor, it is used to set the default sensor value. It also activates the Lux & proximity sensors.
* Lux Sensor (ALS) in Active mode, 64k lux range, Integration 100ms, repeat rate 500ms
* Proximity sensor (PS)) in Active mode, x1 GAIN, 100ms measure rate
* LED IR 60Hz, 50% duty, 50mA, 127 pulses

Parameters:
* __lux_range__ : `LUX_RANGE_64K` dynamic gain from 2 to 64000 Lux, `LUX_RANGE_320` dynamic gain from 0.01 to 320 Lux.


# Wiring

## MOD-LTR-501ALS on ESP8266-EVB
If you have an [UEXT Interface on your Pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT) then you just plug the MOD-RFID1536MiFare with an IDC cable.

Otherwise, you can also use the following Wiring:

![Raccordements](docs/_static/mod-ltr-wiring.png)

# Testing

## MOD-LTR-501ALS example
The following example read raw data and display them into the REPL session.

```from machine import I2C, Pin
from time import sleep
from ltr501 import *

i2c = I2C( sda=Pin(2), scl=Pin(4) )
ltr = LTR_501ALS( i2c ) # Dynamic range from 2 to 64000 Lux

# Constructor for 0.01 to 320 Lux dynamic range
#
# ltr = LTR_501ALS( i2c, lux_range = LUX_RANGE_320 )

while True:
    # Is there some data available?
    dr = ltr.data_ready

    # Luminosity data available ?
    if DR_LUX in dr:
        # read ADC converters ALS_0 & ALS_1.
        l = ltr.lux  

        # ALS_0 should be bisible light
        # ALS_1 should be infrared.
        print( "Lux ALS_0, ALS_1 = ", l )

    # Proximity data available ?
    if DR_PROXIMITY in dr:
        # read raw_value & distance_in_cm
        p = ltr.proximity

        print( "Proximity value, cm =" , p )

    # display separator + waits
    print( '-'*40 )
    sleep( 1 )


print( "That's the end folks")
```

Here the following results:

```
Lux ALS_0, ALS_1 =  (9, 26)
Proximity value, cm = (1382, 3.24866)
----------------------------------------
Lux ALS_0, ALS_1 =  (11, 26)
Proximity value, cm = (1453, 2.90181)
----------------------------------------
Lux ALS_0, ALS_1 =  (12, 25)
Proximity value, cm = (953, 5.34441)
----------------------------------------
Lux ALS_0, ALS_1 =  (13, 25)
Proximity value, cm = (827, 5.95994)
----------------------------------------
Lux ALS_0, ALS_1 =  (13, 25)
Proximity value, cm = (760, 6.28725)
----------------------------------------
Lux ALS_0, ALS_1 =  (14, 25)
Proximity value, cm = (737, 6.39961)
----------------------------------------
Lux ALS_0, ALS_1 =  (14, 26)
Proximity value, cm = (716, 6.5022)
----------------------------------------
Lux ALS_0, ALS_1 =  (14, 27)
Proximity value, cm = (702, 6.57059)
----------------------------------------
```

# Shopping list
* Shop: [UEXT Module MOD-LTR-501ALS](http://shop.mchobby.be/product.php?id_product=1415) module à base de LTR-501ALS
* Shop: [Module WiFi ESP8266 - ESP8266-EVB evaluation board](http://shop.mchobby.be/product.php?id_product=668)
* Shop: [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412)
* Shop: [Console cable](http://shop.mchobby.be/product.php?id_product=144)
