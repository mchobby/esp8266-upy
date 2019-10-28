from machine import Pin, SPI

from ad9833 import *
# SPI must be initialized on mode 2 -> Polarity=1, Phase=0
# Y8 = MOSI --> DAT
# Y6 = SCK  --> CLK
# Y5 = /SS  --> FUNC

# Phase and polarity ARE REQUIRED required for SPI bus in mode 2!
# Do not hesitate to slow down the SPI bus @ baudrate=9600
spi = SPI(2,  baudrate=4800, polarity=1, phase=0)
ssel = Pin( "Y5", Pin.OUT, value=1) # use /ss

# mclk is the source clock on the AD9833 board
gen = AD9833( spi, ssel) # default clock at 25 MhZ

# Initialise the AD9833 with 1.3KHz sine output, no phase shift for both
# registers and remain on the FREQ0 register
frequency0 = 1300 #  1.3 Khz
frequency1 = 50 #  50 Hz
phase      = 0 # No phase shift (0..4095)

# Suspend Output
gen.reset = True

# Configure Freq0
gen.select_register(0)
gen.mode = MODE_SINE
gen.freq = frequency0
gen.phase = phase

# Configure Freq1
gen.select_register(1)
gen.freq = frequency1
gen.phase = phase


# Activate output on Freq0
gen.select_register(0)
gen.reset = False

# Sinewave @ 1.3 KHz should be visible on the output
# Typical output should have 0.6 Vpp
