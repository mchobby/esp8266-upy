# Driver for EEProm 24Cxx of in various size using the I2C machine API
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/eeprom
#
# Example sourced from
#    https://raw.githubusercontent.com/dda/MicroPython/master/EEPROM.py
#    https://create.arduino.cc/projecthub/gatoninja236/how-to-use-i2c-eeprom-30767d
#

__version__ = '0.0.1'

# EEPROM Chip - indicates the capacity
CHIP_24C02C =  256  # 256 bytes, Single page of 256 x 8 bit

class Eeprom_Base:
	""" Descendant must implements read() and write() methods """

	def __init__(self, i2c, addr, chip ):
		self.i2c = i2c
		self.address = addr
		self.capacity= chip

	def check_magic( self, mem_addr, values ):
		""" Check magic key stored into EEPROM @ mem_addr with the list of values """
		data = self.read( mem_addr, len(values) )
		for i in range(len(values)):
			if data[i] != values[i]:
				return False
		return True

class Eeprom_24C02C( Eeprom_Base ):
	""" 2KBits EEPROM (256 bytes). Memory addressed with only one byte! """
	def __init__(self, i2c, addr=0x50 ):
		super( Eeprom_24C02C, self ).__init__(i2c,addr,chip=CHIP_24C02C)

	def read(self, mem_addr, count=1 ):
		""" Returns one or more bytes from EEPROM """
		assert mem_addr < self.capacity, "%s address outside EEPROM capacity" % hex(mem_addr)

		return self.i2c.readfrom_mem( self.address, mem_addr, count )

	def write(self, mem_addr, value):
		raise Exception( 'not implemented' )
		#data = bytearray(3)
		#data[0]=eeaddress >> 8 #MSB
		#data[1]=eeaddress & 0xFF #LSB
		#data[2]=value
		#i2c.send(data, addr=self.address)
		#time.sleep(.05)
