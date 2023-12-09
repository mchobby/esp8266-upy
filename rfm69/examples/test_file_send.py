""" Test the rfmtrf.py of RFM69HCW SPI module - file SENDER node

Must be tested togheter with test_file_rec.py

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""

from machine import SPI, Pin
from rfm69 import RFM69
from rfmtrf import StreamSender
import time

spi = SPI(0, miso=Pin(4), mosi=Pin(7), sck=Pin(6), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )
rfm.node    = 111 # This instance is the node 111


sender = StreamSender( rfm=rfm, destination=123 )
sender.send( filename="demo.py", stream=None, with_exit=True )
