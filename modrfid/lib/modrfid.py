""" MicroPython Driver for MOD-RFID1356MIFARE

   Written by Meurisse D. for MCHobby.be

   oct 05, 2019 - v0.1 - Initial commit.
"""
# Todo: implement the write_block () method

from binascii import unhexlify
from time import sleep

# Error code + reduced message as defined @ https://www.olimex.com/wiki/MOD-RFID1356MIFARE
RFID_READER_ERROR = { 0x01 : "Time Out, the target has not answered",
 0x02 : "A CRC error has been detected by the contactless UART",
 0x03 : "A Parity error has been detected by the contactless UART",
 0x04 : "erroneous Bit Count detected MIFARE anticollision/select operation",
 0x05 : "Framing error during MIFARE operation",
 0x06 : "An abnormal bit-collision detected during",
 0x07 : "Communication buffer size insufficient",
 0x09 : "RF Buffer overflow on the contactless UART",
 0x0a : "RF field has not been switched on in time by the counterpart",
 0x0b : "RF Protocol error (CL_ERROR register)",
 0x0d : "Temperature error: overheating, antenna switched off",
 0x0e : "Internal buffer overflow",
 0x10 : "Invalid parameter (range, format, ...)",
 0x12 : "DEP Protocol: command received not supported by PN532",
 0x13 : "DEP Protocol / Mifare / ISO/IEC 14443-4: specification error",
 0x14 : "Mifare: Authentication error (improper Key used)",
 0x23 : "ISO/IEC 14443-3: UID Check byte is wrong",
 0x7f : "unknown command" }

# MiFare default authentification Key for new cards is 0xFFFFFFFFFFFF
DEFAULT_AUTH_KEY = 'FFFFFFFFFFFF'

class RfidError( Exception ):
	pass

class RFID_READER():
	""" Class to handle MOD-RFID1536-MIFARE from Olimex LTD.

	:param uart: a machine.UART that must be initialized at 38400 baut and timeout = 500 """
	def __init__( self, uart, debug=False ):
		self.uart = uart
		self.debug = debug
		self._read_eeprom = False # Set to True is user required to read the data

		self._last_error = 0  # Last error code returned by the RFID reader
		self._last_id = None  # UID of last card ID
		self._blocks  = None  # dictionnary blocks[n] = bytes() of last readed card (blocks appears after data.
		self.clear()

	#==== Public method ========================================================

	def clear( self ):
		# Clear all the data of last readed card
		self._last_error = 0
		self._last_id = None
		self._blocks  = None

	def update( self, pumping = False ):
		""" Call this as often as possible to read incoming data and
		    process the content of messages.

			"""

		data = self.uart.readline()
		if self.debug and data:
			print( ' << ',data )

		# ignore all lines without data
		if not(data):
			return

		# ignore all lines wuth command prompt invitation
		if data[0]==62: # >
			return

		if data[0]==45: # -
			self.clear() # prepare to parse a new card
			self.parse_id( data )
			if self._read_eeprom:
				# Pumping until a final OK at the end of of block reading
				count = 0
				while count < 30:
					_data = self.update( pumping = True )
					if _data == 'OK':
						return
					count += 1

		if b'Block' in data:
			self.parse_block( data )

		if data[0:4]==b'ERR:':
			self.handle_error( data )

		# pumping the messages until an OK is received (the send_command() use case)
		if pumping:
			if b'OK' in data:
				return 'OK' # OK
			else:
				return data # The caller is pumping the data for its own purpose

	#==== Helpers ==============================================================
	def send_command( self, sCmd, max_read=20, as_string=False ):
		# Send command to RFID module. Return OK if it has been received shortly
		#     after the command otherwise, it will be None.
		# If the command issue an error code in return (ERR:0x00) then the
		#     underlaying code will raise an exception
		#
		# :param max_read: number of line to read until an OK. Data in between
		#                   will be stored to be returned.
		# :param as_string: will transform the readed bytes() into string type (and remove CR/LF)
		# Returns: a Tuple ( OK_received, list_of_data )
		data = sCmd.encode('ascii')
		if self.debug:
			print( ' >> ', data )
		self.uart.write( data )
		self.uart.write( bytes([13,10]) )
		# Pump messages, look for OK or Handle Error
		count = 0
		messages = []
		while count<max_read: # Pump until 20 messages or OK
			r = self.update( pumping = True )
			if r == "OK":
				return (True, messages)
			else:
				if r: # returned data may also be None
					if as_string:
						messages.append( r.decode('utf8').replace('\r','').replace('\n','') )
					else:
						messages.append( r ) # bytes data
			count += 1
		sleep( 0.100 )
		return (False,messages)

	def reader_info( self ):
		""" Get firmware information from RFID reader """
		is_ok,lst = self.send_command( "i" , max_read = 5, as_string=True ) # Response should comes within the 5 lines
		return lst # a list of string

	def eeprom_read( self, enabled ):
		""" Enable/disable EEPROM reading """
		self._read_eeprom = enabled
		is_ok,lst = self.send_command( "e%s" % (1 if enabled else 0), max_read=2 )

	def read_blocks( self, from_block, to_block=None ):
		""" Reader must read a given block toghether with UID (block at a given index 0..x).
		    And range of blocks can calso be mentionned """
		if not(to_block):
			self.send_command( "er%s" % from_block , max_read = 2)
		else:
			self.send_command( "er%s,%s" % (from_block,to_block), max_read = 2)

	def write_block( self, from_block, data ):
		""" Make the reader writing a block X with the 16 byte data.

		:param from_block: Int, must be a valid block Number
		:param data: must by a string encoding 16 bytes under hex representation
		            (eg: 56E4747CBA08040001162D9CE5D0731D) or encoded into a bytes() type."""
		raise NotImplementedError('zut alors!')

	def set_key( self, key, value ):
		""" Set a new authentication key 'a' or 'b' with the defined value (hex, 6 bytes) """
		assert key in ('a','b'), "Only key a or b"
		assert len(value)==12, "key value must be a 6 bytes key encoded under Hex format. Eg: AA12BB34EEFF"
		is_ok,lst = self.send_command( "k%s,%s" % (key,value), max_read=2 )
		return is_ok

	def set_scan_interval( self, time_ms ):
		assert 1 < time_ms < 30000
		is_ok,lst = self.send_command( "mt%i" % time_ms, max_read=2 )
		return is_ok

	def set_led_mode( self, enabled ):
		is_ok,lst = self.send_command( "ml%s" % (1 if enabled else 0), max_read=2 )
		return is_ok

	def set_work_key( self, key ):
		""" Select the key to be used """
		assert key in ('a','b'), "Only key a or b"
		is_ok,lst = self.send_command( "mk%s" % key, max_read=2 )
		return is_ok

	def get_work_key( self ):
		""" Which is the current working key and its value (into a tuple) """
		try:
			is_ok, lst = self.send_command( "k?", max_read=4, as_string=True )
		except RfidError as err:
			# An error ERR:0x10 may be returned is the working key is not set
			return (None, None)

		if not(is_ok):
			return (None,None)
		for s in lst:
			if 'Key' in s:
				keyname  = s.split(':')[0].replace('Key','').strip().lower()
				keyvalue = s.split(':')[1].strip()
				return (keyname,keyvalue)
		return (None,None)

	def get_key( self, key ):
		""" Retreive the authentication key. None is not vailable """
		assert key in ('a','b'), "Only key a or b"
		is_ok,lst = self.send_command( "k%s" % key, max_read = 6, as_string=True )
		if not(is_ok):
			return None
		for s in lst:
			if ('Key %s : '%key.upper()) in s:
				return s.split(':')[1].strip()
		return None

	#==== Parsing ==============================================================
	def handle_error( self, data ):
		# Received an error code encoded like b'ERR:0x14\n'
		# See https://www.olimex.com/wiki/MOD-RFID1356MIFARE for details
		hex_error = data[4:8].decode('utf8') # extract '0x14'
		self._last_error = unhexlify( data[6:8].decode('utf8') )[0] # extract 20
		if self._last_error in RFID_READER_ERROR:
			raise RfidError( '%s : %s' % (hex_error, RFID_READER_ERROR[self._last_error]) )
		raise RfidError( 'Undefined %s error' % hex_error)


	def parse_id( self, data ):
		self._last_id = data[1:9].decode('utf8')

	def parse_block( self, data ):
		_split = data.decode('utf8').split(':') # Block 5 : 00 00 00 ... 00
		block_nr = _split[0].strip().split('ock')[1].strip() # Block  5
		block_d  = _split[1].replace(' ','')       # 00 00 00 ... 00
		# Create eeprom block storage
		if not(self._blocks):
			self._blocks = {}
		self._blocks[int(block_nr)] = block_d

	#==== Members ==============================================================
	@property
	def has_card( self ):
		return self._last_id != None

	@property
	def has_blocks( self ):
		return self._blocks and len(self._blocks)>0

	@property
	def blocks( self ):
		return self._blocks

	@property
	def last_error( self ):
		return self._last_error

	@property
	def card_id( self ):
		return self._last_id
