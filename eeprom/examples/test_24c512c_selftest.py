# Self test a 24C02C EEPROM - This test destroy the content of EEPROM
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/24cxx
#
from machine import I2C
from eeprom24cxx import Eeprom_24C512C, dump
import random

i2c = I2C( 1 )

eeprom = Eeprom_24C512C( i2c, addr=0x50 ) # 64K bytes, 512K bits

def self_test( eeprom ):
	""" Test an EEPROM, write a random data then read it back and compare the result """
	for mem_addr in range( eeprom.capacity ):
		# Stay in the range of a byte!
		value = random.randint( 0, 255 ) & 0xFF
		# Write the value to eeprom
		eeprom.write( mem_addr, value )
		# re-read the value from eeprom (extract the byte from bytes)
		check = eeprom.read( mem_addr )[0]
		if value==check:
			status='passed'
		else:
			status='FAILED'
		print(  "%8s : %s. Written %s readed %s" % (hex(mem_addr), status,'{:02X}'.format(value),'{:02X}'.format(check) ) )

dump( eeprom )

run_it = True
if run_it == True:
	print( "Self-Testing EEPROM!")
	self_test( eeprom )
	print( " " )
	print( "IF all tests fails THEN check the level of WP (Write Protect) pin!" )
else:
	print( "This test will overwrite the content of the EEPROM!")
	print( "Change the 'run_it' variable to True to run it!")
