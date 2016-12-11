# Mesure Barometrique et température avec Adafruit BMP180 (ADA1603) et ESP8266 MicroPython

* Shop: [Adafruit BMP180 (ADA1603)](http://shop.mchobby.be/product.php?id_product=397)
* Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

# Raccordement

![Raccordements](bmp180_bb.jpg)

# Code de test

```
# Utilisation du breakout BMP180 (ADA1603) avec Feather ESP8266 Python
#
# Shop: http://shop.mchobby.be/product.php?id_product=397
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from bmp180 import BMP180
from machine import I2C, Pin

# Bus I2C
#   Ne pas utiliser la broche standard SCL (broche 5) car perturbe la
#   sequence de boot lorsque l'on utilise un bloc d'alim USB
# 
i2c = I2C( sda=Pin(4), scl=Pin(2), freq=20000 )

bmp180 = BMP180( i2c )

# 0 précision la plus basse, mesure rapide
# 3 précision la plus élevée; mesure plus lente
bmp180.oversample_sett = 2 

# Pression au niveau de la mer (en millibar * 100)
bmp180.baseline = 101325

# Température sur le BMP
temp = bmp180.temperature
print( "Temperature: %.2f deg.Celcius" % temp )

p = bmp180.pressure
print( "pressure: %.2f mbar" % (p/100) )
print( "pressure: %.2f hPa" % (p/100) )

# Altitude calculée a partir de la difference de pression 
# entre le niveau de la mer et "ici"
altitude = bmp180.altitude
print( "altitude: %.2f m" % altitude )
```

# La pression au niveau de la mer varie!
Une valeur standard de la pression au niveau de la mer est de 1013.25 mbar (ou 1013.25 hPa).

Cependant, cette valeur varie en fonction des conditions athomsphérique et de la quantité de vapeur d'eau dans l'air.

Par exemple, ce jour, la pression est de 1002.00 hPa à la Panne (En bordure de mer, Belgique). La Belgique étant un petit territoire relativement plat, la variation de pression à la mer est forcement un élément plus important qu'ailleurs.

J'ai donc corrigé ma baseline comme suit (valeur en hPa * 100):

```
bmp180.baseline = 100200
```

Vous pouvez facilement prendre connaissance de cette pression en consultant un site météo local.

Je vous propose [ce lien vers meteobelgique.be](http://www.meteobelgique.be/observations/temps-reel/stations-meteo.html)

# Le senseur ne me donne pas la bonne altitude!
Mon senseur m'indique une altitude à 189m alors que le site météorologique, à deux pas de chez moi, est à 120m de haut!

L'altitude peut être déduite de la différence entre la pression atmosphérique locale et la pression atmospherique au niveau de la mer.
 
Une fois la pression de la baseline corrigée avec

```
bmp180.baseline = 100200
```

mon senseur retourne une altitude de 104m, nettement plus convenable. 

Je me situe en contrebas de la station météo de référence (qui elle dispose d'une tour). 

# La pression atmosphérique semble incorrecte!

Mon senseur retourne la valeur de 98909 (soit 989.09 hPa) alors que la station météo de référence indique 1002 hPa.

La valeur est bonne mais pas ne tient pas compte de la normalisation PNM appliqué par le station de référence.

Nous allons faire ce petit calcul ensemble...

Pour commencer:
* Faites en sorte que la pression au niveau de la mer corresponde à la valeur du jour (baseline=100200)
* Ceci fait, relevez votre altitude à l'aide du senseur (le mienne est de 104 m)
* La pression diminue de 1hPa chaque fois que l'on monte en altitude de 8.3m .

Ensuite:

Les stations météos normalisent la valeur de la pression atmosphérique pour la ramener "au niveau de la mer" (PNM: Pression Niveau Mer ou SLP: _Sea Level Pressure_). 

Cela signifie qu'elles appliquent une correction sur la valeur lue.

![Pression PNM](Pression_PNM.jpg)

Cette correction consiste à creuser "virtuellement" un trou, sous la station météo, allant jusqu'au niveau de la mer. Trou pour y placer "virtuellement" le senseur de pression. On relève ainsi la pression à la même altitude en plusieurs endroits du pays.

Pour ma station de référence, il s'agit de 120m. En gros, la correction consiste à ajouter une colonne d'air de 120m au dessus du senseur.

__Pourquoi une telle correction?__ 

Et bien parce qu'il est plus facile de concevoir le pays plat comme une crèpe et de regarder les différentes pressions en oeuvre à une même altitude. Cela permet pour imaginer plus facilement le déplacement des masses nuageuses (de la pression la plus élevée vers la pression la plus faîble).

__Revenons à nos moutons!__

Mon altitude est de 104m. Rapellez-vous, la pression diminue de 1hPa tous les 8.3m.

Pour 104m la colonne d'air correspondante représente une pression de 104 / 8.3 = 12.53 hPa

Le senseur BMP180 retourne la valeur 989.09 hPa, la valeur corrigée au niveau de la mer est 989.09 + 12.53 = 1001.62 hPa. Soit la valeur de la station de météo de référence (1002 hPa) à deux pas de la maison.

__Notes:__

Vous aurez sans doute noté que la pression de la station de référence est de 1002 hPa, tout comme la pression au niveau de la mer (aussi 1002 hPa). C'est un pure hasard du jour. 

# Comment obtenir une pression atmospherique PNM ?

L'intérêt d'avoir un senseur de pression c'est de pouvoir relever une pression atmosphérique PNM ramener "au niveau de la mer" (PNM: Pression Niveau Mer ou SLP: _Sea Level Pressure_) comme sur les stations météorologiques et les stations de références.

Voici donc la marche a suivre:
1) Lire les points précédents qui contiennent toutes les informations nécessaires.
2) relevez la pression hPa (ou mmbar) au niveau de la mer (sur une station météo de référence)
3) saisissez cette valeur comme baseline (n'oubliez pas de mutliplier par 100)
4) Utilisez le senseur pour déterminer votre altitude.
5) Calculer la valeur de compensation (colonne d'air) en hPa = hauteur-en-m / 8.3

Corrigez ensuite votre programme

```
# pression moyenne au niveau de la mer
p.baseline = 101325
# pression PNM 
p = bmp180.pressure + compensation
```

p contiendra alors la valeur de pression normalisée au niveau de la mer (PNM) comme les stations météos de référence.

Par contre, l'altitude absolue ne sera plus mesurée fiablement (à moins de pouvoir faire une mise-à-jour de p.baseline régulièrement). Il sera toujours possible d'utiliser la valeur de l'altitude pour détecter une différence de niveau si votre senseur est embarqué sur un "ballon sonde". Dans le cas d'une station météo fixe, l'altitude ne sera plus d'une très grande utilité :-) ... c'est la pression PNM qui nous intéresse. 

# Source et ressources
* Source officielle du pilote: https://github.com/micropython-IMU/micropython-bmp180
* Pression Atmospherique expliquée: https://fr.wikipedia.org/wiki/Pression_atmosph%C3%A9rique
