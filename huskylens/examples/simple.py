""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This simple example left the HUSKYLENS in the current algorithm/mode THEN
  list all the identified objects (Boxes & Arrows).
  Library @ https://github.com/mchobby/esp8266-upy/tree/master/huskylens

Buy HUSKYLENS at:
 * https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html
 * https://www.dfrobot.com/product-1922.html

 History:
 * 2024-01-01 created for MicroPython by [MCHobby](shop.mchobby.be)

 GNU Lesser General Public License.
 See <http:#www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
"""

from husky import *
from micropython import const
from machine import I2C, Pin
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

# === Main loop ===========
retry = 0 # reading object attempts
while True:
	# -- What should we read ? -----
	lst = hl.get_all()                   # request all blocks and arrows from HUSKYLENS

	# Nothing received ?
	#  => we do loop again with "continue"
	if not(lst):
		if retry%100 == 0:
			print( "No objects return from Huskylens! %i Retries" % retry )
		retry += 1
		continue

	retry = 0
	# -- Display received data ? -------
	print( "-----------------------------------" )
	# print( "frame number: %s" % hl.frame_number )    # The number of frame HUSKYLENS have processed.
	for idx,item in enumerate(lst):
		# Item in the resulting list are typed.
		if type(item) is Box:
			print( "item %i is a BOX. Center is %i,%i. Width=%i. Height=%i" % (idx, item.center.x, item.center.y, item.width, item.height)  )
		elif type( item ) is Arrow:
			print( "item %i is an Arrow. Origin is %i,%i, Target is %i,%i" % (idx, item.origin.x, item.origin.y, item.target.x, item.target.y) )
		else:
			print( 'item %i: %r' % (idx,item) ) # %r: Print object representation

	time.sleep( 0.7 ) # Make a pause to not overflood the screen
