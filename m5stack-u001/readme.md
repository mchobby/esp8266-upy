This file also exists in [English here](readme_ENG.md)

# Utiliser le capteur environnementalt Grove ENV III (U001-C) en I2C avec MicroPython

ENV III is an environmental sensor that integrates SHT30 and QMP6988 internally to detect temperature, humidity, and atmospheric pressure data. SHT30 is a high-precision and low-power digital temperature and humidity sensor, and supports I2C interface (SHT30:0x44 , QMP6988:0x70).QMP6988 is an absolute air pressure sensor specially designed for mobile applications, with high accuracy and stability, suitable for environmental data collection and detection types of projects.

![Capteur environnemental ENV III avec interface Grove](docs/_static/u001c.jpg)

* Facile à utiliser
* Haute précision
* I2C communication interface

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/m5stack-u001")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/m5stack-u001
```

# Wiring

The sensor  can be powered with 3.3V or 5V power supply.

The SDA / SCL data lines are at 3.3V level.

## ENV III I2C sensor with Raspberry-Pi Pico

![ENV III I2C to Raspberry-Pi Pico](docs/_static/u001c-to-pico.jpg)

# Test

The [env3.py](lib/env3.py) library must be copied on your MicroPython microcontroler.

## Reading the environmental sensor Sensor

The [test.py](examples/test.py) script do reads the sensor value every 100ms.

``` python
xxx
```
