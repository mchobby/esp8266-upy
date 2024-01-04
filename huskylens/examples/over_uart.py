""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  This example shows how to setup the link to HUSKYLENS via UART.
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
from machine import UART
import time

# === Setup ===============
# Raspberry-Pi Pico:
UART(2,baudrate=9600,rx=33,tx=32,timeout=100)
try:
	hl = HuskyLens( uart=uart )
except:
	print( "HuskyLens creation failure!" )
	print( "1. Please check the [Protocol Type] in HUSKYLENS (General Settings>>Protocol Type>>UART 9600)" )
	print( "2. Please check wiring." )
	raise

# Switch the algorithm on HUSKYLENS to make Line Tracking
hl.algorithm = LINE_TRACKING

# === Main loop ===========
retry = 0 # reading object attempts
while True:
	# -- What should we read ? -----
	lst = hl.get_arrows()              # request only arrows from HUSKYLENS

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
	# We do expect an Arrows object in the list
	arrow = lst[0]
	print( "Origin is %i,%i, Target is %i,%i" % (arrow.origin.x, arrow.origin.y, arrow.target.x, arrow.target.y) )

	time.sleep( 0.5 ) # Make a pause to not overflood the screen
