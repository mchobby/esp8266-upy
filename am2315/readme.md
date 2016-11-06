# Mesure temperature/humidité avec senseur AM2315 (ADA2315) et ESP8266 sous MicroPython

* Shop: http://shop.mchobby.be/product.php?id_product=932
* Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

# Raccordement

![Raccordement](AM2315_bb.jpg)

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
    
# Source et ressources
* Source Arduino du pilote: https://github.com/adafruit/Adafruit_AM2315
