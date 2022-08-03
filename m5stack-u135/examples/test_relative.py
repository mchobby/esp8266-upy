""" Test the MicroPython driver for M5Stack U135, I2C Encoder unit, I2C grove.

Set the color of RGB led by turning the knob. Press the know to switch between
R,G,B color values.

Remark:
As the writing of position value to the I2C encoder is not working, we will
use a software based relative position reader (thank to I2CRelEncoder).

* Author(s):
   03 aug 2022: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from i2cenc import I2CRelEncoder
from time import sleep

# Pico - I2C(0) - sda=GP8, scl=GP9
i2c = I2C(0)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

enc = I2CRelEncoder(i2c)

current_color = [0,0,0] # RGB
COLOR_NAME = ["Red", "Green", "Blue" ]
COLOR_VALUE = [(255,0,0), (0,255,0), (0,0,255)]
index = 0 # 0..2 to defined r, g, b colot
print( "turn to change the color intentity" )
print( "Click to change the fundamental R,G,B color update" )

def show_info_color( idx ):
	assert 0<=idx<=2
	global enc, current_color
	print( "We are defining the color %s" % COLOR_NAME[idx] )
	for i in range( 5 ):
		enc.color = COLOR_VALUE[idx]
		sleep(0.150)
		enc.color = (0,0,0)
		sleep(0.150)
	# restore current color
	enc.color = current_color

def show_alert():
	global enc, current_color
	enc.color = (255,255,255)
	sleep(0.100)
	enc.color = (0,0,0)
	sleep(0.100)
	enc.color = current_color

index=0
show_info_color( index )
last_value = current_color[ index ]
enc.reset()
last_pos = enc.rel_position
last_value_for_message = 0
while True:
	pos = enc.rel_position
	if pos != last_pos: # Position changed ?

		# What is the new color value
		v = last_value + (pos-last_pos)
		if v>255:
			v=255
			show_alert()
		elif v<0:
			v=0
			show_alert()

		if v != last_value_for_message: # Only print it when the value had changed
			print( "%s = %i" % (COLOR_NAME[index],v) )
			last_value_for_message = v
		current_color[index] = v
		enc.color = current_color


	if enc.button: # Is the button currently pressed ?
		index = (index+1)%3
		show_info_color( index )
		last_value = current_color[ index ]
		last_value_for_message = 0
		enc.reset()
		last_pos = enc.rel_position

	sleep( 0.05 )
