""" 74hc595, Shift Register - driver for MicroPython

	Write a 16 bits values on a dual daisy chained 74hc595.
	Write word respect the MSBF (higher bit to the left).

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
reg.write_word( 0xFDCA ) # Write a 16bits values with MSBF
# time.sleep(2)
# reg.reset( latch=True ) ## Apply the reset to output
