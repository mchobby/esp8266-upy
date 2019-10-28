from machine import Pin, SPI
from time import sleep

from ad9833 import *
# SPI must be initialized on mode 2 -> Polarity=1, Phase=0
# Y8 = MOSI --> DAT
# Y6 = SCK  --> CLK
# Y5 = /SS  --> FUNC

# Note (EuropeanName,ImperialCode,Frequency)
NOTES = [('DO' ,'C',264),('RE','D',297),('MI','E',330),('FA','F',352),
		 ('SOL','G',396),('LA','A',440),('SI','B',495),('DO','C',528) ]

# Phase and polarity ARE REQUIRED required for SPI bus in mode 2!
# Do not hesitate to slow down the SPI bus @ baudrate=9600
spi = SPI(2,  baudrate=9600, polarity=1, phase=0)
ssel = Pin( "Y5", Pin.OUT, value=1) # use /ss

# mclk is the source clock on the AD9833 board
gen = AD9833( spi, ssel) # default clock at 25 MhZ

def play_note( freq ):
	global gen
	gen.select_register(0)
	gen.mode  = MODE_SINE
	gen.freq  = freq
	gen.phase = 0 # No phase shift (0..4095)

for name, name2, freq in NOTES:
	# Suspend Output
	gen.reset = True
	sleep( 1 )

	print( "Play %s @ %s Hz" % (name,freq) )
	play_note( freq )

	# Activate output on Freq0
	gen.reset = False

	sleep( 2 )

gen.reset = True
print( "That's all folks!")
