# ESP8266 MicroPython Driver

Voici une collection de pilote (et raccordements) pour différents breakouts utilisés avec un __ESP8266 reflashé en MicroPython__.

La plateforme la plus facile à flasher est un [Feather ESP8266 HUZZA ADA2821](http://shop.mchobby.be/product.php?id_product=846)

Ce dépôt rassemble différents pilotes pour des breakouts utilisés chez MC Hobby dans nos projets de documentation.
* Wiki Documentaire - https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython
* Achat de matériel - http://shop.mchobby.be 
 
# Quelques ressources utiles
* [how-to-install-upy.md](how-to-install-upy.md) contient un résumé condensé pour une installation depuis Linux
 * [erase-esp8266.sh](erase-esp8266.sh) - A adapter. Permet d'effacer la flash de l'ESP8266
 * [burn-esp8266.sh](burn-esp8266.sh) - A adapter. Permet de flasher un [binaire téléchargé depuis micropython.org/download](https://micropython.org/download/) sur un ESP8266
* fichiers de configuration
 * [boot.py](boot.py) - A adapter avec l'identifiant et mot de passe de votre réseau WiFi. Une fois copié sur votre ESP8266 (avec RShell), celui-ci se connectera automatiquement sur votre réseau WiFi
 * [port_config.py](port_config.py) - A adapter. Placez y le mot de passe qui protégera votre connexion WebRepl. Une fois copié sur votre ESP8266 (avec REPL), il sera automatiquement utilisé par WebRepl.  

 # RShell

__RShell__ est un outil formidable qui permet de d'éditer/transférer/repl sur une carte MicroPython a travers une simple connexion série (et même Bluetooth sérial).

C'est un outil vraiment _très utile_ qui vaut la peine de s'y attarder... avec lui plus besoin d'avoir accès au "lecteur Flash" de votre carte MicroPython pour y editer ou y copier un fichier.

Ce qu'il y de génial avec RShell, c'est qu'il fonctionne aussi avec ESP8266 (tant mieux parce qu'il n'y a pas de _lecteur flash_ comme sur une PyBoard). 

 * rshell - [Github de rshell](https://github.com/dhylands/rshell) - documentation et instruction d'installation.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - A adpater. Appel RShell avec buffer réduit pour ESP8266. 

__ATTENTION__ Pour un ESP8266 il faut absolument réduire le buffer d'échange... sinon on écrase facilement le système de fichier (et il faudra reflasher la bête) :-/  Voyez le fichier [rshell-esp8266.sh](rshell-esp8266.sh) qui est proposé ici. 

 # WebRepl

xxx

# Feather ESP8266 Huzza et bus I2C

Suite à de nombreux tests, nous avons remarqué que l'utilisation de la broche 5 (SCL) sur le Feather ESP8266 Huzza causait des problèmes de démarrages dans certaines situations précises. [Voyez ce billet](https://forums.adafruit.com/viewtopic.php?f=57&t=105635)

En effet l'utilisation d'un bloc d'alimenation micro-USB (donc sans USB-Serie) empêche le Feather ESP8266 de booter sur un périphérique I2C est branché sur SCL (pin 5). En l'occurence, il s'agissait un senseur Humidité + Température AM2315.

Nous recommandons donc d'utiliser la broche 2 comme signal SCL pour un bus I2C.

# Ressources

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Egalement trouvé des pilotes pour centrales Intertielles sur ce Github
* https://github.com/micropython-IMU/
