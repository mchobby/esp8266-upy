"""
Test the MicroPython driver for M5Stack U136/U134, BH1750FVI Ambiant Light Sensor, I2C grove.
* Author(s):
   22 Aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from dlight import *
from time import sleep

# Pico - I2C(1) - sda=GP6, scl=GP7
i2c = I2C(1)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

ambiant = AmbiantLight(i2c)
# Set the mode
# CONTINUOUSLY_H_RESOLUTION_MODE
# CONTINUOUSLY_H_RESOLUTION_MODE2
# CONTINUOUSLY_L_RESOLUTION_MODE
# ONE_TIME_H_RESOLUTION_MODE
# ONE_TIME_H_RESOLUTION_MODE2
# ONE_TIME_L_RESOLUTION_MODE
ambiant.set_mode( CONTINUOUSLY_H_RESOLUTION_MODE )
while True:
	print( 'Light: %i Lux' % ambiant.lux )
	sleep( 0.200 )
