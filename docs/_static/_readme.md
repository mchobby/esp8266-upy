[This file also exists in ENGLISH](readme_ENG.md)

# ESP8266 MicroPython Driver

Voici une collection de pilote (et raccordements) pour différents breakouts utilisés avec un __ESP8266 reflashé en MicroPython__.

SI cela fonctionne sous ESP8266 ALORS cela fonctionnera aussi sur la [MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython) et tout autre carte MicroPython!

La plateforme la plus facile à flasher est un [Feather ESP8266 HUZZA ADA2821](http://shop.mchobby.be/product.php?id_product=846) ou une [carte d'évaluation ESP8266-EVB d'Olimex](https://shop.mchobby.be/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html) ou les [cartes WEMOS / LOLIN (modules ESP)](https://shop.mchobby.be/fr/123-wemos-lolin-esp)

![ESP8266 et Pyboard](docs/_static/ESP8266-to-PYBOARD.jpg)
![Feather ESP8266](docs/_static/FEAT-HUZZA-ESP8266-01.jpg)
![Olimex ESP8266 Evaluation Board](docs/_static/ESP8266-EVB.jpg)
![Wemos D1 (ESP8266)](docs/_static/WEMOS-D1.jpg)

# Autres sources d'information
* [__Wiki pour MicroPython sur ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython) pour apprendre comment flasher votre ESP sous MicroPython.
* [__GitHub dédicacé Pyboard__](https://github.com/mchobby/pyboard-driver) avec des pilotes nécessitant plus de ressources. https://github.com/mchobby/pyboard-driver.
* Achat de matériel - https://shop.mchobby.be

# Bibliothèques disponibles
Voici une description des bibliothèques disponibles dans ce dépôt. <strong>Chaque sous-répertoire contient des instructions, schémas et codes dans un readme.md personnalisé.</strong>


Explorer par:
* Interface:
@@interface_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_intf_%code%.md)'} # List per interface

* Fabriquant:
@@manufacturer_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_man_%code%.md)'} # List per manufacturer


@@driver_table:{'lang_code':'fr'} # Insert the driver table

# Quelques ressources utiles
* [how-to-install-upy.md](how-to-install-upy.md) contient un résumé condensé pour une installation depuis Linux
 * [erase-esp8266.sh](erase-esp8266.sh) - A adapter. Permet d'effacer la flash de l'ESP8266
 * [burn-esp8266.sh](burn-esp8266.sh) - A adapter. Permet de flasher un [binaire téléchargé depuis micropython.org/download](https://micropython.org/download/) sur un ESP8266
* fichiers de configuration
 * [boot.py](boot.py) - A adapter avec l'identifiant et mot de passe de votre réseau WiFi. Une fois copié sur votre ESP8266 (avec RShell), celui-ci se connectera automatiquement sur votre réseau WiFi
 * [port_config.py](port_config.py) - A adapter. Placez y le mot de passe qui protégera votre connexion WebRepl. Une fois copié sur votre ESP8266 (avec REPL), il sera automatiquement utilisé par WebRepl.  

## RShell

__RShell__ est un outil formidable qui permet de d'éditer/transférer/repl sur une carte MicroPython a travers une simple connexion série (et même Bluetooth serial).

C'est un outil vraiment _très utile_ qui vaut la peine de s'y attarder... avec lui plus besoin d'avoir accès au "lecteur Flash" de votre carte MicroPython pour y éditer ou y copier un fichier.

Ce qu'il y de génial avec RShell, c'est qu'il fonctionne aussi avec ESP8266 (tant mieux parce qu'il n'y a pas de _lecteur flash_ comme sur une PyBoard).

 * [Tuto RShell en Français](https://wiki.mchobby.be/index.php?title=MicroPython-Hack-RShell)
 * [Github de rshell](https://github.com/dhylands/rshell) - documentation et instruction d'installation.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - A adapater. Appel RShell avec buffer réduit pour ESP8266.

__ATTENTION__ : pour un ESP8266 il faut absolument réduire le buffer d'échange... sinon on écrase facilement le système de fichier (et il faudra reflasher la bête) :-/  Voyez le fichier [rshell-esp8266.sh](rshell-esp8266.sh) qui est proposé ici.

## WebRepl

![Repl](dht11/dht11_webrepl.jpg)

Ouvrez WebRepl.html dans votre navigateur et vous pourrez entamer une session REPL avec votre Feather ESP8266 au travers d'une session HTTP.

Tout ce que vous avez besoin de connaître, c'est soit son adresse IP, soit son nom sur le réseau.

__ATTENTION__ :
* Il convient d'avoir un fichier [boot.py](boot.py) correctement configuré pour que votre ESP8266 puisse se connecter sur votre réseau WiFi.
* Vous pouvez également pré-initialiser votre mot de passe WebRepl dans [port_config.py](port_config.py). Les versions plus récentes de MicroPython place le mot de passe dans le fichier boot.py.
RShell sera un outil précieux pour vous assister dans cette tâche.

# Feather ESP8266 Huzza, bus I2C, bloc d'alim. et boot qui plante

Suite à de nombreux tests, nous avons remarqués que l'utilisation de la broche 5 (SCL) sur le Feather ESP8266 Huzza provoquait parfois des problèmes de démarrage dans certains cas. [Voyez ce billet](https://forums.adafruit.com/viewtopic.php?f=57&t=105635)

En effet l'utilisation d'un _bloc d'alimentation_ micro-USB (donc sans USB-Série) _empêche le Feather ESP8266 de booter si un périphérique I2C_ est branché sur SCL (pin 5). En l’occurrence, il s'agissait un senseur Humidité + Température AM2315 (_utilisé seul sur le bus I2C en Pin 4 et 5_).

Avec le temps et nombreuses autres situations, nous avons fini par remarquer que l'AM2315 n'embarque pas de résistance pull-up sur les lignes SDA et SCL.

Si vous rencontrez cette situation, il y a deux solutions:
* Utiliser la broche 2 comme signal SCL pour votre bus I2C (en guise de test par exemple).
* Vérifier s'il manque des résistances pull-up sur le senseur (à coup sûr pour l'AM2315) et les ajouter vous même.

# Lien divers

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Également trouvé des pilotes pour centrales Intertielles sur ce Github
* https://github.com/micropython-IMU/
