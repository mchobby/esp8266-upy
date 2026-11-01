# SGP41 - Air Quality Sensor VoC, NOx over I2C with MicroPython

The SGP41 is a MOx (Hot Plate) based digital gas sensors. 
It's main purpose is to measure the indoor air quality with VoC & NOx measurement. This device is great for air quality project like air purifier, air conditionning, ventillation system.

![sgp41](docs/_static/sgp41.jpg)

The library returns `raw_VOC` and `raw_NOx` values are in the range 0..65535 .

Note that NOx is available only after the conditionning of the MOx. This conditioning takes exactly 10 seconds.

![sgp41 conditionning](docs/_static/conditioning.png)

After conditioning, the NOx value is available. 

The best is to optimise the compensation by providing the real relative humidity and real temperature (otherwise it uses the default)

![sgp41 NOx reading](docs/_static/nox-reading.png)

Temperature & Relative Humidity can be measured with an SHT4x sensor.

## Gas Index 

Sensirions offers the __Gaz Index__ algorithm (see [Arduino implementation](https://github.com/Sensirion/arduino-gas-index-algorithm)) to transform raw reading into useful index.

This algorithm is not available for MicroPython... after inspection, the portage may represent an impressive amount of work (if you need an idea...).

So Index calculation is not available.

# Ressources

* [Sensirion_i2c_sgp4x for Python](https://sensirion.github.io/python-i2c-sgp4x/api.html#) (Sensirion)
* [arduino-i2c-sgp41](https://github.com/Sensirion/arduino-i2c-sgp41) (Sensirion)
* [Sensirion Gas Index Algorithm](https://github.com/Sensirion/gas-index-algorithm) (Sensirion, Github)
* [Sensirion Gas Index Algorithm Arduino Library](https://github.com/Sensirion/arduino-gas-index-algorithm) (Sensirion, Github)