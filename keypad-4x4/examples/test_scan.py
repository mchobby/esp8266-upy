""" Continuously scan a Keypad Matrix and return the index of pressed key """
from keypad import Keypad
from time import sleep

LINES = ["X5","X6","X7","X8"]
COLS  = ["Y9","Y10","Y11","Y12"]

k = Keypad( lines=LINES, cols=COLS )
while True:
	print( k.scan() )
	sleep( 0.5 )
