# Self test a 24C02C EEPROM - This test destroy the content of EEPROM
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/24cxx
#
from machine import I2C
from mcp24cxx import MCP24Cxx, CHIP_MCP24C02C

i2c = I2C( 2 )

eeprom = MCP24Cxx( i2c, addr=0x50, chip=CHIP_MCP24C02C ) # 256 bytes

for mem_addr in range( 256 ):
	data = eeprom.read( mem_addr ) # Read one byte
	print( "0x%2s = %s" % ( hex(mem_addr), data[0]) )
