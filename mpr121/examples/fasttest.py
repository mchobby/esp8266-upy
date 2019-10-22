# Simple demo for MPR121 capacitive sensor.
#
# Print the state of each entry key (0 to 11) on the MPR121 once every second
#
# This version is more efficient by using touched() to initiate ONLY ONE I2C request
# and decode the result for ALL the pins at once.

from machine import I2C
from time import sleep
from mpr121 import MPR121

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

mpr = MPR121( i2c )

touched = bytearray( 12 ) # will contains the value for every pin

while True:
	print( "="*40)
	# Reading and decoding (as fast as possible)
	data = mpr.touched()
	for i in range( 12 ):
		touched[i] = 1 if data & (1<<i) else 0

	# Display the result
	for i in range(12): # 0 to 11
		if touched[i]: # Value > 0 means touched!
			print( "Entry %2s: TOUCHED" % i  )
		else:
			print( "Entry %2s: " % i  )
	sleep(0.1)
