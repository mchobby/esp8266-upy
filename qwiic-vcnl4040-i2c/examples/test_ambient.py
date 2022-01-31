""" test_something.py - test the I2C VCNL4040, outputs ambient light readings to the terminal.

Point the sensor up and start the sketch. Then cover the sensor with your hand.
The readings decrease in value because there is less light detected.

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic VCNL4040   : https://www.sparkfun.com/products/15177
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
------------------------------------------------------------------------
History:
  29 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7


prox = VCNL4040( i2c )


prox.power_proximity( enable=False ) # Power down the proximity portion of the sensor
prox.power_ambient( enable=True ) # Power up the ambient sensor

while True:
	print("Ambient light level: ", prox.ambient )
	time.sleep_ms( 50 )
