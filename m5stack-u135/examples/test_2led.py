"""
Test the MicroPython driver for M5Stack U135, I2C Encoder unit, I2C grove.

Control each of the LEDs

* Author(s):
   03 aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from i2cenc import I2CEncoder
from time import sleep

# Pico - I2C(0) - sda=GP8, scl=GP9
i2c = I2C(0)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

enc = I2CEncoder(i2c)

enc.set_led( 1, (255,0,0) ) # Red
enc.set_led( 2, (0,255,0) ) # Green
sleep( 2 )
enc.color = (0,0,0) # ALL Off
