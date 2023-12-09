[This file is also available in ENGLISH](readme_ENG.md)

# Afficher des valeurs numériques à l'aide d'un afficheur numérique 4x7 à Segments LED (DFR0645) sous MicroPython

Un tel afficheur peut être utilisé pour afficher une valeur numérique commpe un score, tension, etc mais aussi un message rudimentaire.

Cet afficheur exuste en:
* 4 chiffres
* Couleur multiple (red, green)
* Expose un connecteur Gravity (pour raccordement rapide)

![4-Digital LED Segment module (DFR0645)](docs/_static/dfr0645.jpg)

# Bibliothèque

La bibliothèque doit être copiée sur la carte MicroPython avant de pouvoir exécuter les exemples.

Sur une plateforme de type WiFi:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/grav-digital-led")
```

Ou à l'aide de l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/grav-digital-led
```

# Brancher

Notez que le bus I2C doit être limité à la vitesse de 100 KHz pour que le composant fonctionne correctement.

## Raspberry-Pi Pico

Le raccrodement est identique pour les les afficheurs à 4 ou 8 digits.

![DFR0645 afficheur LED 4 digits vers Pico sous MicroPython](docs/_static/dfr0645-to-pico.jpg)

| Broche Module | Couleur Fils | Broche Pico | Remarque     |
|------------|------------|----------|------------|
| SDA        | vert       | 6        | I2C(1).sda |
| SCL        | bleu       | 7        | I2C(1).scl, 100 Khz max |
| GND        | noir       | GND      |            |
| VCC        | rouge      | 3V3      |            |

# Tester

Si vous voulez utiliser ce module, il sera nécessaire d'installer la bibliothèque `ledseg4.py` sur la carte MicroPython.

Le code si dessous indique comment afficher différent type de donnée sur l'afficheur 4 chiffres.

```
from machine import I2C
from ledseg4 import LedSegment4

# Raspberry-Pi Pico
i2c = I2C(1, freq=100000 ) # sda=GP6, scl=GP7 , limité a 100 KHz
dis = LedSegment4( i2c )   # DFR0645 afficheur LED 4 digit

# Afficher des entiers
dis.int( 4289 )
dis.int(-43)

# Afficher des float (virgule flottante)
dis.float(0.1)
dis.float(-3.1415)

# Control de luminosité
# (de 0=min a 7=max)
dis.brightness( 4 )

# Eteindre (off) et allumer (on)
dis.off()
dis.on()
```

La bibliothèque est également capable d'afficher un message texte rudimentaire (ASCII, 7bits).

L'image ci-dessous présente les lettres de l'alphabet (en colonnes) et leur représentation sur l'afficheur.

![Alphabet pour le module à segments LED, 4 digits (DFR0645)](docs/_static/alphabet.jpg)

Les caractères inconnus sont remplacés par des blancs (espace).

Lorsque la chaîne est plus longue que l'afficheur le message défile sur celui-ci.


```
from machine import I2C
from ledseg4 import LedSegment4

# Raspberry-Pi Pico
i2c = I2C(1, freq=100000 ) # sda=GP6, scl=GP7 , limited to 100 KHz
dis = LedSegment4( i2c )  # DFR0645 4 digit LED display

# Affichage de messages
dis.print("halo")                  # retour immédiat
dis.print("Micropython is great!") # défilement de texte
```

Le défilement du texte peut être accéléré ou ralenti en utilisant le paramètre `delay_ms` qui modifie le temps d'attente entre deux étapes successive (500ms par défaut).

```
dis.print("Fast scrolling text", delay_ms=200 ) # Défilement rapide
```

# Liste d'achat
* [Raspberry-Pi Pico](https://shop.mchobby.be/en/search?controller=search&s=pico) @ MCHobby
* [Green I2C display 4 digit 7 segments - 22 mm (SEN0645)](https://shop.mchobby.be/fr/leds/2092-afficheur-i2c-vert-4-chiffres-de-7-seg-22-mm-3232100020924-dfrobot.html) @ MCHobby
* [Green I2C display 4 digit 7 segments - 22 mm (SEN0645)](https://www.dfrobot.com/product-1966.html) @ DFRobot
