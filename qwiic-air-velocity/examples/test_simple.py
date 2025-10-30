"""
test_simple.py - test the basic feature of FS3000-1015  (0 to 15m/s) SparkFun SEN-18768.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://www.sparkfun.com/products/18768

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  28 oct 2025 - Dominique - initial script
"""

from machine import I2C,Pin
from airspeed import FS3000, AIRFLOW_RANGE_15_MPS
import time

# Raspberry-Pi Pico
i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )

# Adresse par défaut (0x72)
# Ajouter parametre address=0x38 pour une adresse personnalisée
air_speed = FS3000( i2c )

# Set the range to match which version of the sensor you are using.
#   FS3000-1005 (0-7.23 m/sec) --->>>  AIRFLOW_RANGE_7_MPS
#   FS3000-1015 (0-15 m/sec)   --->>>  AIRFLOW_RANGE_15_MPS
# air_speed.set_range( AIRFLOW_RANGE_7_MPS )
air_speed.set_range( AIRFLOW_RANGE_15_MPS )

while True:
	print( "FS3000 read raw:", air_speed.read_raw() ) # 125ms acquisition
	# read in Meter Per Second, returns a float from 0 - 7.23 for FS3000-1005, 0 - 15 for FS3000-1015 
	airflow_mps = air_speed.read_mps()
	if airflow_mps != None: # WILL returns None when  CRC error!
		print( "   m/s:", airflow_mps ) 
		airflow_kmh = airflow_mps*3600/1000
		print( "   Km/h:", airflow_kmh ) 
		airflow_mph = airflow_mps*2.2369362912
		print( "   Miles/h:", airflow_mph ) 
	time.sleep( 1 )
