""" MOD-RFID1356MIFARE reader test.

    Read the CARD ID (NUID) from RFID reader and display it on screen.

	Do not hesitate to activate the debug on RFID_READER to see incoming messages!
	see protocol details on https://www.olimex.com/wiki/MOD-RFID1356MIFARE
"""
from machine import UART
from modrfid import RFID_READER

uart = UART( 1, baudrate=38400, timeout=500 )
rfid = RFID_READER( uart, debug=False)
rfid.eeprom_read( False ) # Do not read EEPROM data

# Display MOD-RFID1536MIFARE firmware version to Output
lines = rfid.reader_info()
for line in lines:
	print( line )

print("Please scan RFID cards")
while True:
	rfid.update()
	if rfid.has_card:
		print( "Card detected: %s" % rfid.card_id )
		# Cleat the card data
		rfid.clear()
