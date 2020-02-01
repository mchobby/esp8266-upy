"""
CCS811 Air Quality Sensor Breakout - VOC and eCO2
======================================================================
This library supports the use of the CCS811 air quality sensor in MicroPython.

Author(s):
* Meurisse D for MC Hobby sprl

"""
import time
import ccs811

from machine import I2C

i2c = I2C( 2 )
ccs811 = ccs811.CCS811( i2c )

# Check if the sensor returns an error
if ccs811.check_error:
	print( "An error occured!")
	print( "ERROR_ID = %s" % ccs811.error_id.as_text )
	while True:
		time.sleep( 0.100 )

# Wait for the sensor to be ready
while not ccs811.data_ready:
	time.sleep( 0.100 )

while True:
    print("CO2: {} PPM, TVOC: {} PPB"
          .format(ccs811.eco2, ccs811.tvoc))
    time.sleep(0.5)
