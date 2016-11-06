# ESP8266 MicroPython Driver

Voici une collection de pilote (et raccordements) pour différents breakouts utilisés avec un __ESP8266 reflashé en MicroPython__.

Cela concerne différents breakouts utilisés chez MC Hobby pour nos projets de documentation.
* Wiki Documentaire - https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython
* Achat de matériel - http://shop.mchobby.be 

# Feather ESP8266 Huzza et bus I2C
Suite à de nombreux tests, nous avons remarqué que l'utilisation de la broche 5 (SCL) sur le Feather ESP8266 Huzza causait des problèmes de démarrages dans certaines situations précises. [Voyez ce billet](https://forums.adafruit.com/viewtopic.php?f=57&t=105635)

En effet l'utilisation d'un bloc d'alimenation micro-USB (donc sans USB-Serie) empêche le Feather ESP8266 de booter sur un périphérique I2C est branché sur SCL (pin 5). En l'occurence, il s'agissait un senseur Humidité + Température AM2315.

Nous recommandons donc d'utiliser la broche 2 comme signal SCL pour un bus I2C.
 
# Ressources

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Egalement trouvé des pilotes pour centrales Intertielles sur ce Github
* https://github.com/micropython-IMU/
