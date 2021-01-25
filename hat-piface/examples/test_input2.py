""" Hat PiFace under MicroPython - test inputs (read all inputs @ once)

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/hat-piface
"""

from machine import SPI, Pin
from piface import PiFace
import time

# PYBStick / PYBStick-HAT-FACE
spi = SPI( 1, phase=0, polarity=0 ) # SCLK=S23, MISO=S21, MOSI=S19
cs = Pin( 'S24', Pin.OUT, value=True ) # SPI_CE0=S24, use X5 for Pyboard
# Raspberry-pico
# spi = SPI( 0, phase=0, polarity=0 )
# cs = Pin( 5, Pin.OUT, value=True )

piface = PiFace( spi, cs, device_id=0x00 )

# read all input in one operation
try:
	# Prepare Input names list
	pin_names =  ['IN%i' % pin for pin in range(8) ]
	print( "Press CTRL+C to halt script" )
	while True:
		values = piface.inputs.all # Get all input @ once
		datas = zip(pin_names,values) # Combine the two list [ (pin_name0,value0), (pin_name1,value1), ... ]
		print( ", ".join( ["%s:%s" % (name_value[0],name_value[1]) for name_value in datas] ))
		time.sleep(0.5)
except:
	print( "That s all folks" )
