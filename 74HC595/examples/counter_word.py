""" 74hc595, Shift Register - driver for MicroPython

	16 bits counter. Use write word to count from 0 to 65535.
	Write word respect the MSBF (higher bit to the left).

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/74hc595
"""

from machine import Pin
from sn74hc595 import ShiftReg
import time


reg = ShiftReg( Pin(20), Pin(21), Pin(19), Pin(18)  )
for w in range( 65536 ): # 0 to 65535
	reg.write_word( w ) # Write a 16bits values with MSBF
# time.sleep(2)
# reg.reset( latch=True ) ## Apply the reset to output
