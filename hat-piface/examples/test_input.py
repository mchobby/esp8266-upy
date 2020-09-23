""" Hat PiFace under MicroPython - test inputs (read one input @ once)

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/hat-piface
"""

from machine import SPI, Pin
from piface import PiFace
import time

# PYBStick / PYBStick-HAT-FACE
spi = SPI( 1, phase=0, polarity=0 ) # SCLK=S23, MISO=S21, MOSI=S19
cs = Pin( 'S24', Pin.OUT, value=True ) # SPI_CE0=S24, utiliser X5 pour Pyboard

piface = PiFace( spi, cs, device_id=0x00 )

# Read all inputs (one input at once)
try:
	print( "Press CTRL+C to halt script" )
	while True:
		for i in range( 0, 8 ): # 0..7
			if piface.inputs[ i ]:
				print( "Input %s is pressed" % i )
		time.sleep_ms( 300 )
except:
	print( "That s all folks" )
