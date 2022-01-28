
""" test2.py - test the I2C Joystick was_pressed feature

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
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

joy = Joystick_I2C( i2c )

while True:
	print( '------------------------')
	print( 'Pausing for 5 sec' )
	time.sleep( 5 )
	print( "Was Pressed : ", joy.was_pressed )
