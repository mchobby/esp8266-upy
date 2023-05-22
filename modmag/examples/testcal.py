"""
MAG3110 3 axis digital magnetometer. 

Shows how to use the built-in calibration and get a heading with 
   the Olimex MOD-MAG / Sparkfun MAG3110 board (based on MAG3110)

Calibration only works with a level sensor orientation and uses only x and y axes.
 
TO CALIBRATE: spin the sensor around 360 degrees.
  The calibration mode exits after 5-10 seconds.

MOD-MAG board : http://shop.mchobby.be/product.php?id_product=1413
MOD-MAG : https://www.olimex.com/Products/Modules/Sensors/MOD-MAG/open-source-hardware  
User Guide : https://www.olimex.com/Products/Modules/Sensors/MOD-MAG/resources/MOD-MAG.pdf 

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
"""

from machine import I2C, Pin
from time import sleep
from mag3110 import MAG3110, DR_OS_1_25_32

i2c = I2C( sda=Pin(2), scl=Pin(4) )
mag = MAG3110( i2c ) 

print( "CHIP ID: %s" % mag.who_am_i() )

# Set the output data rate (1.25 Hz) and oversampling ratio (32 times) 
#   mag.setDR_OS( DR_OS_1_25_32 )

# Set sensor in active mode
mag.start()
 
while True:
	# Not yet calibrated ?
	if not mag.is_calibrated:
		# Not yet calibrating ?
		if not mag.is_calibrating:
			print( "Starting calibration mode!")
			mag.enter_calibration()
		else:
			mag.step_calibration()
	else:
		print( "Calibrated" )
		break

	# display MAG info while calibrate
	#   (x,y,z) tuple
	# xyz = mag.read() 
	# print( xyz )
	
print( 'User Offset = %s,%s,%s' % mag.user_offset() )
#mag.setDR_OS( DR_OS_1_25_32 )
while True:
    if mag.data_ready:
        print( 'x,y,z = %s,%s,%s ' % mag.read() )
        heading = mag.heading()
        print( 'Heading = ', heading )
        print( '-'*40 )	
        sleep( 3 )

print( "That's the end folks")
