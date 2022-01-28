
""" test.py - test the I2C Joystick for general functions

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic Joystick   : https://www.sparkfun.com/products/15168
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
------------------------------------------------------------------------
History:
  27 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from machine import I2C, Pin
from joyi2c import Joystick_I2C
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

joy = Joystick_I2C( i2c )

print( 'Joystick connected:', 'Yes' if joy.is_connected else 'NO' )
print( 'Version:', joy.version )
print( 'Vertical/Horizontal range 0..1024' )
print( '')
print( 'Button is pressed, X (horizontal), y (vertical)')
print( '-'*40 )
while True:
	print( '%5s, %4i, %4i ' % (joy.pressed, joy.x, joy.y) )
	time.sleep( 0.200 )
