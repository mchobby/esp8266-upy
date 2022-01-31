""" test_readprox.py - test the I2C VCNL4040 read proximity - is_close, is_away

     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr
     CAN'T GET IT TO WORK! grrrrrr


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
from vcnl4040 import VCNL4040, UPPER, LOWER, VCNL4040_PS_INT_BOTH
import time

from machine import I2C, Pin
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

prox = VCNL4040( i2c )

prox.power_proximity( enable=True ) # Power down the proximity portion of the sensor
prox.power_ambient( enable=True ) # Power up the ambient sensor

# Set the integration time for the proximity sensor 1 to 8 is valid
prox.set_ambient_integration_time(8)
prox.set_prox_integration_time(8)

prox.set_als_threshold( UPPER, 350)
prox.set_als_threshold( LOWER, 50)

prox.set_prox_threshold( UPPER, 2000)
prox.set_prox_threshold( LOWER, 150)

prox.set_ambient_interrupt_persistance(1)
prox.enable_ambient_interrupts( enable=True )

# Enable both 'away' and 'close' interrupts
prox.prox_interrupt_type( VCNL4040_PS_INT_BOTH )

while True:
	prox.proximity
	prox.ambient
	print( "is dark" if prox.is_dark else "", "is light" if prox.is_light else "")
	print( "is close" if prox.is_close else "", "is away" if prox.is_away else "" )
	time.sleep_ms(10)
