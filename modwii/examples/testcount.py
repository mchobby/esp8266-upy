'''
Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.

display direction every 500ms
display the buttons pressure count every 2 seconds.

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
import time
from wiichuck import WiiChuck

# Pyboard
# i2c = I2C( 2 ) # Y10=SDA, Y9=SCL
i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

dir_time   = time.time()
count_time = time.time()
while True:
	if time.time()-dir_time > 0.5:
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
		print( "Joy direction : %s" % (direction) )
		dir_time = time.time()

	if time.time()-count_time > 2:
		# Test button states
		print( "C Button pressure count: %s" % wii.c_count )
		print( "Z Button pressure count: %s" % wii.z_count )
		count_time = time.time()

	wii.update()
	time.sleep_ms( 5 )
