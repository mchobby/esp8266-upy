""" test.py - test the Weather Station

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Weather Station : https://shop.mchobby.be/product.php?id_product=2385
---> Raspberry-Pi Pico or Pico Wireless: https://shop.mchobby.be/fr/157-pico-rp2040
------------------------------------------------------------------------
History:
  16 march 2023 - Dominique - initial code writing
"""

from machine import UART
from weather import WeatherStation

# Raspberry-Pi Pico, GP4=TX, GP5=RX
u = UART( 1, 9600, timeout=100 )

ws = WeatherStation( u )
iter = 0
while True:
	iter += 1
	print( '' )
	# print( ws._buffer )
	print( 'New data received: %s - iteration %i' % (ws.update(),iter) )
	print( '  Wind Direction: %i degrees' % ws.wind_dir ) # 0..360
	print( '  Wind speed    : %f m/s (instantaneous)' % ws.wind_speed_real )
	print( '  Wind speed    : %f m/s (mean last minute)' % ws.wind_speed )
	print( '  Wind speed    : %f m/s (max last 5 minutes)' % ws.wind_speed_max )
	print( '  Rain cycles   : %i bucket (counter, 0-9999)' % ws.rain_cycle_real )
	print( '  Rain cycles   : %i bucket (last minute)' % ws.rain_cycle )
	print( '  Rain          : %f mm (last minute)' % ws.rain_mm )
	print( '  Rain          : %f mm (last hour)' % ws.rain_mm_hour )
	print( '  Rain          : %f mm (last 24H)' % ws.rain_mm_day )
	print( '  Temperature   : %f Celcius' % ws.temp )
	print( '  Humidity      : %f %%Rel' % ws.hrel )
	print( '  Pressure      : %f hPa' % ws.pressure )
