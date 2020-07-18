""" Read data for a SHT31-F sensor

test.py - read the data of from SHT31-F over the I2C interface
* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).
Products:
---> https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/1882-sht31-f-capteur-d-humidite-et-temperature-3232100018822-dfrobot.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.
------------------------------------------------------------------------
History:
  18 july 2020 - Dominique - initial script
"""
from machine import I2C
from sht3x import SHT3x, REPEATABILITY_HIGH, REPEATABILITY_LOW
import time

i2c = I2C(1)
sht = SHT3x( i2c )
print( "Chip Serial Number %s" % hex(sht.serial_number) )


if sht.soft_reset():
	print( "Software Reset done")

# heaterEnable( activate ): Turn on the heater inside the chip to enable the sensor get correct humidity value in wet environments.
# Heaters should be used in wet environments, and other cases of use will result in incorrect readings
# Note that heater affect temperature reading !!!!

#heater_state = sht.heater( enabled=True )
#if not heater_state:
#	print( "Heater not activated" )
#else:
#	print( "Heater activated" )


# Read with selected repeatability
# temp,rh = sht.read_all( REPEATABILITY_LOW )

# Read with REPEATABILITY_HIGH
temp,rh = sht.tmp_rh
print( "Temp: %s, %%Humidity: %s" % (temp,rh) )

while True:
	print( "Temp: %s, %%Humidity: %s" %  sht.tmp_rh )
	# Just read temperature
	#    temp = sht.temperature
	# Just read relative humidity
	#    rh  sht.humidity
	time.sleep( 0.5 )
