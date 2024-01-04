""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This advanced example shows the full function of library for HUSKYLENS via I2c.
  Library @ https://github.com/mchobby/esp8266-upy/tree/master/huskylens

Buy HUSKYLENS at:
 * https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html
 * https://www.dfrobot.com/product-1922.html

History:
 * 2023-12-28 Ported to MicroPython by [MCHobby](shop.mchobby.be)
 * 2020-03-13 Created for Arduino By [Angelo qiao](Angelo.qiao@dfrobot.com)

 GNU Lesser General Public License.
 See <http:#www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
"""

from husky import *
from micropython import const
from machine import I2C, Pin
import time

# HUSKYLENS T=green=SDA; R=blue=SCL

ID0 = const(0) # not learned results. Grey result on HUSKYLENS screen
ID1 = const(1) # first learned results. colored result on HUSKYLENS screen
ID2 = const(2) # second learned results. colored result on HUSKYLENS screen
# and so on.....

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

# Uncomment one of the following code to switch the algorithm on HUSKYLENS.
#   Otherwise HuskyLens will continue use the currently selected algorithm.
#
# hl.algorithm = FACE_RECOGNITION
# hl.algorithm = OBJECT_TRACKING
# hl.algorithm = OBJECT_RECOGNITION
# hl.algorithm = LINE_TRACKING
# hl.algorithm = COLOR_RECOGNITION
# hl.algorithm = TAG_RECOGNITION
# hl.algorithm = OBJECT_CLASSIFICATION # not tested yet

# === Main loop ===========
retry = 0 # reading object attempts
while True:
	# -- What should we read ? -----
	lst = hl.get_all()                   # request all blocks and arrows from HUSKYLENS
	# lst = hl.get_blocks()              # request only blocks from HUSKYLENS
	# lst = hl.get_arrows()              # request only arrows from HUSKYLENS

	# lst = hl.get_all( learned=True )   # request blocks and arrows tagged ID != 0 from HUSKYLENS
	# lst = hl.get_blocks( learned=True )# request blocks tagged ID != ID0 from HUSKYLENS
	# lst = hl.get_arrows( learned=True )# request arrows tagged ID != ID0 from HUSKYLENS

	# lst = hl.get_by_id( ID1 )             #request blocks and arrows tagged ID == ID1 from HUSKYLENS
	# lst = hl.get_by_id( ID1, block=True ) #request blocks tagged ID == ID1 from HUSKYLENS
	# lst = hl.get_by_id( ID1, arrow=True ) #request arrows tagged ID == ID1 from HUSKYLENS
	# lst = hl.get_by_id( ID2 )             #request blocks and arrows tagged ID == ID2 from HUSKYLENS

	# -- Nothing received ? -------
	#  => we do loop again with "continue"
	if not(lst):
		# only notifies USER every 100 reading (to not overflood the screen)
		if retry%100 == 0:
			print( "No objects return from Huskylens! %i Retries" % retry )
		retry += 1
		continue

	# -- Display received data ? -------
	retry = 0
	print( "-----------------------------------" )
	print( "Current Algorithm: %s" % ALGORTHIM_NAMES[hl.algorithm]) # None/Undefined means that library doesn't know the active selection on HuskyLens
	print( "Count of learned IDs: %s" % hl.learned ) # The count of (faces, colors, objects or lines) you have learned on HUSKYLENS.
	print( "frame number: %s" % hl.frame_number )    # The number of frame HUSKYLENS have processed.
	print( "HuskyLens response. Count: %s" % hl.count )
	for idx,item in enumerate(lst):
		print( 'item %i: %r' % (idx,item) ) # %r: Print object representation

		# Item in the resulting list are typed.
		# So we can use the extra properties the offers by the class.
		if type(item) is Box:
			print( "item is a BOX. Center is %i,%i. Width=%i. Height=%i" % (item.center.x, item.center.y, item.width, item.height)  )
		elif type( item ) is Arrow:
			print( "item is an Arrow. Origin is %i,%i, Target is %i,%i" % (item.origin.x, item.origin.y, item.target.x, item.target.y) )

	time.sleep( 0.5 ) # Make a pause to not overflood the screen
