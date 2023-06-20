""" Send a byte to a 74HC595 serial to parallel Shift register

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/74hc595
"""

from sn74hc595 import ShiftReg
from machine import Pin
import time

# Data pin, Click pin, Latch pin, Reset pin
reg = ShiftReg( Pin(20), Pin(21), Pin(19), Pin(18)  )
reg.write_byte( 255 ) # Set all output on
time.sleep(1)
reg.write_byte( 0 )  # Set all output off
time.sleep(1)
reg.write_byte( 0b10101010 )
time.sleep(1)
reg.write_byte( 0b01010101 )
time.sleep(1)
reg.write_byte( 0b00001110 )
time.sleep(1)
reg.write_byte( 255 ) # Set all output on
time.sleep(1)
reg.reset( latch=True ) # Reset internal buffer + Apply to the output
