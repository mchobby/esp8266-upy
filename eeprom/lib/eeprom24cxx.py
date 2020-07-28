# Driver for EEProm 24Cxx of in various size using the I2C machine API
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/eeprom
#
# Example sourced from
#    https://raw.githubusercontent.com/dda/MicroPython/master/EEPROM.py
#    https://create.arduino.cc/projecthub/gatoninja236/how-to-use-i2c-eeprom-30767d
#

__version__ = '0.0.1'

import time
import struct

# EEPROM Chip - indicates the capacity
CHIP_24C02C  = 256   # 256 bytes, Single page of 256 x 8 bit
CHIP_24C64   = 8192  #  8 Kbytes, 64  Kbits
CHIP_24C128  = 16384 # 16 Kbytes, 128 Kbits
CHIP_24C256  = 32768 # 32 Kbytes, 256 Kbits
CHIP_24C512C = 65536 # 64 Kbytes, 512 Kbits

def dump( eeprom  ):
	""" Dump EEPROM content with HexView format
	    in row of 8 bytes each """
	old_debug = eeprom.debug
	eeprom.debug = False
	for index in range( eeprom.capacity//8 ):
		base_addr = index * 8
		data = [ eeprom.read(base_addr+offset)[0] for offset in range(8) ]
		hex_repr = [ '{:02X}'.format(value) for value in data ]
		str_repr = [ chr(value) if 32 <=value<=126 else '.' for value in data ]
		print( "%4s : %s : %s" % ( hex(base_addr), ' '.join(hex_repr),''.join(str_repr) ) )
	eeprom.debug = old_debug

class Eeprom_Base:
	""" Descendant must implements read() and write() methods """

	def __init__(self, i2c, addr, chip ):
		self.debug = False
		self.i2c = i2c
		self.address = addr
		self.capacity= chip
		if 1<=self.capacity<=0xFF+1:
			self.addr_bytes = 1 # 256 bytes : 8 bits addressing
		elif 0xFF+1 < self.capacity <= 0xFFFF+1:
			self.addr_bytes = 2 # up to 64 Kb : 16 bits addressing
		elif 0xFFFF+1 < self.capacity <= 0xFFFFFF+1:
			self.addr_bytes = 3 # up to 16Mb : 24 bits addressing
		elif 0xFFFFFF+1 < self.capacity <= 0xFFFFFFFF+1:
			self.addr_bytes = 4 # up to 4 Gb : 32 bits addressing
		else:
			raise Exception( 'Cannot handle over 4 bytes addressing!')
		# Allocate Write Buffer space for address + space for 1 byte of data
		self.wbuf = bytearray( self.addr_bytes+1 )
		self.rbuf = bytearray( self.addr_bytes ) # Buffer for read operation

	def write(self, mem_addr, value):
		assert mem_addr < self.capacity, "%s address outside EEPROM capacity" % hex(mem_addr)
		# MSBF
		for i in range( self.addr_bytes ):
			self.wbuf[i] = (mem_addr >> ((self.addr_bytes-1-i)*8) ) & 0xFF
		self.wbuf[self.addr_bytes] = value
		self.i2c.writeto( self.address, self.wbuf)
		time.sleep_ms( 50 )
		if self.debug:
			print( "%4s : W : %s" % ( hex(mem_addr),'{:02X}'.format(value) ))

	def read(self, mem_addr, count=1 ):
		""" Returns one or more bytes from EEPROM. Return bytes object """
		assert mem_addr < self.capacity, "%s address outside EEPROM capacity" % hex(mem_addr)
		# MSBF
		for i in range( self.addr_bytes ):
			self.rbuf[i] = (mem_addr >> ((self.addr_bytes-1-i)*8) ) & 0xFF
		self.i2c.writeto( self.address, self.rbuf)
		data = self.i2c.readfrom( self.address, count )
		if self.debug:
			print( "%4s : R : %s" % ( hex(mem_addr),data ) )
		return data

	def erase( self, value=0xFF ):
		""" Erase the content of the EEPROM """
		old_debug = self.debug
		self.debug = False
		for i in range( self.capacity ):
			self.write( mem_addr=i, value=value )
		self.debug = old_debug

	def check_magic( self, mem_addr, values ):
		""" Check magic key stored into EEPROM @ mem_addr with the list of values """
		data = self.read( mem_addr, len(values) )
		for i in range(len(values)):
			if data[i] != values[i]:
				return False
		return True

	def write_magic( self, mem_addr, values ):
		""" Write the magic key into the EEPROM @ mem_addr. Values is either a list() of bytes, either a bytes() object """
		offset = 0
		for value in values:
			self.write( mem_addr+offset, value )
			offset += 1
		return len(values) # Number of bytes written

	def byte_write( self, mem_addr, a_byte ):
		""" Write a value from 0 to 255. Return the number of bytes written."""
		assert 0<=a_byte<=255, 'Invalid range for byte'
		self.write( mem_addr, a_byte )
		return 1

	def byte_read( self, mem_addr ):
		""" Return the value of the byte """
		return self.read( mem_addr )[0]

	def sint_write( self, mem_addr, a_int ):
		""" Write (-32768 to 32767) short int stored on 2 bytes  """
		assert -32768 <= a_int <= 32767, "Invalid range -32768 to 32767"
		self.write_magic( mem_addr, struct.pack(">h", a_int) ) # 2 bytes
		return 2

	def sint_read( self, mem_addr ):
		""" Read (-32768 to 32767) short int from memory """
		return struct.unpack( ">h", self.read( mem_addr, count=2) )[0]

	def usint_write( self, mem_addr, a_int ):
		""" Write (0 to 65535) unsigned short int stored on 2 bytes """
		assert 0 <= a_int <= 65535, "Invalid range 0 to 65535"
		self.write_magic( mem_addr, struct.pack(">H", a_int) ) # 2 bytes
		return 2

	def usint_read( self, mem_addr ):
		""" Read (0 to 65535) Unigned short int from memory """
		return struct.unpack( ">H", self.read( mem_addr, count=2) )[0]

	def int_write( self, mem_addr, a_int ):
		""" Write (-2,147,483,648 to 2,147,483,647) SIGNED long integer """
		self.write_magic( mem_addr, struct.pack(">i",a_int) ) # 4 bytes
		return 4

	def int_read( self, mem_addr ):
		""" Read (-2,147,483,648 to 2,147,483,647) Unigned short int from memory """
		return struct.unpack( ">i", self.read( mem_addr, count=4) )[0]

	def float_write( self, mem_addr, a_float ):
		""" write float to memory """
		self.write_magic( mem_addr, struct.pack(">f",a_float) ) # 4 bytes
		return 4

	def float_read( self, mem_addr ):
		""" Read float from memory """
		return struct.unpack( ">f", self.read( mem_addr, count=4) )[0]

	def string_write( self, mem_addr, a_string, storage_length ):
		""" Store a string, storage Length is also stored in one byte """
		# fill space with Null char then overwrite the null with the string characters.
		# String will be cut @ storage_length when longer
		assert storage_length <= 255, 'Max 255 chars'
		self.byte_write( mem_addr, storage_length )
		self.write_magic( mem_addr+1, struct.pack("%is"%storage_length,a_string.encode('UTF-8') ) )
		return storage_length+1

	def string_read( self, mem_addr ):
		""" Read a string stored at the the mem_addr location intp the storage_length area """
		storage_length = self.byte_read( mem_addr )
		bin = struct.unpack("%is"%storage_length, self.read(mem_addr+1, storage_length) )[0]
		return bin.decode("UTF-8").rstrip('\x00')

class Eeprom_24C02C( Eeprom_Base ):
	""" 2KBits EEPROM (256 bytes). Memory addressed with only one byte! """
	def __init__(self, i2c, addr=0x50 ):
		super( Eeprom_24C02C, self ).__init__(i2c,addr,chip=CHIP_24C02C)

class Eeprom_24C512C( Eeprom_Base ):
	""" 512KBits EEPROM (64 Kbytes). Memory addressed with only one byte! """
	def __init__(self, i2c, addr=0x50 ):
		super( Eeprom_24C512C, self ).__init__(i2c,addr,chip=CHIP_24C512C)
