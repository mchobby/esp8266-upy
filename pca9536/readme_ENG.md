[Ce fichier existe également en FRANCAIS](readme.md)

# PCA9536 - 4 Bit I2C GPIO Expander

![PCA9536 PinOut](docs/_static/pca9536-pinout.png)

PCA9536 is an 8-pin chip (5V tolerant pins) that provides 4 bits of General Purpose parallel Input/Output (GPIO).

The PCA9536 is used as interface on some I2C expansion board so this GitHub section only contains the driver and examples code.

Here below a common usage for the PCA9536.

![PCA9536 usage](docs/_static/pca9536-usecase.png)

__The PCA9536 have an very particular feature__ with the internal 100 kΩ pull-up resistor (cannot be disabled!) on input pins.

The power-on reset feature sets the registers to their default values and initializes the device state machine.

Main features:
* [PCA9536 datasheet](https://www.nxp.com/products/analog/interfaces/ic-bus/ic-general-purpose-i-o/4-bit-i2c-bus-and-smbus-i-o-port:PCA9536)
* 4-bit I2C bus GPIO (0 Hz to 400 kHz clock frequency)
* Operating power supply voltage range of 2.3 V to 5.5 V
* 5 V tolerant I/Os
* Polarity Inversion register
* Low standby current
* No glitch on power-up
* Internal power-on reset
* 4 I/O pins which default to 4 inputs with 100 kΩ internal pull-up resistor
* ESD protection exceeds 2000 V
* Latch-up testing is done to JEDEC Standard JESD78 which exceeds 100 mA

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/pca9536")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/pca9536
```

# Testing

```
from pca9536 import PCA9536
from machine import Pin, I2C
from time import sleep

# Create the I2C bus accordingly to your plateform.
# Pyboard: SDA on Y9, SCL on Y10.
#         Default bus Freq 400000 = 400 Khz is to high.
#         So reduce it to 100 Khz. Do not hesitate to test with 10 KHz (10000)
i2c = I2C( 2, freq=100000 )
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )

pca = PCA9536( i2c )

# Set IO0 to Input - Hardware pull-up activat on all Pin by default
pca.setup( 0, Pin.IN  )
# Set IO1 to Input - Hardware pull-up activat on all Pin by default
#	Result is False when pin is HIGH (not connected to ground)
#	Result is True  when pin is LOW  (connected to ground)
pca.setup ( 1, Pin.IN )

# Set IO3 to Output
pca.setup( 3, Pin.OUT )
pca.output( 3, False )  # High by default because of the pull-up for input
for i in range( 2 ):
	# Tip: see output_pins() for multiple pins updates
	pca.output( 3, True )
	sleep( 1 ) # 1 Second
	pca.output( 3, False )
	sleep( 1 )

# Read value on GPIO 0 - pull-up activated by default
for i in range( 10 ):
	# Tip: see input_pins() for multiple pin reads
	print( "IO0 = %s" % (pca.input(0)) )
	sleep( 1 )

# Read value on GPIO 1 - pull-up activated by default
for i in range( 10 ):
	# Tip: see input_pins() for multiple pin reads
	print( "IO1 = %s" % (pca.input(1)) )
	sleep( 1 )
```
