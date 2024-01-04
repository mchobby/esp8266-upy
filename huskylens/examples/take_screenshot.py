""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This example shows how to take a screenshoot and store it into the SD Card.
  Library @ https://github.com/mchobby/esp8266-upy/tree/master/huskylens

Buy HUSKYLENS at:
 * https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html
 * https://www.dfrobot.com/product-1922.html

 History:
 * 2024-01-01 Created for MicroPython by [MCHobby](shop.mchobby.be)

 GNU Lesser General Public License.
 See <http:#www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
"""

from husky import *
from micropython import const
from machine import I2C
import time

# === Setup ===============
# Raspberry-Pi Pico: SDA=green(T)=gp8, SCL=blue(R)=gp9
i2c = I2C( 0, freq=100000 ) # sda=Pin(8), scl=Pin(9
try:
	hl = HuskyLens( i2c=i2c )
except:
	print( "HuskyLens creation failure!" )
	print( "1. Please check the [Protocol Type] in HUSKYLENS (General Settings>>Protocol Type>>I2C)" )
	print( "2. Please check wiring." )
	raise

# Will always returns False! (No way to know if the picture was taken or not)
# In case of error (eg: no SD) the HuskyLens will display an error message on UI
# Image are saved on SD:/HUSKYLENS/<increasing-number>.bmp
# Image are encoded with PC bitmap, Windows 3.x format, 320 x -240 x 24
print( hl.screen_to_sd() )
