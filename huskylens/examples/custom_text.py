""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This example shows how to draw custom text on HUSKYLENS UI.
  Library @ https://github.com/mchobby/esp8266-upy/tree/master/huskylens

Buy HUSKYLENS at:
 * https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html
 * https://www.dfrobot.com/product-1922.html

 History:
 * 2023-12-31 Created for MicroPython by [MCHobby](shop.mchobby.be)


 GNU Lesser General Public License.
 See <http:#www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
"""

from husky import *
from micropython import const
from machine import I2C
import time

# HUSKYLENS T=green=SDA; R=blue=SCL

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

hl.clear_text() # Clear any custom text drawed on the HuskyLens UI
hl.custom_text(  0, 0, "Demo" ) # X, Y, Message
hl.custom_text( 10,35, "10:35" )
