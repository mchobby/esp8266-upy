""" Call it from mshell as a demo script.

    This file will toggle the GP25 LED state on a Raspberry-Pi Pico at each
	call
"""

print( "gp25 starting")
from machine import Pin
Pin(25).toggle()
print( "gp25 exciting")
