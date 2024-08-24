__version__ = '0.0.2'

import os

# Based on dylands code @ https://forum.micropython.org/viewtopic.php?t=8112
def dir_exists(filename):
	try:
		return (os.stat(filename)[0] & 0x4000) != 0
	except OSError:
		return False

def file_exists(filename):
	try:
		return (os.stat(filename)[0] & 0x4000) == 0
	except OSError:
		return False

def file_size( filename ):
	try:
		return os.stat(filename)[6]
	except OSError:
		return -1
