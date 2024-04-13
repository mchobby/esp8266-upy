""" VEML6075 : Ultraviolet (UV) Sensor with MicroPython

  This example makes raw data reading from the sensor.
  Library @ https://github.com/mchobby/esp8266-upy/tree/master/veml6075

Buy VEML6075 at:
 * https://shop.mchobby.be/en/environnemental-press-temp-hum-gas/1881-gravity-veml6075-uv-sensor-i2c-3232100018815-dfrobot.html
 * https://www.dfrobot.com/product-1906.html

History:
 * 2024-01-21 Portage to MicroPython by [MCHobby](shop.mchobby.be)

"""

from veml6075 import *
from machine import I2C
import time

# === Setup ===============
# Raspberry-Pi Pico
i2c = I2C( 1, freq=100000 ) # sda=Pin(6), scl=Pin(7)
veml = VEML6075( i2c=i2c )
print( "UV_IT: %s " % veml.conf.UV_IT )
while True:
	uva_raw   = veml.read_uva_raw()        # read UVA raw (uint16)
	uvb_raw   = veml.read_uvb_raw()        # read UVB raw (uint16)
	comp1_raw = veml.read_uv_comp1_raw()   # read COMP1 raw (uint16)
	comp2_raw = veml.read_uv_comp2_raw()   # read COMP2 raw (uint16)

	uva = veml.uva           # get UVA (float)
	uvb = veml.uvb           # get UVB (float)
	uvi = veml.uvi(uva, uvb) # get UV index (float)

	print("")
	print("======== start print ========")
	print("UVA   raw: %s" % uva_raw )
	print("UVB   raw: %s" % uvb_raw )
	print("COMP1 raw: %s" % comp1_raw )
	print("COMP2 raw: %s" % comp2_raw )
	print("")
	print("UVA    : %s" % uva )
	print("UVB    : %s" % uvb )
	print("UVIndex: %.2f" % uvi )
	print("UVIndex:    ")
	if uvi < UVI_LOW:
		print("  UVI low")
	elif uvi < UVI_MODERATE:
		print("  UVI moderate")
	elif uvi < UVI_HIGH:
		print("  UVI high")
	elif Uvi < UVI_VERY_HIGH:
		print("  UVI very high")
	else:
		print("  UVI extreme")

	print("mw/cm^2: %.2f" % uvi_to_mwpcm2(uvi) )

	print("======== end print ========")
	time.sleep(1)
