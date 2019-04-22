[This file also exists in ENGLISH here](readme_eng.md)

# Qu'est ce que l'écosystème UEXT  d'Olimex ?

[Olimex](https://www.olimex.com/) a créé de nombreuses cartes microcontrôleurs ainsi que les nano-ordinateurs OlinuXino. Leurs produits sont généralement équipés d'un connecteur UEXT (IDC 10) qui permet de véhiculer:
* une __alimentation 3.3V__,
* un bus __I2C 3.3V__,
* un bus __SPI 3.3v__,
* un __UART 3.3v__.
Ce connecteur s'accompagne de nombreux capteurs et carte d'extension appelés __Modules UEXT__ développés par Olimex (voir [ici chez MCHobby](https://shop.mchobby.be/fr/138-uext) ou [là chez Olimex](https://www.olimex.com/Products/Modules/) ).

Une bonne partie des modules UEXT exploitent le bus I2C, ce qui facilite leur utilisation sur des cartes ESP8266 puisque cela ne nécessite que deux broches pour communiquer avec le module.

# Connecteur UEXT des ESP8266 d'Olimex
![Connecteur UEXT sur les ESP8266 d'Olimex](ESP8266-EVB-UEXT.jpg)

Créer l'instance du bus I2C du connecteur UEXT avec MicroPython

```
from machine import Pin, I2C

i2c = I2C( sda=Pin(2), scl=Pin(4) )
```

__Note :__ les lignes UART sont utilisée par la session REPL  MicroPython sur l'ESP.

# Utiliser UEXT sur ESP8266-EVB
Voici un exemple de raccordement et d'exploitation de connecteur UEXT sur la [carte ESP8266-EVB](https://shop.mchobby.be/fr/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html).

Cette exemple utilise un senseur LTR-501ALS (mesure de luminosité ambiante) avec connecteur UEXT et un [câble console](https://shop.mchobby.be/fr/raspberry-pi-3/144-cable-usb-vers-ttl-serie-3232100001442.html) pour communiquer avec l'ESP via son port série.

![Exploiter le connecteur UEXT](mod-ltr-wiring.png)
