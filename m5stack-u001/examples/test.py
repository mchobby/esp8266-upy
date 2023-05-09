"""
Test the MicroPython driver for M5Stack U001-C ENV III, SHT30 + QMP6988, I2C grove.
* Author(s):
   23 Aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from sht3x import SHT3x
from qmp6988 import QMP6988
from time import sleep

# Pico - I2C(1) - sda=GP6, scl=GP7
i2c = I2C(1)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

sht = SHT3x(i2c, address=0x44)
qmp = QMP6988(i2c)
while True:

	t = sht.temperature
	h = sht.humidity
	p = qmp.pressure # in Pascal

	print( 'Temp: %3.1f C, Hum: %3i %%Rh, Pressure: %6i Pa' % (t, h, p) )
	sleep( 0.500 )
