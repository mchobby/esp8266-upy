# Self test a 24C02C EEPROM - This test destroy the content of EEPROM
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/24cxx
#
from machine import I2C
from mcp24cxx import Eeprom_24C02C

i2c = I2C( 2 )

eeprom = Eeprom_24C02C( i2c, addr=0x50 ) # 256 bytes

def show( eeprom ):
	""" simply list the content of the eeprom """
	for mem_addr in range( eeprom.capacity ):
		data = eeprom.read( mem_addr ) # Read one byte
		print( "%2s = %s" % ( hex(mem_addr), data[0]) )

def dump( eeprom  ):
	""" Dump EEPROM content with HexView format """
	for index in range( eeprom.capacity//8 ):
		base_addr = index * 8
		data = [ eeprom.read(base_addr+offset)[0] for offset in range(8) ]
		hex_repr = [ '{:02X}'.format(value) for value in data ]
		str_repr = [ chr(value) if 32 <=value<=126 else '.' for value in data ]
		print( "%4s : %s : %s" % ( hex(base_addr), ' '.join(hex_repr),''.join(str_repr) ) )

dump( eeprom )
