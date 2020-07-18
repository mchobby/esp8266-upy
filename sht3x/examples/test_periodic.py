""" Read data for a SHT31-F sensor

test_periodic.py - activate the periodic read on the SHT31-F then try to read
  the data made available by the SHT31 at every period cycle

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
import time
from machine import I2C
from sht3x import SHT3x, REPEATABILITY_HIGH, MEASUREFREQ_1HZ, NotReady

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

print( "Initial température : %s" % sht.temperature )
print( "Initial Humidity    : %s" % sht.humidity )

# startPeriodicMode Enter cycle measurement mode and set repeatability and read frequency.
#  - measureFreq Read the MEASUREFREQ_HZ5 (every 2s), MEASUREFREQ_1HZ  (every 1s)
#	 MEASUREFREQ_2HZ (every 0.5s), MEASUREFREQ_4HZ (every 0.25s), MEASUREFREQ_10HZ (every 0.1s)
# - repeatability Read the repeatability of temperature and humidity data, the default parameter is REPEATABILITY_HIGH.
#    REPEATABILITY_HIGH (humidity repeatability is 0.10%RH, the temperature repeatability is 0.06°C)
#    REPEATABILITY_MEDIUM (humidity repeatability is 0.15%RH, the temperature repeatability is 0.12°C).
#    REPEATABILITY_LOW  (humidity repeatability is0.25%RH, the temperature repeatability is 0.24°C)
# Returns True indicates success
if not sht.start_periodic_mode( MEASUREFREQ_1HZ, REPEATABILITY_HIGH ):
	print("Failed to enter the periodic mode")

print("------------------Read data in cycle measurement mode-----------------------")
ctime = time.time()
while True:
	try:
		_data = sht.tmp_rh # In periodic mode, data MUST be acquired in one operation
		print("Ambient temperature °C: %s" % _data[0] )
		print("Relative humidity(%%RH): %s" % _data[1] )
	except NotReady:
		print( 'Not ready!')

	# Please adjust the frequency of reading according to the frequency of the chip collection data.
	# The frequency to read data must be greater than the frequency to collect the data, otherwise the returned data will go wrong.
	time.sleep_ms( 300 )

	# Exit periodic read after 20 seconds
	if (time.time()-ctime) > 20:
		if sht.is_periodic:
			sht.stop_periodic_mode()
			print( "Exited from the cycle measurement mode, enter the single measurement mode" )
