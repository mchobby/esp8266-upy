"""
MAG3110 3 axis digital magnetometer.

Test the Olimex MOD-MAG / Sparkfun MAG3110 board (based on MAG3110). 
Just read values from sensor

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
mag.setDR_OS( DR_OS_1_25_32 )
# Set sensor in active mode
mag.start()

while True:
	# wait for a data to be ready
	if mag.data_ready:
		# read the (x,y,z) tuple
		xyz = mag.read() 
		print( 'x,y,z = %s,%s,%s ' % xyz )
	

print( "That's the end folks")