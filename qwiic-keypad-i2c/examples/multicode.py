""" multicode.py - use the I2C keypad to check "one of many" entry code

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Keypad - 12 Button  : https://www.sparkfun.com/products/15290
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

------------------------------------------------------------------------

History:
  12 january 2022 - Dominique - initial portage from Arduino to MicroPython
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
	# diplay encoding length
	print( 'Callback: "%s"' % ('X'*len(user_entry.strip())) )

code_list = ['1*123','2*777','3*456','4*###','12345']

locker = CodeChecker( i2c, address=0x4B, code=code_list )
locker.on_update = update_display
print( 'KeyPad connected:', 'Yes' if locker.is_connected else 'NO' )
print( 'Version:', locker.version )
print( 'Valid codes: ',code_list)

while True:
	print( '==== Enter KeyCode  ====' )
	if locker.execute():
		print( 'Code "%s" catched!' % locker.user_entry )

print( "That's all Folks!" )
