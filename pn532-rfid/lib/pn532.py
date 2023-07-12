""" RFID/NFC pn532 driver for MicroPython

	Main library managing card operation.
	Uses a HAL (Hardware Abstaction Layer) to communicates with the PN532 Hardware.

Sponsor
* Lycee Francais Jean-Monnet, Bruxelles, Belgique

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/pn532-rfid
"""
# based on Arduino implementation
#      https://github.com/elechouse/PN532/blob/PN532_HSU/PN532/PN532.cpp

from pn_const import *

class PN532:
	def __init__( self, hal_interface ):
		self._hal = hal_interface # HArdware abstraction layer to communicate with PN532
		self.pn532_packetbuffer = bytearray( 64 )
		# uint8_t _uid[7];  // ISO14443A uid
		# uint8_t _uidLen;  // uid len
		# uint8_t _key[6];  // Mifare Classic key
		# uint8_t inListedTag; // Tg number of inlisted tag.
		# uint8_t _felicaIDm[8]; // FeliCa IDm (NFCID2)
		# uint8_t _felicaPMm[8]; // FeliCa PMm (PAD)


	def begin( self ):
		self._hal.wake_up()

	def get_firmware_version( self ):
		# Returns uint32_t response encoding Chipset & Firmware
		self.pn532_packetbuffer[0] = PN532_COMMAND_GETFIRMWAREVERSION

		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:1] ) != 0:
			return 0;

		# read data packet
		status = self._hal.read_response( mv_command[:] )
		#print( "getFirmwareVersion: status", status)
		if status < 0:
			return 0

		response = self.pn532_packetbuffer[0]
		response <<= 8
		response |= self.pn532_packetbuffer[1]
		response <<= 8
		response |= self.pn532_packetbuffer[2]
		response <<= 8
		response |= self.pn532_packetbuffer[3]
		return response

	@property
	def firmware_version( self ):
		_val = self.get_firmware_version()
		_chipset = "pn5%s" % hex((_val>>24)&0xFF).replace('0x','')
		_firmversion = "%s.%s" % ( (_val>>16) & 0xFF, (_val>>8) & 0xFF )
		return {"CHIPSET":_chipset, "FIRMWARE":_firmversion}

	def sam_config( self ):
		# Configure the SAM Security Access Module
		# Returns: True when everything is OK
		#print("PN532.sam_config: enter");
		self.pn532_packetbuffer[0] = PN532_COMMAND_SAMCONFIGURATION
		self.pn532_packetbuffer[1] = 0x01 # normal mode;
		self.pn532_packetbuffer[2] = 0x14 # timeout 50ms * 20 = 1 second
		self.pn532_packetbuffer[3] = 0x01 # use IRQ pin!

		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:4] ) != 0:
			return False

		status = self._hal.read_response( mv_command[:] )
		#print( "PN532.sam_config: response status=", status)
		return status >= 0 # Response can have a length of 0

	def read_passive_targetID( self, cardbaudrate ):
		#print("PN532.read_passive_targetID: enter");
		self.pn532_packetbuffer[0] = PN532_COMMAND_INLISTPASSIVETARGET
		self.pn532_packetbuffer[1] = 1  # max 1 cards at once (we can set this to 2 later)
		self.pn532_packetbuffer[2] = cardbaudrate

		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:3] ) != 0:
			return 0x0  # command failed

		# read data packet
		status = self._hal.read_response( mv_command[:] )
		#print( "PN532.read_passive_targetID: response status=", status )
		if status < 0: # otherwise status contains the number of bytes read
			return 0x0

		# check some basic stuff
		# ISO14443A card response should be in the following format:
		#   byte            Description
		#   -------------   ------------------------------------------
		#   b0              Tags Found
		#   b1              Tag Number (only one used in this example)
		#   b2..3           SENS_RES
		#   b4              SEL_RES
		#   b5              NFCID Length
		#   b6..NFCIDLen    NFCID

		if self.pn532_packetbuffer[0] != 1 :
			return None # No tag received

		sens_res = self.pn532_packetbuffer[2] << 8 # uint16_t
		sens_res += self.pn532_packetbuffer[3]

		# print("ATQA: %s" % hex(sens_res) )
		# print("SAK : %s" % hex(self.pn532_packetbuffer[4]) )

		# Card appears to be Mifare Classic
		_uidlen = self.pn532_packetbuffer[5]
		_uid = []
		for i in range( _uidlen ):
			_uid.append( self.pn532_packetbuffer[6 + i] )

		return bytes(_uid) # Return it as Immutable object

	def mifareclassic_authenticate_block( self, uid, block_nr, key_nr, key ):
		# Tries to authenticate a block of memory on a MIFARE card using the
		# INDATAEXCHANGE command.  See section 7.3.8 of the PN532 User Manual
		# for more information on sending MIFARE and other commands.
		#
		#  uid   the card UID. The length (in bytes) of the card's UID (Should
		#    		be 4 for MIFARE Classic)
		#  block_nr   The block number to authenticate.  (0..63 for 1KB cards, and 0..255 for 4KB cards).
		#  key_nr     Which key type to use during authentication (0 = MIFARE_CMD_AUTH_A, 1 = MIFARE_CMD_AUTH_B)
		#  key        key data binary containing the 6 bytes key value
		#
		# returns: True if everything executed properly, False for an error

		#	uint8_t i;
		#	// Hang on to the key and uid data
		#	memcpy (_key, keyData, 6);
		#	memcpy (_uid, uid, uidLen);
		#	_uidLen = uidLen;

		# Prepare the authentication command
		assert len(key)==6
		assert len(uid)==4
		self.pn532_packetbuffer[0] = PN532_COMMAND_INDATAEXCHANGE  # Data Exchange Header
		self.pn532_packetbuffer[1] = 1                             # Max card numbers
		self.pn532_packetbuffer[2] = MIFARE_CMD_AUTH_B if key_nr==MIFARE_CMD_AUTH_B else MIFARE_CMD_AUTH_A
		self.pn532_packetbuffer[3] = block_nr                      # Block Number (1K = 0..63, 4K = 0..255
		for i in range( len(key) ):
			self.pn532_packetbuffer[4+i] = key[i]
		for i in range( len(uid) ):
			self.pn532_packetbuffer[10 + i] = uid[i] # 4 bytes card ID

		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:10+len(uid)] ) != 0:
			return False

    	# Read the response packet
		status = self._hal.read_response( mv_command[:] )
		#print( "PN532.read_passive_targetID: response status=", status )
		if status < 0: # otherwise status contains the number of bytes read
			return False

		# Check if the response is valid and we are authenticated???
		# for an auth success it should be bytes 5-7: 0xD5 0x41 0x00
		# Mifare auth error is technically byte 7: 0x14 but anything other and 0x00 is not good
		if self.pn532_packetbuffer[0] != 0x00:
			print("Authentification failed")
			return False

		return True

	def mifareclassic_read_data_block( self, block_nr, data ):
		# Read the data of a given block and store them into a 16 bytes data array
		#    Please authenticate yourself first.
		# Returns: True when success
		assert len(data)==16

		# Prepare the command */
		self.pn532_packetbuffer[0] = PN532_COMMAND_INDATAEXCHANGE
		self.pn532_packetbuffer[1] = 1               # Card number
		self.pn532_packetbuffer[2] = MIFARE_CMD_READ # Mifare Read command = 0x30
		self.pn532_packetbuffer[3] = block_nr        # Block Number (0..63 for 1K, 0..255 for 4K)

		# Send the command
		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:4] ) != 0:
			return False

		# Read the response packet
		status = self._hal.read_response( mv_command[:] )
		if status < 0: # otherwise status contains the number of bytes read
			return False

		# If byte 8 isn't 0x00 we probably have an error (read_response only returns
		# the inner data and strips response header)
		if self.pn532_packetbuffer[0] != 0x00 :
			return False

		# Copy the 16 data bytes to the output buffer
		# Block content starts at byte 9 of a valid response
		for i in range(len(data)):
			data[i] = self.pn532_packetbuffer[i+1]

		return True

	def mifareclassic_write_data_block( self, block_nr, data ):
		# Write the 16 bytes of data to given block.
		#    Please authenticate yourself first.
		# Returns: True when success
		assert len(data)==16
		# Prepare the first command
		self.pn532_packetbuffer[0] = PN532_COMMAND_INDATAEXCHANGE;
		self.pn532_packetbuffer[1] = 1                 # Card number
		self.pn532_packetbuffer[2] = MIFARE_CMD_WRITE  # Mifare Write command = 0xA0
		self.pn532_packetbuffer[3] = block_nr          # Block Number (0..63 for 1K, 0..255 for 4K)
		for i in range( len(data) ):                        # Charge data Payload
			self.pn532_packetbuffer[4+i] = data[i]

		# Send the command
		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:20] ) != 0:
			return False

		# Read the response packet
		status = self._hal.read_response( mv_command[:] )
		if status < 0: # otherwise status contains the number of bytes read
			return False

		return True

	def mifareclassic_is_first_block( self, block_nr ):
		# Indicates if the block_nr is the first block of a sector
		# (0 based block_nr number)

		# Test if we are in the small or big sectors
		if block_nr < 128:
			return (block_nr % 4) == 0
		else:
			return (block_nr % 16) == 0
