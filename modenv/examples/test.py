"""
MOD-ENV Environmental sensor with CCS811 & BME280 in MicroPython
================================================================
* CCS811 - Air Quality Sensor Breakout - VOC and eCO2.
* BME280 - Temperature, Atmospherique Pressure, Relative Humidity

See https://github.com/mchobby/esp8266-upy/tree/master/modenv for more information

Author(s):
* Meurisse D for MC Hobby sprl

"""
import time
import ccs811
import bme280

from machine import I2C

i2c = I2C( 2 )
ccs811 = ccs811.CCS811( i2c )
bme = bme280.BME280( i2c=i2c )

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
	values = bme.raw_values # Temperature, pressure hPa, %Rel Humidity
	print("CO2: {} PPM, TVOC: {} PPB, Temp: {} C, hPa: {}, Rh {} percent".format(ccs811.eco2, ccs811.tvoc, values[0], values[1], values[2]) )

	time.sleep(0.5)
