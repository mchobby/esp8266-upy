""" Test of RFM69HCW SPI module - RECEIVER node
		Display the message
		Display the RadioHead header

Must be tested togheter with test_header_send.py

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
# Optionally set an encryption key (16 byte AES key). MUST match both side
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )

# --- Node address ---
rfm.node = 123 # This instance is the node 123
#rfm.node = 0xFF # use broadcast (as unconfigured address)

print("Waiting for packets...")
while True:
	# receives the data INCLUDING RadioHead header (4 bytes)
	packet = rfm.receive( with_header=True, timeout=2.0 ) # We have more time
	if packet is None:
		# Packet has not been received
		print(".")
	else:
		print( '-'*40 )
		print("Received (RAW)   :", packet )
		# ---- RadioHead packet header -----------------------------------------
		#  4 bytes header
		__destination = packet[0]
		print( 'destination node :', __destination ,  'BROADCAST' if __destination==0xFF else '', '(Hey it is me!)' if (rfm.node!=0xFF) and (__destination==rfm.node) else '' )
		# ID - contains seq count for reliable datagram mode - Third byte of the RadioHead header.
		#    Automatically set to the sequence number when send_with_ack() used.
		# node address - default is broadcast (First byte of the RadioHead header)
		#    The default address of this Node. (0-255).
		#    If not 255 (0xff) then only packets address will accept it.
		__node = packet[1]
		print( 'Sender node      :', __node ,  'BROADCAST' if __node==0xFF else '' )
		# destination address - default is broadcast (Second byte of the RadioHead header)
		#    The default destination address for packet transmissions. (0-255).
		#    If 255 (0xff) then any receiving node should accept the packet.
		__identifier = packet[2]
		print( 'Identifier       :', __identifier ,  '(a sequence number for reliable datagram)' )
		# flags - identifies ack/reetry packet for reliable datagram mode
		#  - Upper 4 bits reserved for use by Reliable Datagram Mode.
		#  - Lower 4 bits may be used to pass information.
		__flags = packet[3]
		print( 'Flags            :', __flags ,  bin(__flags) )
		print( '   _RH_FLAG_ACK  :', 'YES' if (__flags & 0x80) else 'no' )
		print( '   _RH_FLAG_RETRY:', 'YES' if (__flags & 0x40) else 'no' )
		print( '   user defined  :', hex(__flags & 0x0F), '(lower 4 bits)' )

		# ---- Extract USER message ---------------------------------------------
		# And decode to ASCII text
		packet_text = str(packet[4:], "ascii")
		print("Received (ASCII) :", packet_text)
