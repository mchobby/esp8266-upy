[This file also exists in ENGLISH](readme_ENG.md)

# Plateform Agnostic MicroPython Driver

Initialement, cette collection de pilote + raccordement pour différents breakouts fût  destinée au microcontrôleur ESP8266 reflashé en MicroPython d'où le nom "_esp8266-upy_" pour ce dépôt.

Depuis, cette collection a largement dépassée son cadre initial puisque les pilotes sont écrits pour __fonctionner indépendamment de la [plateforme MicroPython](https://shop.mchobby.be/fr/56-micropython) cible__.

![PLateform Agnostic MicroPython Driver](docs/_static/PAM-driver.jpg)

__MIP ready!__ Les bibliothèques peuvent être installées avec l'[outil MIP](https://docs.micropython.org/en/latest/reference/packages.html) (__MicroPython Install Package__).

# Bibliothèques disponibles
Voici une description des bibliothèques disponibles dans ce dépôt. <strong>Chaque sous-répertoire contient des instructions, schémas et codes dans un readme.md personnalisé.</strong>

Explorer par:
* Interface:
@@interface_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_intf_%code%.md)'} # List per interface
* Fabriquant:
@@manufacturer_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_man_%code%.md)'} # List per manufacturer


@@driver_table:{'lang_code':'fr'} # Insert the driver table

# Lien divers
* [__Wiki pour MicroPython sur ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython) pour apprendre comment flasher votre ESP sous MicroPython.
* [__GitHub dédicacé Pyboard__](https://github.com/mchobby/pyboard-driver) avec des pilotes nécessitant plus de ressources. https://github.com/mchobby/pyboard-driver.
* Achat de matériel - https://shop.mchobby.be

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Également trouvé des pilotes pour centrales Intertielles sur ce Github
* https://github.com/micropython-IMU/
