""" Hat PiFace under MicroPython - test outputs

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/hat-piface
"""

from machine import SPI, Pin
from piface import PiFace
import time

# PYBStick / PYBStick-HAT-FACE
spi = SPI( 1, phase=0, polarity=0, baudrate=400000 ) # SCLK=S23, MISO=S21, MOSI=S19
cs = Pin( 'S24', Pin.OUT, value=True ) # SPI_CE0=S24
# Raspberry-pico
# spi = SPI( 0, phase=0, polarity=0 )
# cs = Pin( 5, Pin.OUT, value=True )

piface = PiFace( spi, cs, device_id=0x00 )

# Make a chase on outputs
try:
	print( "Press CTRL+C to halt script" )
	while True:
		for i in range( 8 ): # 0..7
			piface.outputs[i] = True
			time.sleep_ms( 300 )
			piface.outputs[i] = False
except:
	piface.reset() # Reset all outputs
