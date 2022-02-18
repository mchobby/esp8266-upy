""" Basic test of RFM69HCW SPI module

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""

from machine import SPI, Pin
from rfm69 import RFM69

def dbm_to_mw(dBm):
	""" Transform the power in dBm to its equivalent in milliWatt """
	return 10**((dBm)/10.)

spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
rfm.bitrate = 250000 # 250 Kbs
rfm.frequency_deviation = 250000 # 250 KHz
rfm.tx_power = 13  # 13 dBm = 20mW (default value, safer for all modules)
#rfm.tx_power = 20 # 20 dBm = 100mW, 20 dBm for FRM69HW
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )

print( 'RFM version     :', rfm.version )
print( 'Freq            :', rfm.frequency_mhz )
print( 'Freq. deviation :', rfm.frequency_deviation, 'Hz' )
print( 'bitrate         :', rfm.bitrate, 'bits/sec' )
print( 'tx power        :', rfm.tx_power, 'dBm' )
print( 'tx power        :', dbm_to_mw(rfm.tx_power), 'mW' )
print( 'Temperature     :', rfm.temperature, 'Celsius' )
print( 'Sync on         :', 'yes' if rfm.sync_on else 'no' )
print( 'Sync size       :', rfm.sync_size )
print( 'Sync Word Length:', rfm.sync_size+1, "(Sync size+1)" )
print( 'Sync Word       :', rfm.sync_word )
print( 'CRC on          :', rfm.crc_on )

print( 'Preamble Lenght :', rfm.preamble_length )
print( 'aes on          :', rfm.aes_on )
print( 'Encryption Key  :', rfm.encryption_key )
