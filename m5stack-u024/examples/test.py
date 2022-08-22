"""
Test the MicroPython driver for M5Stack U024, I2C Joystick Unit, I2C grove.
* Author(s):
   22 Aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from joyi2c import Joystick
from time import sleep

# Pico - I2C(1) - sda=GP6, scl=GP7
i2c = I2C(1)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

joy = Joystick(i2c)
while True:
	joy.update() # Query joystick over I2C and update internal
	print( "X: %4i, Y: %4i, Button: %s" % (joy.x, joy.y, joy.button) )
	sleep( 0.1 )
