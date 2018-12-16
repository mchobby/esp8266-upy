'''
Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.

display accelerometer values every 500ms

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

i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

acc_time   = time.time()
while True:
	if time.time()-acc_time > 0.5:
		print( '-'*20 )
		print( "Joy Accelerometer x,y,z  : %4d, %4d, %4d" % (wii.accel_x, wii.accel_y, wii.accel_z) )
		# https://www.novatel.com/solutions/attitude/ 
		# pitch = airplane nose up/down
		# roll  = airplane rooling to right / left 
		print( "Joy roll, pitch (degrees): %4d, %4d" % (wii.roll, wii.pitch) )
		acc_time = time.time()

	wii.update()
	time.sleep_ms( 5 )
