""" 74hc595, Shift Register - driver for MicroPython

	Write multiple bytes on daisy chained

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/74hc595
"""

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy"

from machine import Pin
from sn74hc595 import ShiftReg
import time


reg = ShiftReg( Pin(20), Pin(21), Pin(19), Pin(18)  )
reg.write_bytes( [255,0] ) # Low Byte first (all ON), High byte next (all OFF)
time.sleep(1)
reg.write_bytes( [0, 255] ) # Low Byte first (all OFF), High byte next (all ON)
time.sleep(1)
reg.write_bytes( [0b10101010, 0b01010101] ) # Lower Byte First (Little Endian)
# time.sleep(2)
# reg.reset( latch=True ) ## Apply the reset to output
