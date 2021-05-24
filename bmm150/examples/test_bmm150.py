"""  BMM150 3 axis magnetic sensor - basic test on M5Stack Core

* Author(s):
   24 may 2021: Meurisse D. (shop.mchobby.be) - Porting example from NET

"""

from machine import I2C, Pin
import bmm150
import math
import time

# Create I2C bus on M5Stack core
i2c = I2C( sda=Pin(21), scl=Pin(22) )
# BMM150 is used at address 0x10 on M5Stack Core
bmm = bmm150.BMM150( i2c, address=0x10 )
print( 'initialized' )

value = bmm150.BMM150_Mag_Data()

while True:
	bmm.read_mag_data()
	# simplify code reading by copy the values
	value.x = bmm.raw_mag_data.raw_datax;
	value.y = bmm.raw_mag_data.raw_datay;
	value.z = bmm.raw_mag_data.raw_dataz;
	print( value.x , value.y , value. z )

	# calculation
	xyHeading = math.atan2( value.x, value.y )
	zxHeading = math.atan2( value.z, value.x )
	heading = xyHeading;
	if heading < 0:
		heading += 2*math.pi
	if heading > (2*math.pi) :
		heading -= 2*math.pi

	headingDegrees = heading * 180/math.pi
	xyHeadingDegrees = xyHeading * 180 / math.pi
	zxHeadingDegrees = zxHeading * 180 / math.pi

	print( "Heading:", headingDegrees )
	time.sleep_ms(100)
