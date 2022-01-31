""" test.py - test the I2C VCNL4040 proximity sensor to read IR, ambient and white light.

Along with proximity and ambient light sensing the VCNL4040 has a 'white light'
sensor as well. Point the sensor up and start the sketch. Then cover the sensor with your hand.
	* IR readings increase as the reflected IR light increases
	* Ambient light readings decrease as less ambient light can get to the sensor
	* White light readings decrease as less white light is detected

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic VCNL4040   : https://www.sparkfun.com/products/15177
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
------------------------------------------------------------------------
History:
  28 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

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
