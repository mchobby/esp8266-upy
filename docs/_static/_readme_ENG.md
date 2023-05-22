[Ce fichier existe également en FRANCAIS](readme.md)

# Plateform Agnostic MicroPython Driver

Initially, this collection of driver + wiring were created for ESP8266 running under MicroPython. The reason for this repository "esp8266-upy" name.

Since, the collection widely evolved and drivers are written to work independently from the target [MicroPython plateform](https://shop.mchobby.be/fr/56-micropython).

![PLateform Agnostic MicroPython Driver](docs/_static/PAM-driver.jpg)

__MIP ready!__ The libraries can be installed with the [MIP Tool](https://docs.micropython.org/en/latest/reference/packages.html) (__MicroPython Install Package__).

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explore it by:
* Interface:
@@interface_list:{'lang_code':'eng','str':'[%code%](docs/indexes/drv_by_intf_%code%_ENG.md)'} # List per interface

* Manufacturer:
@@manufacturer_list:{'lang_code':'eng','str':'[%code%](docs/indexes/drv_by_man_%code%_ENG.md)'} # List per manufacturer

@@driver_table:{'lang_code':'eng'} # Insert the driver table

# Ressources
* [__Wiki about MicroPython on ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython), a french support to learn how to flash an ESP with MicroPython.
* [__GitHub dedicated to the Pyboard__](https://github.com/mchobby/pyboard-driver) with other drivers requiring more ressources. https://github.com/mchobby/pyboard-driver.
* Where to buy - https://shop.mchobby.be


There are many Adafruit  drivers (various plateforms) on this Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

And some IMU (inertial sensor) driver on Github
* https://github.com/micropython-IMU/
