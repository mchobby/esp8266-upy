""" RFID/NFC pn532 driver for MicroPython

	Access a ISO14443A/MiFare tag and display UID
	  THEN try to access the block number 4 with the default KEYA value
	  THEN write some data in block 4

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

# MicroPython alike implementation
print( nfc.firmware_version )

# configure board to read RFID tags
if( nfc.sam_config() ):
	print( "SAM configured")
else:
	print( "SAM configuration failure!")

print("Waiting for an ISO14443A/MiFare Card for writing...");

# Buffer for writing data
data_to_write = bytearray(16)

# Data to be written
sData = "MICROPYTHON HERE" # Exactly 16 bytes
for idx, val in enumerate( sData.encode('ASCII') ):
	data_to_write[idx] = val
print( "--- Data to Write ---")
print( sData ) # String representation
print( data_to_write ) # Binary representation
_l = hexlify( data_to_write ).decode('ASCII').upper()
_l = ' '.join(_l[i:i+2] for i in range(0, len(_l), 2)) # Insert space every two chars
print( _l ) # Hexadecimal représentation
print( "---------------------")
print( " " )


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

	if len(uid)==4:
		# We probably have a Mifare Classic card ...
		print("Seems to be a Mifare Classic card (4 byte UID)");

		# Now we need to try to authenticate it for read/write access
		# Try with the factory default KeyA: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
		print("Trying to authenticate block 4 with default KEYA value");
		keya = bytes( [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] )

		# Start with block 4 (the first block of sector 1) since sector 0
		# contains the manufacturer data and it's probably better just
		# to leave it alone unless you know what you're doing
		#
		# Block_nr=4, KeyNr=0
		success = nfc.mifareclassic_authenticate_block(uid, 4, 0, keya)

		if not( success ):
			print("Ooops ... authentication failed: Try another key?")
			time.sleep(1)
			continue

		print("Sector 1 (Blocks 4..7) has been authenticated");
		mv_data = memoryview( data_to_write )

		# Write something to block 4 and this should be read back in a minute
		success = nfc.mifareclassic_write_data_block(4, mv_data);
		if not(success):
			print("Ooops ... unable to WRITE to target block.  Try another key?" )
			time.sleep(1)
			continue

		print( "Block writen... script end!" )
		break

	# Wait a bit before reading the card again
	time.sleep(1)

print( "That's all folks!" )
