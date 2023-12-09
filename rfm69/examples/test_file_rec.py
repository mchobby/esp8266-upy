""" Test the rfmtrf.py of RFM69HCW SPI module - file RECEIVER node

Must be tested togheter with test_file_send.py

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""

from machine import SPI, Pin
from rfm69 import RFM69
from rfmtrf import StreamReceiver
import time

spi = SPI(0, miso=Pin(4), mosi=Pin(7), sck=Pin(6), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )
rfm.node    = 123 # This instance is the node 123


receiver = StreamReceiver( rfm=rfm, svc_id=0x01 ) # File Transfert service
receiver.listen()
