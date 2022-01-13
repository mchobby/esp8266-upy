"""
test.py - test the I2C keypad

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

------------------------------------------------------------------------

History:
  10 january 2022 - Dominique - initial portage from Arduino to MicroPython
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
print( 'Press buttons: * to exit reading loop')
while True:
	kpad.update_fifo()
	_btn = kpad.button # Return ASCII code
	while _btn != 0:
		print( "ASCII: %s,  Char: %s" % (_btn, chr(_btn) ) )
		if _btn == 42:
			raise Exception( 'User Exit!' )
		kpad.update_fifo()
		_btn = kpad.button # read next
	time.sleep_ms( 200 )
