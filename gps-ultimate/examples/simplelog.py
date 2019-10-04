# Simple GPS datalogging demonstration.
# This actually doesn't even use the GPS library and instead just reads raw
# NMEA sentences from the GPS unit and dumps them to a file on an SD card
# (recommended) or internal storage (be careful as only a few kilobytes to
# megabytes are available).  Before writing to internal storage you MUST
# carefully follow the steps in this guide to enable writes to the internal
# filesystem:
import machine

# Path to the file to log GPS data.  By default this will be appended to
# which means new lines are added at the end and all old data is kept.
# Change this path to point at internal storage (like '/flash/gps.txt') or SD
# card mounted storage ('/sd/gps.txt') as desired.
LOG_FILE = '/sd/gps.txt'      # Example for writing to SD card path /sd/gps.txt
#LOG_FILE = '/flash/gps.txt'  # Example for writing to internal path /flash/gps.txt
#LOG_FILE = 'gps.txt'  # Example for writing to current directory (maybe Flash or SD depending on boot device)


# File more for opening the log file.  Mode 'ab' means append or add new lines
# to the end of the file rather than erasing it and starting over.  If you'd
# like to erase the file and start clean each time use the value 'wb' instead.
LOG_MODE = 'ab'

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
print( 'open uart to gps module')
uart = machine.UART(1, baudrate=9600, timeout=3000) # TX=X9, RX=X10

# Main loop just reads data from the GPS module and writes it back out to
# the output file while also printing to serial output.
print( 'opening file %s' % LOG_FILE )
with open(LOG_FILE, LOG_MODE) as outfile:
    print("Start logging")
    while True:
        sentence = uart.readline()
        print( sentence )
        outfile.write(sentence)
        outfile.flush()
    print("End of logging")
