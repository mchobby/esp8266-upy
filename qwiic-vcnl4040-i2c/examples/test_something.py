""" test_something.py - test the I2C VCNL4040, Something present

This example takes an initial reading at power on. If the reading changes
by a significant amount the sensor reports that something is present.
Point the sensor up and start the sketch. Then bring your hand infront of the sensor.

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).
Products:
---> SparkFun Qwiic VCNL4040   : https://www.sparkfun.com/products/15177
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400
------------------------------------------------------------------------
History:
  29 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from machine import I2C, Pin
from vcnl4040 import VCNL4040
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

prox = VCNL4040( i2c )

startingProxValue = 0
deltaNeeded = 0
nothingThere = False

# Set the current used to drive the IR LED - 50mA to 200mA is allowed.
prox.set_led_current( 200 ) # The max

# The sensor will average readings together by default 8 times.
# Reduce this to one so we can take readings as fast as possible
prox.set_prox_integration_time(8) # 1 to 8 is valid

# Take 8 readings and average them
for i in range( 8 ):
	startingProxValue += prox.proximity
startingProxValue /= 8

# Calculate a Delta
deltaNeeded = startingProxValue * 0.05 # Look for 5% change
if deltaNeeded < 5:
	deltaNeeded = 5 # Set a minimum

while True:
	value = prox.proximity
	#print( "Proximity Value: ", value )

	# Let's only trigger if we detect a 5% change from the starting value
	# Otherwise, values at the edge of the read range can cause false triggers
	if value > (startingProxValue + deltaNeeded):
		print("Something is there!" )
		nothingThere = False
	else:
		if nothingThere == False:
			print( "I don t see anything" )
		nothingThere = True

	time.sleep_ms(10)
