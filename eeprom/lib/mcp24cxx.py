# Driver for EEProm 24Cxx of in various size using the I2C machine API
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/eeprom
#
# Example sourced from
#    https://raw.githubusercontent.com/dda/MicroPython/master/EEPROM.py
#

__version__ = '0.0.1'

CHIP_MCP24C02C =  256  # 256 bytes, Single page of 256 x 8 bit

class MCP24Cxx:

	def __init__(self, i2c, addr=0x50, chip=CHIP_MCP24C02C ):
		self.i2c = i2c
		self.address = addr
		self.capacity= chip

	def read(self, mem_addr, count=1 ):
		# Read from EEPROM
		#data = bytearray(count)
		#data[0]=eeaddress >> 8 #MSB
		#data[1]=eeaddress & 0xFF #LSB
		#i2c.send(data, addr=self.address)
		#value=i2c.recv(1, self.address)
		#return value[0]
		assert mem_addr < self.capacity, "%s address outside EEPROM range" % mem_addr

		return self.i2c.readfrom_mem( self.address, mem_addr, count )

	def write(self, mem_addr, value):
		raise Exception( 'not implemented' )
		#data = bytearray(3)
		#data[0]=eeaddress >> 8 #MSB
		#data[1]=eeaddress & 0xFF #LSB
		#data[2]=value
		#i2c.send(data, addr=self.address)
		#time.sleep(.05)
