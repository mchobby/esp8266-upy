# Simple demo for MPR121 capacitive sensor.
#
# Print the state of each entry key (0 to 11) on the MPR121 once every second
#
# Please note that each call to is_touched() initiate a request on the I2C bus
# so this approach is not really efficient.

from machine import I2C
from time import sleep
from mpr121 import MPR121

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

mpr = MPR121( i2c )

while True:
	print( "="*40)
	for i in range(12): # 0 to 11
		if mpr.is_touched(i):
			print( "Entry %2s: TOUCHED" % i  )
		else:
			print( "Entry %2s: " % i  )
	sleep(1)
