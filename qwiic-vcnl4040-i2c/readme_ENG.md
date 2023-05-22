[Ce fichier existe également en FRANCAIS](readme.md)

# Using the VCNL4040 proximity/distance Qwiic sensor (I2C) with MicroPython

Sparkfun do manufacture the distance/proximity sensor based on the VCNL4040 chip (SparkFun, SEN-15177). This sensor do have a Qwiic connector which make it easy to wire/plug.

The board can be used to detect object 20cm around the sensor.

![SparkFun Qwiic I2C VCNL4040](docs/_static/vcnl4040-qwiic.jpg)

The VCNL4040 is a simple IR presence and ambient light sensor. This sensor is excellent for detecting if something has appeared in front of the sensor. We often see this type of sensor on automatic towel dispensers, automatic faucets, etc. You can detect objects qualitatively up to 20cm away. This means you can detect if something is there, and if it is closer or further away since the last reading, but it's difficult to say it is 7.2cm away. If you need quantitative distance readings (for example sensing that an object is 177mm away) check out the SparkFun Time of Flight (ToF) sensors with mm accuracy.

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/qwiic-vcnl4040-i2c")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/qwiic-vcnl4040-i2c
```

# Wiring

## Wire to MicroMod-RP2040

On the following picture, the [MicroMod Learning Machine](https://www.sparkfun.com/products/16400) _Carrier board_ (SparkFun,  DEV-16400) is used to bring the Qwiic connectivity out of the MicroMod-RP2040.

![Qwiic vcnl4040 proximity sensor to MicroMod RP2040](docs/_static/vcnl4040-to-micromod-rp2040.jpg)

## Wire to Raspberry-Pi Pico

You can wire the sensor board to a pico thanks to the [Qwiic Cable Breakout](https://www.sparkfun.com/products/14425) (SparFun, PRT-14425)

![Qwiic VCNL proximity sensor to Raspberry-Pi Pico](docs/_static/vcnl4040-to-pico.jpg)

# Testing

Before execting the examples, it will be necessary to copy the [vcnl4040.py](lib/vcnl4040.py) library to the MicroPython board.

## test.py

The [test.py](examples/test.py) example script do poll the VCNL4040 sensor.

``` python
from machine import I2C, Pin
from vcnl4040 import VCNL4040

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

prox = VCNL4040( i2c )
prox.power_proximity( enable=True )
print( "Proximity value :", prox.proximity )
```

## test_readprox.py - read the level from proximity sensor

The [test_readprox.py](examples/test_readprox.py) example script will read data from the proximity sensor.

Please note that the sensor is activated as soon as the sensor object is created.

``` python
from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

from machine import I2C, Pin
import time

i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
prox = VCNL4040( i2c )

while True:
	print( "Proximity Value: ", prox.proximity )
	time.sleep_ms(10)
```

Which produce the following results on the REPL session:

```
Proximity Value:  2   <-- nothing near of the sensor
Proximity Value:  2
Proximity Value:  3
...
Proximity Value:  76
Proximity Value:  76
Proximity Value:  133
Proximity Value:  229
Proximity Value:  229
Proximity Value:  229
Proximity Value:  434
Proximity Value:  909
Proximity Value:  909
Proximity Value:  909
Proximity Value:  1169  <-- paper sheet in front of sensor
Proximity Value:  1169
Proximity Value:  1169

Proximity Value:  1699
Proximity Value:  1699
...
Proximity Value:  906  <-- moving sheet away
Proximity Value:  906
Proximity Value:  791
Proximity Value:  791
Proximity Value:  694
Proximity Value:  694
Proximity Value:  588
...
Proximity Value:  5   <-- Nothing in front of sensor
Proximity Value:  3
Proximity Value:  2
Proximity Value:  1
Proximity Value:  2
```

More we are close, more the value will increase!


## test_something.py - Is there something on the front of the sensor

The [test_something.py](examples/test_something.py) example script will quickly
detect when an object passes in the front of the sensor.

``` python
from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
prox = VCNL4040( i2c )

startingProxValue = 0
deltaNeeded = 0
nothingThere = False

# Set the current used to drive the IR LED - 50mA to 200mA is allowed.
prox.set_led_current( 200 ) # The max

# The sensor will average readings together by default 8 times.
# Reduce this to one so we can take readings as fast as possible
prox.set_prox_integration_time(8) # 1 to 8 is valid

# Take 8 readings and average them
for i in range( 8 ):
	startingProxValue += prox.proximity
startingProxValue /= 8

# Calculate a Delta
deltaNeeded = startingProxValue * 0.05 # Look for 5% change
if deltaNeeded < 5:
	deltaNeeded = 5 # Set a minimum

while True:
	value = prox.proximity
	#print( "Proximity Value: ", value )

	# Let's only trigger if we detect a 5% change from the starting value
	# Otherwise, values at the edge of the read range can cause false triggers
	if value > (startingProxValue + deltaNeeded):
		print("Something is there!" )
		nothingThere = False
	else:
		if nothingThere == False:
			print( "I don t see anything" )
		nothingThere = True

	time.sleep_ms(10)
```

Which produce the following results on the REPL session:

```
I don t see anything
Something is there!   <-- moving the hand toward the sensor (~20cm)
Something is there!
Something is there!
Something is there!
Something is there!   <--keeping hand over the sensor (~5cm)
Something is there!
Something is there!
Something is there!
Something is there!
Something is there!
Something is there!
Something is there!
Something is there!
I don t see anything
Something is there!
Something is there!
Something is there!
Something is there!
Something is there!
I don t see anything
Something is there!
Something is there!
Something is there!
```

## test_ambient.py - Ambient light

The [test_ambient.py](examples/test_ambiant.py) example script will detect the
light level around the sensor.

``` python
from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
prox = VCNL4040( i2c )


prox.power_proximity( enable=False ) # Power down the proximity portion of the sensor
prox.power_ambient( enable=True ) # Power up the ambient sensor

while True:
	print("Ambient light level: ", prox.ambient )
	time.sleep_ms( 50 )
```

A value of 1000 was measured for articial light. Covering the sensor with the
hand will quickly drops the value around 50.


## test_readall.py - reads the various light levels

The [test_readall.py](examples/test_readall.py) example script detects the:
* ambient light,
* infrared light (IR),
* white light.

Along with proximity and ambient light sensing the VCNL4040 has a 'white light' sensor as well. Point the sensor up and start the sketch. Then cover the sensor with your hand.

* IR readings increase as the reflected IR light increases, so more the object is close from the the sensor (Proximity reading)
* Ambient light readings decrease as less ambient light can get to the sensor (eg: hand over the sensor)
* White light readings increases as more white light reach the sensor (removing the hand from sensor... or daylight instead of night)

``` python
from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

prox = VCNL4040( i2c )
prox.power_proximity( enable=True ) # Power down the proximity portion of the sensor
prox.power_ambient( enable=True ) # Power up the ambient sensor
prox.enable_white_channel( enable=True )

print( "Prox Value : Ambient :  White Level" )
while True:
	print(prox.proximity, prox.ambient, prox.white )
	time.sleep_ms( 100 )
```

## test_interrupt.py - trigger an proximity interrupt

The [test_interrupt.py](examples/test_interrupt.py) example script will configure the sensor to activate the interrupt pin (going LOW) when an object is close from the sensor.

Check with a multimeter, the INT pin does to 0 Volt when an objet is on front of the sensor (1-2 cm).

__The great thing about the interrupt, is that the sensor doesn't need to be queried over the I2C bus__ (_Polling_) to know if an objet get close from the sensor!
