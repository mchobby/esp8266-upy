# Installer MicroPython ESP8266 edition
Vous pouvez trouver la dernière version de micro python pour ESP8266 ici:

* https://micropython.org/download/

Voici les commandes utilisées pour installer les outils et opérations nécessaire pour reflashage d'un ESP8266 

```
pip install esptool

esptool.py --port /path/to/ESP8266 erase_flash

esptool.py --port /path/to/ESP8266 --baud 460800 write_flash --flash_size=8m 0 firmware.bin
```
