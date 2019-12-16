""" Continuously attempt to read a key on a 4x4 keypad """
from keypad import Keypad4x4
from time import sleep

k = Keypad4x4()

while True:
	# remove timeout parameter for infinite timeout
	key = k.read_key( timeout=2 )
	print( key )
