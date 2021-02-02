[Ce fichier existe également en FRANCAIS](readme.md)

# TCA9554A - 8 bits GPIO Expander via I2C

The TCA9554A from Texas Instrument allows you to add 8 inputs/outputs with interrupt output and configuration register.

![TCA9554A pinout](docs/_static/tca9554a.jpg)

This component:
* works with 1.65V to 5.5V logic level.
* Does have 3 addressing bits (default is 0x38).
* does have a "polarity" configuration (to invert polarity of input pins)
* activates a 100 KOhms pull-up resistor on input pins.

See the [TCA9554A datasheet](https://www.ti.com/lit/gpn/tca9554a) for more information.

# Wire

# TCA9554A to Raspberry-Pi Pico

![tca9554a to pico](docs/_static/tca9554a-to-pico.jpg)

# TCA9554A to Pyboard

![tca9554a to Pyboard](docs/_static/tca9554a-to-pyboard.jpg)

# Example

The [test_all_out.py](examples/test_all_out.py) example script shows how to use this class.

The MicroPython API for the TCA9554A is identical to the MCP23017 interface, so you can use the MCP23017 to learn the usage of this class.

``` python
from machine import I2C, Pin
from tca9554a import TCA9554A
from time import sleep

# Pico, sda=GP6, scl=GP7
i2c = I2C(1)
# Pyboard, sda=X10, scl=X9
# i2c = I2C(1)

tca = TCA9554A( i2c )

for i in range(8):
	tca.setup( i, Pin.OUT )

print( "All output ON" )
for i in range(8):
	tca.output( i, True )

sleep(2)

print( "All output OFF" )
for i in range(8):
	tca.output( i, False )

print( "That s all Folks!")
```
