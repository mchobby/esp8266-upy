""" MOD-RFID1356MIFARE reader test.

    Read the CARD ID (NUID) + EEPROM Block 0 from RFID reader and display it on screen.

	Do not hesitate to activate the debug on RFID_READER to see incoming messages!
	see protocol details on https://www.olimex.com/wiki/MOD-RFID1356MIFARE
"""
from machine import UART
from modrfid import RFID_READER, DEFAULT_AUTH_KEY
from time import sleep

uart = UART( 1, baudrate=38400, timeout=500 )
rfid = RFID_READER( uart, debug=False)

# Set MiFare A KEY for reading (used the FFFFFFFFFFFF default one for new cards)
# Change is only allowed if the Key in not yet initialized to FFFFFFFFFFFF
key_a = rfid.get_key( 'a' )
print( 'Key A = %s' % key_a )

# Code below is not reliable AT ALL and cause ERR: if not in debug mode
# Key A have been fixed by using the USB-CDC support.
#if key_a != '112233445566':
#	print( 'Change the key A...')
#	rfid.set_key( 'a', '112233445566' )

# Which if the current working key
current_key, current_key_value = rfid.get_work_key()
print( "Current working Key is %s with key=%s" % (current_key, current_key_value) )
if current_key != 'a':
	print('Set current work key to a')
	rfid.set_work_key( 'a' )

key_b = rfid.get_key( 'b' )
print( 'Key B = %s' % key_b )

# We want to read EEPROM block 0 (manufacturer block) together with the CARD ID
# Can have up to 64 block
rfid.read_blocks( 0 )
# read EEPROM blocks 0 to 7 (not working on Firmware 2.1.8)
# rfid.read_blocks( 0,7 )

# activate eeprom block reading
rfid.eeprom_read( True )

# Set scan interval to 2 secondes
rfid.set_scan_interval( 2000 )

# Turn off LEDs
rfid.set_led_mode( enabled=False )

print("Please scan RFID card")
while True:
	try:
		rfid.update()

		if rfid.has_card:
			print( "Card detected: %s" % rfid.card_id )

		if rfid.has_blocks:
			print( 'EEPROM blocks')
			# rfid.blocks is a dictionnary
			for block_nr, block_data in rfid.blocks.items():
				print( "  blocks % s : %s" % (block_nr, block_data) )

		if rfid.has_card:
			# Something has been read so now...
			# Clear the captured data
			rfid.clear()
	except Exception as err:
		print( '[ERROR] %s' % err )
		print( '[ERROR] LastError = %s' % rfid.last_error )
