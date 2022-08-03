"""
Test the MicroPython driver for M5Stack U135, I2C Encoder unit, I2C grove.

Test the common features of the I2C encoder.

* Author(s):
   03 aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from i2cenc import I2CEncoder
from time import sleep

# Pico - I2C(0) - sda=GP8, scl=GP9
i2c = I2C(0)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

enc = I2CEncoder(i2c)

print( "Testing the LEDs" )
enc.color = (255,0,0) # Red
sleep( 0.5 )
enc.color = (0,255,0) # Green
sleep( 0.5 )
enc.color = (0,0,255) # Blue
sleep( 1 )
enc.color = (0,0,0) # Off

print( "Press the button and rotate the switch")

last_v = 0
while True:
	if enc.button: # Is the button currently pressed ?
		print( 'Button PRESSED')
		enc.position = 0 # reset the counter - not working!

	v = enc.position # -32768 <= v <= 32767
	if v != last_v: # Only display if value changes
		print( v )
		last_v = v
	sleep( 0.05 )
