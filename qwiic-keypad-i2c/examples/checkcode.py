""" checkcode.py - use the I2C keypad to check entry code

based on SparkFun example on following link
   https://github.com/sparkfun/Qwiic_Keypad_Py/blob/main/examples/qwiic_keypad_ex3.py

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
from kpadcode import CodeChecker
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

def update_display( user_entry, timeout ):
	if timeout:
		print( 'Callback: timeout!' )
	print( 'Callback: "%s"' % user_entry )

locker = CodeChecker( i2c, address=0x4B, code='1234*' )
locker.on_update = update_display
print( 'KeyPad connected:', 'Yes' if locker.is_connected else 'NO' )
print( 'Version:', locker.version )

locked = True
while locked:
	print( '==== Enter KeyCode to Unlock ====' )
	locked = not( locker.execute() )
	if locked:
		print( 'Execute() timeout! Try again' )

# Loop exits only when code is right
print( 'Yes! Unlocked!' )
print( '')
print( '')
print( "That's all Folks!" )
