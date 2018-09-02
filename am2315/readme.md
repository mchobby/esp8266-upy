# Mesure temperature/humidité avec senseur AM2315 (ADA2315) et ESP8266 sous MicroPython

* Shop: [senseur AM2315 (ADA2315)](http://shop.mchobby.be/product.php?id_product=932)
* Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

# Raccordement

Nous ne l'avions pas remarqué directement mais l'AM2315 nécessite des résistance pull-up pour fonctionner car celle-ci ne sont ni présentes sur l'AM2315, ni sur l'ESP8266. C'est la raison pour laquelle nous avons opté pour un bus I2C sur les Pin 2 et 4!

![Raccordement](AM2315_bb.jpg)

Avec le temps, nous nous sommes rendu compte que le montage fonctionnait correctement avec les deux broches Pin 5 et 4 si d'autres composants I2C étaient présent sur le bus.

Etant donné que les différents breakout embraquent souvent des résistances pull-up, nous nous sommes rendu compte que c'est ce qui faisait défaut lorsque l'AM2315 était monté seul sur les Pin 5 et 4. Voici donc le montage alternatif de l'AM2315 avec résistance pull-up.

![Raccordement avec pull-up](AM2315_bb_v2.png)

# Code de test

```
# Utiliser un senseur AM2315 I2C temperature/humidité (ADA2315) avec ESP8266 sous MicroPython
#
# Shop: http://shop.mchobby.be/product.php?id_product=932
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from am2315 import *
from machine import I2C, Pin

# Bus I2C
#   Ne pas utiliser la broche standard SCL (broche 5) car perturbe la
#   sequence de boot lorsque l'on utilise un bloc d'alim USB
#
i2c = I2C( sda=Pin(4), scl=Pin(2), freq=20000 )
#   Possible si utilisé avec des résistances pull-up ou autres breakout I2C.
# i2c = I2C( sda=Pin(4), scl=Pin(5), freq=20000 )

a = AM2315( i2c = i2c )

def show_values():
    if a.measure():
       print( a.temperature() )
       print( a.humidity() )

# Deux lectures consécutives sont parfois nécessaire
# pour faire une mise-à-jour connecte des valeurs lues.

show_values()
time.sleep( 1 )
show_values()
```

Ce qui donne le résultat suivant dans WebRepl

![Resultat](AM2315_webrepl.jpg)

# Feather ESP8266 Huzza, bus I2C, bloc d'alim. et boot qui plante

Suite à de nombreux tests, nous avons remarqués que l'utilisation de la broche 5 (SCL) sur le Feather ESP8266 Huzza provoquait parfois des problèmes de démarrage dans certains cas. [Voyez ce billet](https://forums.adafruit.com/viewtopic.php?f=57&t=105635)

En effet l'utilisation d'un _bloc d'alimentation_ micro-USB (donc sans USB-Série) _empêche le Feather ESP8266 de booter si un périphérique I2C_ est branché sur SCL (pin 5). En l’occurrence, il s'agissait un senseur Humidité + Température AM2315 (_utilisé seul sur le bus I2C en Pin 4 et 5_).

Avec le temps et nombreuses autres situations, nous avons fini par remarquer que l'AM2315 n'embarque pas de résistance pull-up sur les lignes SDA et SCL.

Si vous rencontrez cette situation, il y a deux solutions:
* Utiliser la broche 2 comme signal SCL pour votre bus I2C (en guise de test par exemple).
* Vérifier s'il manque des résistances pull-up sur le senseur (à coup sûr pour l'AM2315) et les ajouter vous même.

# Source et ressources
* Source Arduino du pilote: https://github.com/adafruit/Adafruit_AM2315
