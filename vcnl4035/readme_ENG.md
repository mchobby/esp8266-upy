[Ce fichier existe également en FRANCAIS ici](readme.md)

# VCNL4035: Proximity and Gesture sensor with MicroPython

VCNL4035X01 is an I2C integrates a proximity sensor (PS), ambient light sensor (ALS) and LED drivers for 3 externals Infrared LEDs (named IREDs).

![VCNL4035 breakout](docs/_static/vcnl4035-breakout.jpg)

The ambient light sensor offers a 16 bits resolution and proximity sensor with high resolution of 12 or 16 bits. The sensor handle background light cancellation, thresholds and programmable interrupt.

Sensor also offers immunity to red glow (> 890 nm IREDs), fluorescent light flicker immunity, programmable LED current and integration time. 

Gesture is the most impressive application of this sensor.

![vcnl4035 gesture](docs/_static/vcnl4035-gesture.jpg)

This sensor is best for following applications:

* Handled and consumer device
* Industrial application
* Proximity sensor
* Gesture sensor
* Hygienic application
* Force sensor (measuring the distance to a bending reflective surface deforming under the force).

Thanks to the multiple LEDs, the sensor can perform advanced measurements

![VCNL4035 gesture](docs/_static/vcnl4035-gesture.png)

The [test_read_gesture.py applicative example](examples/app/test_read_gesture.py) is a basic implementation for detecting swipes (closed to the sensor) and push (moving hand down toward the sensors)

![VCNL4035 Swipe detection](docs/_static/vcnl4035-swipe.jpg)

which produces the following results in the REPL output

```
PUSH detected
PUSH detected
SWIPE_RIGHT detected
SWIPE LEFT detected
SWIPE_RIGHT detected
SWIPE LEFT detected 
``` 

# Library

The library must be copied on the MicroPython board before using the examples.

The MicroPython library also including some of the _applicative_ implementation.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/vcnl4035")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/vcnl4035
```

# Wiring

Usual wiring uses an I2C interface. 

Advanced application will requires the Interrupt pin to the microcontroler.

![wiring the VCNL4035-3V3-BRK](docs/_static/vcnl4035-wiring.jpg)

# Examples
Examples are splitted in two groups:

* __examples/basic/__ : [basic examples](examples/basic) testing the VCNL4035 features.
* __examples/app/__ : [applicative examples](examples/app) buiding advanced features around the VCNL4035.

To understand examples, it is important to understand the ZX coordinates.

![vcnl4035 ZX axis](docs/_static/vcnl4035-ZX-axis.jpg)

# Limitation

* Support for switching between modes Proximity Sensor & Ambient Light Sensor.
* Implement low power mode in VCNL App.

# Shopping list

* [VCNL40035 breakout](https://shop.mchobby.be/fr/proximite-distance/2878-vcnl4035-capteur-de-proximite-et-gesture-3232100028784-mchobby.html) is available at MCHobby
