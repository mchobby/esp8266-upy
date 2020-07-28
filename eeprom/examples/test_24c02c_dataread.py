# Read back structured data from 24C02C EEPROM
#
# see the test_mcp24c02c_datawrite.py to initialize the EEPROM with data.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/24cxx
#
from machine import I2C
from eeprom24cxx import Eeprom_24C02C, dump

i2c = I2C( 1 )

eeprom = Eeprom_24C02C( i2c, addr=0x50 ) # 256 bytes
# eeprom.debug = True

print( "Read data from addr 0x00 ...")
if eeprom.check_magic( 0x00, bytearray('MCHOBBY') ):
	print("Magic key detected!")
else:
	raise Exception('No magic key! See test_mcp24c02c_datawrite.py to initialize EEPROM' )

print("Read 3 bytes. Should be 35,36,37")
data = eeprom.read( 0x07, count=3 )
for value in data:
	print( '   %i' % value )

print("Read version. Expected 15")
print( '   %i' % eeprom.byte_read( mem_addr=0x0A ) ) # 1 byte length

print("Read short signed int. Expected -4435")
print( '   %i' % eeprom.sint_read ( mem_addr=0x0B ) ) # 2 bytes length

print("Read unsigned short int. Expected 65123")
print( '   %i' % eeprom.usint_read ( mem_addr=0x0D ) ) # 2 bytes length

print("Read signed int. Expected 1000222") # 4 bytes length
print( '   %i' % eeprom.int_read ( mem_addr=0x0F ) ) # 4 bytes length

print("Read float. Expected 3.141592") # 4 bytes length
print( '   %f' % eeprom.float_read ( mem_addr=0x13 ) ) # 4 bytes length

print( "Read string. Expected Belgium")
print( '   %s' % eeprom.string_read( mem_addr=0x17 ) ) # storage_length was 20. So 21 bytes.

print( "Read boolean. Expected True")
# Address = 0x17 + 1 (storage_length) + 20 (storage_space)
a_bool = True if eeprom.byte_read( mem_addr=0x2c ) > 0 else False
print( '   %s' % a_bool )
