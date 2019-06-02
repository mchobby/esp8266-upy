[Ce fichier existe également en FRANCAIS](readme.md)

# ESP8266 MicroPython Driver

This is a collection of drivers (and wiring) for various board, breakout and connectors used with an __ESP8266 under MicroPython__.

IF it works with the ESP8266 THEN it will also run with the [MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython) or any other MicroPython boards!

![ESP8266 and Pyboard](docs/_static/ESP8266-to-PYBOARD.jpg)

The most easiest plateform to flash with MicroPython are the [Feather ESP8266 HUZZA ADA2821](http://shop.mchobby.be/product.php?id_product=846) or an [ESP8266-EVB evaluation board from Olimex](https://shop.mchobby.be/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html) or a [WEMOS / LOLIN (ESP modules) boards](https://shop.mchobby.be/fr/123-wemos-lolin-esp)

![Feather ESP8266](docs/_static/FEAT-HUZZA-ESP8266-01.jpg)
![Olimex ESP8266 Evaluation Board](docs/_static/ESP8266-EVB.jpg)
![Wemos D1 (ESP8266)](docs/_static/WEMOS-D1.jpg)

# Other information source
* [__Wiki about MicroPython on ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython), a french support to learn how to flash an ESP with MicroPython.
* [__GitHub dedicated to the Pyboard__](https://github.com/mchobby/pyboard-driver) with other drivers requiring more ressources. https://github.com/mchobby/pyboard-driver.
* Where to buy - https://shop.mchobby.be

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explorer par:
* Interface:
@@interface_list:{'lang_code':'eng','str':'[%code%](docs/drv_by_intf_%code%_ENG.md)'} # List per interface

* Fabriquant:
@@manufacturer_list:{'lang_code':'eng','str':'[%code%](docs/drv_by_man_%code%_ENG.md)'} # List per manufacturer

@@driver_table:{'lang_code':'eng'} # Insert the driver table

# Some useful information
* [how-to-install-upy.md](how-to-install-upy.md) how to install MicroPython on ESP8266 from a Linux machine (like the Raspberry-Pi)
 * [erase-esp8266.sh](erase-esp8266.sh) - used to erase the flash from the ESP8266
 * [burn-esp8266.sh](burn-esp8266.sh) - used to flash the [MicroPython binary downloaded from micropython.org/download](https://micropython.org/download/) on a ESP8266
* Configuration file
 * [boot.py](boot.py) - to update with netword SSID and password for the WiFi network. Once copied on the ESP8266 (with RShell), it this file will automatically connect the ESP8266 on the WiFi network.
 * [port_config.py](port_config.py) - to update, it will contain the WebRepl password to protect the connexion. It will be automatically used by WebRepl deamon.  

## RShell

__RShell__ is a wonderfull tool used to edit/transfert/repl your board running MicroPython from a single serial connexion (or Serial over bluetooth).

It is a _really useful_ that would be great to learn... with RShell, you can access the MicroPython filesystem (in Flash memory) to edit and copy files.

The wonderfulnes of RShell, is that it also works great with ESP8266 (thankfully because there are no way to emulate USB Mass Storage on ESP8266, a _flash drive_ like is work with the genuine PyBoard).

 * [French tutorial on RShell](https://wiki.mchobby.be/index.php?title=MicroPython-Hack-RShell)
 * [Rshell GitHub](https://github.com/dhylands/rshell) - with english documentation and installation instruction.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - to update. Calls RShell with a small size exchange buffer (needed for ESP8266).

__WARNING__ : On a ESP8266 it is necessary to reduce the exchange buffer... otherwise, it may corrupt the MicroPython filesystem (and it would be necessary to re-flash the ESP8266 with MicroPython) :-/  See the file [rshell-esp8266.sh](rshell-esp8266.sh) suggested in this repository.

## WebRepl

![Repl](dht11/dht11_webrepl.jpg)

Open WebRepl.html in your WebBrowser to start a REPL Session through an HTTP network connexion.

All you need to know is the IP of the the ESP8266 board on the Network.

__WARNING__ :
* You will have to get your [boot.py](boot.py) file properly configured to connect the WiFi network and to start the WebRepl deamon.
* You can also initialise the WebRepl password in the [port_config.py](port_config.py) file. More recent MicroPython firmware will set the WebRepl password from the Boot.py file.
RShell will be a valuable tool for this configuration task.


# Various links

There are many Adafruit  drivers (various plateforms) on this Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

And some IMU (inertial sensor) driver on Github
* https://github.com/micropython-IMU/
