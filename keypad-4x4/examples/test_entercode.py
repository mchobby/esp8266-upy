""" Read a code on the Keypad Matrix """

from keypad import Keypad4x4
from time import sleep

k = Keypad4x4()
MAGIC_CODE = "444719"

def read_code( timeout=None ):
	global k
	r = ""
	while True:
		key = k.read_key( timeout=timeout )
		if key == None: # If timeout...
			return ""
		elif key == "#": # if enter key
			return r
		else:
			r += key


print( "Enter the code in the Keypad (# : enter)" )
print( "magic is %s" % MAGIC_CODE )
while True:
	# read a cide ib tge Keyboard. Press # for enter key
	code = read_code()
	print( "Keyed-in code is: %s" % code )
	if code == MAGIC_CODE:
		print( "Hurray, you entered the magic code!")
		break

print( "That's all Folks!")
