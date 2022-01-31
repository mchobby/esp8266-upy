""" test.py - test the I2C VCNL4040 proximity sensor to raise interrupt on object proximity

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

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

prox = VCNL4040( i2c )
# Turn on the ambient sensor
prox.power_ambient( enable=True )

# Set the integration time for the proximity sensor 1 to 8 is valid
prox.set_prox_integration_time(8)

# Set the integration time for the ambient light sensor in milliseconds 80 to 640ms is valid
prox.set_ambient_integration_time(80)

# If sensor sees more than this, interrupt pin will go low
prox.set_prox_threshold( UPPER, 2000)
# The int pin will stay low until the value goes below the low threshold value
prox.set_prox_threshold( LOWER, 150)

# Enable both 'away' and 'close' interrupts
prox.prox_interrupt_type( VCNL4040_PS_INT_BOTH )

# Activates interruption pin. The INT pin is pulled low when an object is
# close to the sensor (value is above high threshold) and is reset to high when
# the object moves away (value is below low threshold).
# Get a multimeter and probe the INT pin to see this feature in action.
prox.prox_logic_mode( enable=True )
