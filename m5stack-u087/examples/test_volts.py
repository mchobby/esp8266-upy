"""
Test the MicroPython driver for M5Stack U087, Vmeter Unit, I2C grove.

Just make a read of the voltage in Volts

* Author(s):
   08 july 2021: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from vmeter import *
from time import sleep

# Pico - I2C(1) - sda=GP8, scl=GP9
i2c = I2C(1, freq=10000)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

vmeter = Voltmeter(i2c)
while True:
	# use get_voltage() for value in mV
	# use voltage for value in Volts
	print( 'Voltage: %5.3f Volts' % vmeter.voltage )
	sleep( 0.3 )
