Ce fichier existe également en [Français ici](readme.md)

# Using an I2C Grove ENV III environmental sensor with (U001-C) with MicroPython

ENV III is an environmental sensor that integrates SHT30 and QMP6988 internally to detect temperature, humidity, and atmospheric pressure data. SHT30 is a high-precision and low-power digital temperature and humidity sensor, and supports I2C interface (SHT30:0x44 , QMP6988:0x70).QMP6988 is an absolute air pressure sensor specially designed for mobile applications, with high accuracy and stability, suitable for environmental data collection and detection types of projects.

![ENV III environmental sensor with Grove Interface](docs/_static/u001c.jpg)

* Simple and easy to use
* High accuracy
* Interface de communication I2C

# Bibliothèque

Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/m5stack-u001")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/m5stack-u001
```

# Brancher

Le capteur peut être alimenté en 3.3V ou 5V.

Les signaux I2C (SDA / SCL) sont en niveau logique 3.3V .

## Capteur ENV III I2C avec  Raspberry-Pi Pico

![ENV III I2C sur Raspberry-Pi Pico](docs/_static/u001c-to-pico.jpg)

# Tester

## Lecture des données environmental

Le script [test.py](examples/test.py) effectue une acquisition de données toutes les 100ms.

``` python
xxx
```
