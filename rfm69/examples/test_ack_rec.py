""" Receive message requiring ACK - test of RFM69HCW SPI module - RECEIVER node

Must be tested togheter with test_ack_send.py

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

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )
rfm.node = 123 # This instance is the node 123

print( 'Temperature     :', rfm.temperature, 'Celsius' )
print( 'Freq            :', rfm.frequency_mhz )
print( 'Freq. deviation :', rfm.frequency_deviation, 'Hz' )
print( 'bitrate         :', rfm.bitrate, 'bits/sec' )
print( 'NODE            :', rfm.node )
# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.

print("Waiting for packets...")
while True:
	packet = rfm.receive( with_ack=True )
	# Optionally change the receive timeout from its default of 0.5 seconds:
	# packet = rfm.receive(timeout=5.0)
	# If no packet was received during the timeout then None is returned.
	if packet is None:
		# Packet has not been received
		print("Received nothing! Listening again...")
	else:
		# Received a packet!
		print( "Received (raw bytes):", packet )
		# And decode to ASCII text
		packet_text = str(packet, "ascii")
		print("Received (ASCII):", packet_text)
