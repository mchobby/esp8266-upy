""" test_simple.py - use the Serial PMS5003 (PM2.5) to read air quality

based on Adafruit example
   https://github.com/sparkfun/Qwiic_Keypad_Py/blob/main/examples/qwiic_keypad_ex3.py

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> PM2.5 (PMS5003) : https://shop.mchobby.be/product.php?id_product=1332
---> PM2.5 Air Quality (PMS5003) : https://www.adafruit.com/product/3686
---> PMS5003 Particulate Matter Sensor : https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable
---> Raspberry-Pi Pico : https://shop.mchobby.be/fr/157-pico-rp2040

------------------------------------------------------------------------

History:
  02 april 2022 - Dominique - initial code writing
"""
from machine import UART
from pm25 import PM25
import time

# Raspberry Pico : GP0=tx (not used), GP1=rx (used)
ser = UART( 0, baudrate=9600, timeout=800 )
pm25 = PM25( ser )

while True:
	pm25.acquire()
	print( '-'*40 )
	print( 'Concentration Units (standard)')
	print( '  pm1.0: %i' % pm25.data.std.pm10 )
	print( '  pm2.5: %i' % pm25.data.std.pm25 )
	print( '  pm10.0: %i' % pm25.data.std.pm100 )
	print( 'Concentration Units (Environmental)')
	print( '  pm1.0: %i' % pm25.data.env.pm10 )
	print( '  pm2.5: %i' % pm25.data.env.pm25 )
	print( '  pm10.0: %i' % pm25.data.env.pm100 )
	print( 'Particle > x um / 0.1L air')
	print( '  0.3um: %i' % pm25.data.particles.um03 ) # Particles > 0.3 µM / 0.1L air
	print( '  0.5um: %i' % pm25.data.particles.um05 ) # Particle > 0.55 µM / 0.1L air
	print( '  1.0um: %i' % pm25.data.particles.um10 )# Particle > 1.0 µM / 0.1L air
	print( '  2.5um: %i' % pm25.data.particles.um25 )
	print( '  5.0um: %i' % pm25.data.particles.um50 )
	print( '  10.0um: %i' % pm25.data.particles.um100 )
	time.sleep(1)
