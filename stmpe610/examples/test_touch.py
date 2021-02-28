# Project home: https://github.com/mchobby/esp8266-upy/tree/master/stmpe610
#
# This example will reads the version form stmpe610 chip
#
from machine import SPI,Pin
from stmpe610 import *
import time

# PYBStick config (idem with PYBStick-Feather-Face)
# spi = SPI( 1, baudrate=10000000 )
# cs_pin = Pin("S15")
# dc_pin = Pin("S13")
# rst_pin = None

# Raspberry-Pi Pico
#   Note: the mode 0 (phase=0,polarity=0) does not returns proper version value
spi = SPI( 0, baudrate=1000000,  phase=1, polarity=0 ) # Mode 1
cs_pin = Pin(2) # GP2

stmp = STMPE610( spi, cs_pin )
# Value 0x811 espected
print( "Version: 0x%x" % stmp.version )
while True:
	if stmp.touched:
		pt = stmp.point
		if pt:
			print('Touched (x,y,z) @ (%i, %i, %i)' % pt )
		else:
			print('Touched (without point data)' )
	time.sleep_ms( 100 )
