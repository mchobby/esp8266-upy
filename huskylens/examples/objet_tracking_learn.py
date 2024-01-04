""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This example:
  1) switch to object tracking.
  2) forget the learned object (then wait a second)
  3) start a new learning (for a new object, move around it).
  4) once learning achieved, switch-off learning.
     Then use simple.py to list objects and their positions.
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

ID1 = const(1) # in Object Tracking the only object is ID1

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

hl.algorithm = OBJECT_TRACKING
hl.forget() # Forget last learning (if any)
time.sleep(2)
hl.learn_once( ID1 )
print( "once learning achieved, switch-off learning." )
print( "Then use simple.py to list objects and their positions")
