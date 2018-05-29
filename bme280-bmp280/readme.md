# Introduction
Cette bibliothèque est un pilote pour le senseur BME280 température/pression/humidité et BMP280 température/pression pour être utilisé avec MicroPython sur les cartes ESP8266.

Cette bibliothèque provient du dépôt GitHub https://github.com/catdog2/mpy_bme280_esp8266 (voyez le contenu du fichier bme280.py pour les crédits).

# A propos du BME280 et BMP280

Le BMP280 et BME280 sont des senseurs environnementaux de Bosch qui combinent la mesure de la pression, température. Le BME280 permet également de mesurer l'humidité relative. 

Ces senseurs peuvent communiquer via I2C ou SPI; Ce pilote utilise I2C.

* Shop: [Adafruit BMP280 (ADA2651)](http://shop.mchobby.be/product.php?id_product=1118)
* Shop: [Adafruit BME280 (ADA2652)](http://shop.mchobby.be/product.php?id_product=684)
* Wiki: [nos tutoriels MicroPython pour ESP8266](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython)
* [Fiche technique du BME280](https://www.adafruit.com/datasheets/BST-BME280_DS001-10.pdf) Adafruit Industries.
 
# Raccordement

### Raccordement BMP280 ###
![Raccordements](bmp280_bb.jpg)

### Raccordement BME280 ###
![Raccordements](bme280_bb.jpg)

# Utilisation 
Copiez la bibliothèque `bme280.py` sur votre carte ESP8266 (ex: en utilisant webrepl, rsheel, ou ampy).

Puis utiliser le code suivant pour faire fonctionner votre senseur. Tester le code dans une session REPL ou WebREPL. 

### Utilisation avec BME280 ###

``` python
from machine import Pin, I2C
from bme280 import *

i2c = I2C(scl=Pin(5), sda=Pin(4))
bme = BME280(i2c=i2c)

print(bme.values)
```

### Utilisation avec BMP280 ###

``` python
from machine import Pin, I2C
from bme280 import *

i2c = I2C(scl=Pin(5), sda=Pin(4))
bmp = BME280(i2c=i2c, address=BMP280_I2CADDR )

print(bmp.values)
```

Qui produit un tuple de valeurs avec des informations _Human Readeable_: 
* La température en degrés Celcius (valeur en , 
* La pression en HectoPascal
* L'humidité relative en pourcent<br />Pour un BMP280, la valeur de l'humidité sera toujours égale à 0 parce que le BMP280 ne dispose pas du senseur d'humidité.

``` python
('22.36C', '1005.65hPa', '0.00%')
```

La classe propose également une propriété `raw_values` qui retourne un tuple avec des valeurs numériques:

Par exemple, l'appel de :

``` python
print(bmp.raw_values)
```

produira le résultat suivant :

``` python
(22.36, 1005.65, 0.0)
```

# En détails #

La propriété `values` est une fonction de convenance qui retourne un tuple avec les différentes valeurs du senseur sous forme de chaîne de caractère au format _human-readable_ (lisible par un humain). Cela permet de vérifier rapidement le fonctionnement du senseur. 

Dans la pratique, la méthode utilisée est `read_compensated_data()` qui retourne un tuple `(temperature, pression, humidité)` où:

* `temperature`:  est exprimée en centième de degrés celcius. Par exemple, la valeur 2534 indique une température de 25.34 degrés.
* `pression`: Pression athmosphérique codé sur une valeur 32 bits dont les premiers 24 bits est une valeur entière et les 8 derniers bits la valeur fractionnelle. Diviser la valeur par 256 pour obtenir la valeur en Pascals. Par exemple, la valeur 24674867 correspond à la valeur 96386.2Pa, ou 963.862hPa.
* `humidité`: Humidité relative codée sur une valeur 32 bits dont les premiers 22 bits indique une valeur entière et les 10 bits suivant indiquant la valeur fractionnelle. Pour obtenir la valeur en %RH, divisé par 1024. Par exemple, la valeur 47445 correpsond à une humidité relative 46.333 %RH.

