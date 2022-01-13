"""
test2.py - Read I2C keypad key + delay between reading & action.

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

------------------------------------------------------------------------

History:
  11 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from machine import I2C, Pin
from kpadi2c import Keypad_I2C
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

kpad = Keypad_I2C( i2c )
print( 'KeyPad connected:', 'Yes' if kpad.is_connected else 'NO' )
print( 'Version:', kpad.version )
while True:
	kpad.update_fifo()
	_btn   = kpad.button # Return ASCII code
	_deltaT= kpad.time_since_pressed
	if _btn == 0: # no reading
		time.sleep_ms( 200 )
		continue # restart loop

	print( "Button %s was pressed %d milliseconds ago." % (chr(_btn),_deltaT) )
