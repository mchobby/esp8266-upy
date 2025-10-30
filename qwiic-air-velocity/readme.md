[This file also exists in ENGLISH here](readme_ENG.md)

# Utiliser un capteur de vélocité de l'air (I2C, SEN-18768) de SparkFun avec MicroPython

Le breakout FS3000-1015 de SparkFun est un capteur velocité de l'air permettant de détecter le débit d'air d'un conditionneur d'air (HAVC), d'un système de ventillation ou d'un data center.


![SparkFun SEN-18768 based on FS3000-1015](docs/_static/AirVelocitySensor.jpg)

The FS3000-1015 de Renesas est un module monté en surface capable de relever une vélocité de l'air entre 0 et 15m/s (0 à 54 Km/H). Pour ce faire, il utilise un capteur MEMs thermopile et une résolution 12 bits (0 à 4095).

La bibliothèque supporte les deux versions du breakout:

* FS3000-1015 : mesure de 0 à 15m/s
* FS3000-1005 : mesure de 0 à 7ms/s 

Le breakout expose une interface I2C accessible via le connecteur Qwiic (aussi appelé StemmaQT), ce qui l'intègre dans l'écosystème Qwiic qui simplifie les raccordements grâce à sa connexion universelle.

Sparfun propose [https://www.sparkfun.com/sparkfun-air-velocity-sensor-breakout-fs3000-1015-qwiic.html ses bibliothèques] Arduino et MicroPython. Les bibliothèques exploite une surcouche d'abstraction maison visant a supporter MicroPython et CiruitPython. Cette approche ne correspondant pas à l'approche de ce dépôt, le pilote est redéveloppé depuis la bibliothèque Arduino.

# Bibliothèque


La bibliothèque `airspeed.py` doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/qwiic-air-velocity")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/qwiic-air-velocity
```

# Raccordement

## Raspberry-Pi Pico

![Air Velocity to Raspberry Pico](docs/_static/air-velocity-to-pico.jpg)

L'instance du capteur est créé à l'aide des instructions suivantes:

```
from machine import I2C,Pin
from airspeed import FS3000, AIRFLOW_RANGE_15_MPS
i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
# Adresse par défaut (0x28)
# Ajouter parametre address=0x28 pour une adresse personnalisée
air_speed = FS3000( i2c )
```

# Utiliser

Voici quelques exemples d'utilisation de la bibliothèque `airspeed.py`.

* [test_simple.py](examples/test_simple.py) - exemples simples (repris ci-dessous)


``` python
from machine import I2C,Pin
from airspeed import FS3000, AIRFLOW_RANGE_15_MPS
import time

# Raspberry-Pi Pico
i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
# Adresse par défaut
air_speed = FS3000( i2c )

# air_speed.set_range( AIRFLOW_RANGE_7_MPS )
air_speed.set_range( AIRFLOW_RANGE_15_MPS )

while True:
	print( "FS3000 lecture brute:", air_speed.read_raw() ) # 125ms acquisition
	#  lecture en metre par seconde, retourne un float de 0 - 7.23 pour FS3000-1005, 0 - 15 pour FS3000-1015 
	airflow_mps = air_speed.read_mps()
	if airflow_mps != None: # retourne None en cas d'erreur CRC!
		print( "   m/s:", airflow_mps ) 
		airflow_kmh = airflow_mps*3600/1000
		print( "   Km/h:", airflow_kmh ) 
		airflow_mph = airflow_mps*2.2369362912
		print( "   Miles/h:", airflow_mph ) 
	time.sleep( 1 )

```

# Où acheter
* [SparkFun  Air Velocity Sensor Breakout - FS3000-1015 (Qwiic SEN-18768)](https://www.sparkfun.com/sparkfun-air-velocity-sensor-breakout-fs3000-1015-qwiic.html) @ SparkFun

