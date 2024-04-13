"""
Test the MicroPython driver for M5Stack U088, SGP30 TVOC CO2 sensor, I2C grove.
* Author(s):
   11 Apr 2024: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C, Pin
from sgp30 import *
import time

# Pico - I2C(0) - sda=GP8, scl=GP9
i2c = I2C(0, sda=Pin.board.GP8, scl=Pin.board.GP9 )
sgp = SGP30( i2c=i2c )

# The first 10 to 20 reading will return "TVOC 0 ppb eCO2 400 ppm" because the
# sensor need to warm up and returns null values.
#
# The baseline method are used for calibration. Read more about it at
# https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/arduino-code#baseline-set-and-get-2980166
while True:
	eCO2, TVOC = sgp.iaq_measure()
	print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))

	# H2, Ethanol = sgp.raw_measure()
	# print("H2 = %d ticks \t Ethanol = %d ticks" % (eCO2, TVOC))
	time.sleep(1)
