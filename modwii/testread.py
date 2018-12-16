'''
Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.

MOD-Wii-UEXT-NUNCHUCK : http://shop.mchobby.be/product.php?id_product=1416 
MOD-Wii-UEXT-NUNCHUCK : https://www.olimex.com/Products/Modules/Sensors/MOD-WII/MOD-Wii-UEXT-NUNCHUCK/  

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from machine import I2C, Pin
from time import sleep_ms
from wiichuck import WiiChuck

i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

while True:
	# Detect direction from boolean property
	direction = ''
	if wii.joy_up:
		direction = 'Up'
	elif wii.joy_down:
		direction = 'Down'
	elif wii.joy_right:
		direction = '>>>'
	elif wii.joy_left:
		direction = '<<<'

	print( "-"*20 )
	# Test button states
	print( "Button C: %s" % wii.c )
	print( "Button Z: %s" % wii.z )
	# print X, Y analog value + detected direction
	print( "Joy X, Y: %4d,%4d  (%s)" % (wii.joy_x, wii.joy_y, direction) )

	wii.update()
	sleep_ms( 150 )
