[This file also exists in ENGLISH](readme_ENG.md)

# Utiliser une centrale inertielle (IMU) ISM330DHCX avec MicroPython

Le composant ISM330DHCX de ST Electronics est un dérivé direct du LSM6DSOX (aussi du même fonndeur).

Cette Unité de mesure Intertielle combine un Accélérometre, Gyroscope et capteur de température. Ce composant dispose d'un support pour I2C et SPI... mais cette implémentation ce concentre uniquement sur le bus I2C.

Ce pilote fonctionnera avec tous les [breakout ISM330DHCX](https://shop.mchobby.be/fr/mouvement/2883-ism330dhcx-centrale-inertielle--3232100028838.html) exposant une interface I2C.

![ISM330DHCX-3V3-BRK disponible à MCHobby](docs/_static/ISM330DHCX-01.jpg)

# Credit

Ce pilote est un portage MicroPython du [dépôt Adafruit_LSM6DS pour Arduino](https://github.com/adafruit/Adafruit_LSM6DS/tree/master).

Cette bibliothque est un magnifique travail réalisé par Adafruit.

La bibliothèque Arduino est relativement complexe avec de nombreuses classes et sous-classes. Elle s'appuie également sur la [bibliothèque Adafruit_Sensor library](https://github.com/adafruit/Adafruit_Sensor/tree/master)

```
[ISM330DHCX class]--->[LSM6DSOX class]--->[LSM6DS class]
``` 

Ce __portage MicroPython implemente les classes essentielles et définitions nécessaires afin de pouvoir utiliser l' ISM330DHCX__ .

# Brancher

Le plus simple est d'utiliser le populaire connecteur Qwiic/StemmaQt qui trannsporte le bus I2C. Le branchement est élémentaire.

![Raccorder un ISM330DHCX-3V3-BRK sur Rapsberry-Pi Pico](docs/_static/ISM330DHCX-3V3-BRK-to-pico.jpg)

Sinon: Il faut branncher les signaux sda, scl sur le microconntroleur. Il faut égalemennt connecter 3V3 et GND pour alimenter le breakout.

# Bibliothèque 

La bibliothèque doit être copiée sur la carte MicroPython avant de pouvoir utiliser les examples.

Sur une carte disposant d'une connexion WiFi:

 ```
 >>> import mip
 >>> mip.install("github:mchobby/esp8266-upy/lsm6ds")
 ```

Ou d'utiliser l'utilitaire mpremote :

 ```
 mpremote mip install github:mchobby/esp8266-upy/lsm6ds
 ```

# Exemples

L'exemple [ism330dhcx_test.py](examples/ism330dhcx_test.py) collecte les innformations à propos des capteurs et affiche celle-cis dans la sortie REPL.

Cet exemple est très pratique pour tester la connectivité avec le capteur.

Voici un résultat typique:

```
------------------------------------
Sensor: LSM6DS_A
Type: Acceleration (m/s2)
Driver Ver: 1
Unique ID: 1745
Min Value: -156.9064
Max Value: 156.9064 
Resolution: 0.061
------------------------------------
------------------------------------
Sensor: LSM6DS_G
Type: Gyroscopic (rad/s)
Driver Ver: 1
Unique ID: 1746
Min Value: -34.91
Max Value: 34.91 
Resolution: 7.6358e-05
------------------------------------
------------------------------------
Sensor: LSM6DS_T
Type: Ambient Temp (C)
Driver Ver: 1
Unique ID: 1744
Min Value: -40
Max Value: 85 
Resolution: 1
------------------------------------
```

Le second exemple [ism330dhcx_read.py](examples/ism330dhcx_read.py) capture les données du capteur puis affiche celle-ci dans la sortie REPL.

Voici un résultat typique produit par le script:

```
Accelerometer range set to: 
	+-4G
Gyroscope range set to: 
	2000 degrees/s
Accelerometer data rate set to: 
	104 Hz
Gyro data rate set to: 
	104 Hz
Temperature 22.2343736 deg C
Accel X: -1.884348 	Y: 0.7573284 	Z: 9.759127 m/s^2
Gyro X: 0.002443461 	Y: -0.010995574 	Z: 0.0061086524 radians/s
Temperature 22.261718 deg C
Accel X: -1.88554432 	Y: 0.75254268 	Z: 9.738788 m/s^2
Gyro X: 0.0012217305 	Y: -0.00366519132 	Z: 0.004886922 radians/s
```

# Liste d'achat
* [ISM330DHCX breakout](https://shop.mchobby.be/fr/mouvement/2883-ism330dhcx-centrale-inertielle--3232100028838.html) @ MCHobby
* ISM330DH @ Adafruit
