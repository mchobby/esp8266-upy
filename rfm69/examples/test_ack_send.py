""" Send with ACK test of RFM69HCW SPI module - SENDER node

Must be tested togheter with test_ack_rec.py

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
rfm.node    = 111 # This instance is the node 111

print( 'Temperature     :', rfm.temperature, 'Celsius' )
print( 'Freq            :', rfm.frequency_mhz )
print( 'Freq. deviation :', rfm.frequency_deviation, 'Hz' )
print( 'bitrate         :', rfm.bitrate, 'bits/sec' )
print( 'NODE            :', rfm.node )

# Send a packet and waits for its ACK.
# Note you can only send a packet up to 60 bytes in length.
rfm.destination = 123 # Send to spécific node 123
for i in range(10):
	print("Send with ACK %i!" % i)
	ack = rfm.send_with_ack(bytes("Send with ACK %i!\r\n" % i , "utf-8"))
	print("   +->", "ACK received" if ack else "ACK missing" )
	time.sleep(1)
