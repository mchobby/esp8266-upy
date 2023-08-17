""" RFID/NFC pn532 driver for MicroPython

	Read a ISO14443A/MiFare tag and display UID and try to dump the 64
	memory blocks by using the default KEYA value (universal key).

Sponsor
* Lycee Francais Jean-Monnet, Bruxelles, Belgique

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/pn532-rfid
"""
# Based on Arduino example:
#   https://github.com/elechouse/PN532/blob/PN532_HSU/PN532/examples/readMifare/readMifare.pde
#
from pn_const import *
from hal_uart import PN_UART
from pn532 import PN532
from binascii import hexlify
from machine import Pin
import time

uart_hal = PN_UART( 1, Pin(12,Pin.OUT,value=1) ,1000 ) # Uart_ID, ResetPin, TimeOut ms
nfc = PN532( uart_hal )
nfc.begin()

print( nfc.firmware_version )

# configure board to read RFID tags
if( nfc.sam_config() ):
	print( "SAM configured")
else:
	print( "SAM configuration failure!")

print("Waiting for an ISO14443A/MiFare Card for DUMPING ...");
data = bytearray(16)  # Array to store the data while reading
authenticated = False # Flag to indicate if the sector is authenticated

while True:
	# Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
	# 'uid' will be populated with the UID otherwise None. uid length will
	# is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
	uid = nfc.read_passive_targetID( PN532_MIFARE_ISO14443A )

	if uid == 0x00:
		print("Communication Error!")
		continue
	elif uid != None:
		# Display some basic information about the card
		print("Found an ISO14443A card")
		print("  UID Length: %i bytes" % len(uid) )
		print("  UID Value: %s" % hexlify(uid).upper() )
		_l = hexlify( uid ).decode('ASCII').upper()
		_l = ' '.join(_l[i:i+2] for i in range(0, len(_l), 2)) # Insert space every two chars
		print("  UID      : %s" % _l )
	else:
		continue

	if len(uid)!=4:
		print( "Seems NOT to be a Mifare classic tag (4 byte UID)")
		print( "Skip memory dump!")
		time.sleep(1)
		continue

	# define the Universal key
	key_universal = bytes( [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] )

	# We probably have a Mifare Classic card ...
	print("Seems to be a Mifare Classic card (4 byte UID)");
	for current_block in range(64): # 0..63
		if nfc.mifareclassic_is_first_block(current_block):
			authenticated = False

		if not(authenticated):
			if current_block==0:
				# This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
				#   or 0xA0 0xA1 0xA2 0xA3 0xA4 0xA5 for NDEF formatted cards using key a,
				#   but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
				# key_nr=1 => keyb
				success = nfc.mifareclassic_authenticate_block(uid, current_block, 1, key_universal )
			else:
				# This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
				# or 0xD3 0xF7 0xD3 0xF7 0xD3 0xF7 for NDEF formatted cards using key a,
				# but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
				# key_nr=1 => keyb
				success = nfc.mifareclassic_authenticate_block(uid, current_block, 1, key_universal )
			if success:
				authenticated = True
			else:
				print("Block %02i : Authentication error!" % current_block )

		if not(authenticated):
			print("Block %02i : Skip dump (not authenticated)" % current_block )
			continue

		# Authenticated ... we should be able to read the block now
		# Dump the data into the 'data' array
		mv_data = memoryview( data )
		success = nfc.mifareclassic_read_data_block( current_block, mv_data[:] )
		if not(success):
			print("Block %02i : read failure!" % current_block )
			continue

		# Data seems to have been read ... spit it out
		_l = hexlify( data ).decode('ASCII').upper()
		_l = ' '.join(_l[i:i+2] for i in range(0, len(_l), 2)) # Insert space every two chars
		print( "Block %02i : %s" % ( current_block, _l ) )

	# Wait a bit before reading the card again
	time.sleep(1)
