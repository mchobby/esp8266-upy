[This file also exists in FRENCH here](readme.md)

# Measuring %Rel humidity and temperature with SI7005 sensor with MicroPython

![SI7005 on NCD mini board](ncd_si7005.png)

The SI7005 is a digital relative humidity and temperature sensor.
* +/- 4.5 %RH
* +/- 0.5 °C

This monolithic CMOS IC integrates:
* temperature and humidity sensor elements,
* an analog-to-digital converter,
* signal processing,
* calibration data, and
* an I2C host interface.

Both the temperature and humidity sensors are factory-calibrated and the calibration data is stored in the on-chip non-volatile memory. Ideal solution for measuring temperature, humidity, and dew-point, in a number of industrial and consumer applications.

Applications of the SI7005 include:
* respiratory therapy,
* white goods,
* asset/goods tracking and
* automotive climate control.

## About NCD Modules
The NCD I2C Mini Modules are designed with a standard & convenient 4-Pin plug connector. Thanks to the connector, it eliminating the need for soldering and the devices can be daisy-chained onto the I2C Bus.

This NCD SI7005 module includes on-board power regulation and PCA9306 I2C level-shifting circuitry to adapt to 5V I2C bus.

# Wiring

It is a I2C sensor based on NCD connector, so use the appropritate interface to connect it. This repository propose NCD interface for [MicroPython Pyboard](https://github.com/mchobby/pyboard-driver/blob/master/NCD/README.md) and [ESP modules](../NCD/readme.md).

![Wiring with Feather ESP8266](../NCD/ncd_feather.png)

Notice that __National Control Device propose [many adapter board](https://store.ncd.io/shop/?fwp_product_type=adapters) __ for many development plateform.

# Testing
Copy the file `si70x.py` and `test.py` on your MicroPython board.

The `test.py` file (listed here under) can be loaded from REPL session with `import test`

```
from machine import I2C, Pin
from si70x import SI7005
import time

# Create the I2C bus accordingly to your plateform.
# Pyboard: SDA on Y9, SCL on Y10.
#         Default bus Freq 400000 = 400 Khz is to high.
#         So reduce it to 100 Khz. Do not hesitate to test with 10 KHz (10000)

i2c = I2C( 2, freq=100000 )
# Feather ESP8266: sda=2, scl=4.
# i2c = I2C( sda=Pin(2), scl=Pin(4) )

mpl = SI7005( i2c )
i = 0
while True:
	i += 1
	print( '--- Iteration %s %s' % (i,'-'*20) )
	# tuple (hrel, temp)
	print( 'raw_values ', mpl.raw_values ) # computer Friendly humidity, temp
	print( 'values ', mpl.values ) # Human Friendly values
```

which produce the following results:

```
...
--- Iteration 1669 --------------------
raw_values  (54.875, 24.25)
values  ('54.88 %HRel', '24.21875 C')
--- Iteration 1670 --------------------
raw_values  (54.9375, 24.25)
values  ('54.94 %HRel', '24.21875 C')
--- Iteration 1671 --------------------
raw_values  (54.9375, 24.21875)
values  ('54.94 %HRel', '24.25 C')
--- Iteration 1672 --------------------
raw_values  (54.875, 24.25)
values  ('54.88 %HRel', '24.21875 C')
--- Iteration 1673 --------------------
raw_values  (54.875, 24.21875)
values  ('54.94 %HRel', '24.25 C')
--- Iteration 1674 --------------------
raw_values  (54.875, 24.25)
values  ('54.88 %HRel', '24.21875 C')
```

# Where to buy
* NCD-SI7005 : http://shop.mchobby.be/
* NCD-SI7005 : https://store.ncd.io/product/si7005-humidity-and-temperature-sensor-%c2%b14-5rh-%c2%b10-5c-i2c-mini-module/
