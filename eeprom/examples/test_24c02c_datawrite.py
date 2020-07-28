# Store/Write structured data into a 24C02C EEPROM
# see the test_mcp24c02c_dataread.py to read them.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/24cxx
#
from machine import I2C
from eeprom24cxx import Eeprom_24C02C, dump

i2c = I2C( 1 )

eeprom = Eeprom_24C02C( i2c, addr=0x50 ) # 256 bytes
# eeprom.debug = True
print( "Erasing %s bytes" % eeprom.capacity )
eeprom.erase()

print( "Writing data...")
mem_addr = 0
mem_addr += eeprom.write_magic( mem_addr, bytearray('MCHOBBY') ) # Write a Magic Key @ addr 0
mem_addr += eeprom.write_magic( mem_addr, [35,36,37] ) # Use a list to write values #$%
mem_addr += eeprom.byte_write ( mem_addr, 15 ) # version 15
mem_addr += eeprom.sint_write ( mem_addr, -4435 ) # Write a signed int (-32768 to 32767)
mem_addr += eeprom.usint_write ( mem_addr, 65123 ) # Write a usint (0 to 65535)
mem_addr += eeprom.int_write ( mem_addr, 1000222 ) # Write a long int -2 millard up to 2 milliard
mem_addr += eeprom.float_write ( mem_addr, 3.141592 ) # Write a float
mem_addr += eeprom.string_write( mem_addr, 'Belgium', 20) # Store a string into a 20
a_bool = True
mem_addr += eeprom.byte_write( mem_addr, 1 if a_bool else 0 )

dump( eeprom )
