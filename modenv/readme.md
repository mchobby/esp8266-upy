[This file also exists in ENGLISH here](readme_ENG.md)

# Utiliser un capteur environnemental pour mesurer la qualité de l'air avec votre carte MicroPython

La carte MOD-ENV d'Olimex exploite deux capteurs I2C:
* Un capteur BME280 de Bosch -> Mesure de pression atmosphérique, température et humidité relative.
* Un capteur CCS811 -> mesure de la qualité de l'air eCO2 (Dioxyde de carbone équivalent) et composés organiques volatiles (VOC / COV)

![Capteur MOD-ENV d'Olimex](docs/_static/modenv.jpg)

# Brancher
Le capteur se branche très simplement sur une carte équipée d'un port UEXT comme l' [adaptateur UEXT pour pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT) ou la carte [Pyboard-UNO-R3](https://shop.mchobby.be/fr/nouveaute/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html).

![Connecteur UEXT sur Pyboard](docs/_static/uext-breakout.jpg)

Il est également possible de réaliser les branchement d'un connecteur UEXT (IDC 10 broches) directement sur la Pyboard comme indiqué ci-dessous. Il ne restera plus qu'a y raccorder le capteur environnemental.

![Bus I2C sur connecteur UEXT](docs/_static/modenv-to-pyboard.jpg)

# Tester
Les bibliothèques `bme280.py` et `ccs811.py` doivent être copiés sur la carte MicroPython.

Ces bibliothèques sont disponibles dans les dépôts suivants:
* `bme280.py` : https://github.com/mchobby/esp8266-upy/tree/master/bme280-bmp280
* `ccs811.py` : https://github.com/mchobby/esp8266-upy/tree/master/ccs811

Le script `test.py` permet d'exploiter les fonctionnalités principales du capteur.

``` Python
import time
import ccs811
import bme280

from machine import I2C

i2c = I2C( 2 )
ccs811 = ccs811.CCS811( i2c )
bme = bme280.BME280( i2c=i2c )

# Check if the sensor returns an error
if ccs811.check_error:
	print( "An error occured!")
	print( "ERROR_ID = %s" % ccs811.error_id.as_text )
	while True:
		time.sleep( 0.100 )

# Wait for the sensor to be ready
while not ccs811.data_ready:
	time.sleep( 0.100 )

while True:
	values = bme.raw_values # Temperature, pressure hPa, %Rel Humidity
	print("CO2: {} PPM, TVOC: {} PPB, Temp: {} C, hPa: {}, Rh {} percent".format(ccs811.eco2, ccs811.tvoc, values[0], values[1], values[2]) )

	time.sleep(0.5)
```

Ce qui produit les résultats suivants dans la console

```
CO2: 400 PPM, TVOC: 0 PPB, Temp: 24.4 C, hPa: 995.94, Rh 46.49 percent
CO2: 400 PPM, TVOC: 0 PPB, Temp: 24.4 C, hPa: 995.91, Rh 46.48 percent
CO2: 400 PPM, TVOC: 0 PPB, Temp: 24.4 C, hPa: 995.87, Rh 46.52 percent
CO2: 400 PPM, TVOC: 0 PPB, Temp: 24.4 C, hPa: 995.96, Rh 47.09 percent
CO2: 413 PPM, TVOC: 1 PPB, Temp: 24.41 C, hPa: 995.93, Rh 47.44 percent
CO2: 413 PPM, TVOC: 1 PPB, Temp: 24.39 C, hPa: 995.97, Rh 47.6 percent
CO2: 405 PPM, TVOC: 0 PPB, Temp: 24.39 C, hPa: 995.95, Rh 47.59 percent
CO2: 405 PPM, TVOC: 0 PPB, Temp: 24.41 C, hPa: 996.02, Rh 48.13 percent
... Breathing toward the environmental Sensor
... Souffler vers le capteur environnementale
CO2: 454 PPM, TVOC: 8 PPB, Temp: 24.47 C, hPa: 996.02, Rh 51.67 percent
CO2: 454 PPM, TVOC: 8 PPB, Temp: 24.62 C, hPa: 996.04, Rh 53.98 percent
CO2: 454 PPM, TVOC: 8 PPB, Temp: 24.78 C, hPa: 996.08, Rh 55.22 percent
CO2: 454 PPM, TVOC: 8 PPB, Temp: 24.91 C, hPa: 996.0999, Rh 56.7 percent
CO2: 480 PPM, TVOC: 12 PPB, Temp: 25.04 C, hPa: 996.04, Rh 58.35 percent
CO2: 480 PPM, TVOC: 12 PPB, Temp: 25.18 C, hPa: 995.96, Rh 60.75 percent
CO2: 605 PPM, TVOC: 31 PPB, Temp: 25.32 C, hPa: 996.08, Rh 61.63 percent
CO2: 605 PPM, TVOC: 31 PPB, Temp: 25.44 C, hPa: 996.06, Rh 63.0 percent
CO2: 620 PPM, TVOC: 33 PPB, Temp: 25.54 C, hPa: 996.03, Rh 65.12001 percent
CO2: 620 PPM, TVOC: 33 PPB, Temp: 25.52 C, hPa: 996.06, Rh 62.73 percent
CO2: 523 PPM, TVOC: 18 PPB, Temp: 25.5 C, hPa: 996.02, Rh 59.27 percent
CO2: 523 PPM, TVOC: 18 PPB, Temp: 25.48 C, hPa: 996.0999, Rh 56.72 percent
```

L'exemple avancé [`test_enh.py`](examples/test_enh.py) pousse les données environnement sur le capteur CCS811 tous les 1/4 d'heures.

# Ou acheter
* [MOD-ENV : Capteur Environnemental](https://shop.mchobby.be/fr/uext/1780-capteur-environnementale-tout-en-un-bme280-ccs811-3232100017801.html) @ MCHobby
* [MOD-ENV : Capteur Environnemental](https://www.olimex.com/Products/Modules/Sensors/MOD-ENV/open-source-hardware) @ Olimex
