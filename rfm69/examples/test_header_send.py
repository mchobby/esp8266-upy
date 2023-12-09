""" Send message with RFM69HCW SPI module - SENDER node

Must be tested togheter with test_header_rec.py

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""

from machine import SPI, Pin
from rfm69 import RFM69
import time

spi = SPI(0, miso=Pin(4), mosi=Pin(7), sck=Pin(6), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
# Set an encryption key (16 byte AES key). MUST match both side
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )
# Alternative way to write it
# rfm.encryption_key = bytes( [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8] )

# --- Node address ---
rfm.node    = 111 # This instance is the node 111
# rfm.node    = 0xFF # default node address (Broadcast address)

# --- Destination address ---
rfm.destination = 123 # Send to a given target node 123
# rfm.destination = 0xFF # default destination value for broadcasting

counter = 0
while True:
	counter += 1
	msg = "Send message %i!" % counter
	print( msg )
	# send a message with USER DEFINED:
	#   - Identifier (8bits, 0..255)
	#   - Flags (4 bits, 0..15)
	#
	rfm.send( bytes(msg, "utf-8"), identifier=(counter%20), flags=0b1011 )
	time.sleep(4)
