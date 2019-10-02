import micropython
micropython.alloc_emergency_exception_buf(100)

from machine import I2C
from mcp4725 import MCP4725
from pyb import Timer
from time import sleep

# Samples to draw the camel waveform to emit
BUFFER = [0,0,1,2,3,5,8,12,18,26,37,53,73,101,138,185,245,321,414,527,663,822,
          1007,1217,1452,1708,1983,2272,2567,2860,3143,3405,3636,3826,3966,4048,
		  4067,4020,3908,3734,3506,3232,2925,2601,2275,1963,1683,1448,1270,1160,
		  1122,1160,1270,1448,1683,1963,2275,2601,2925,3232,3506,3734,3908,4020,
		  4067,4048,3966,3826,3636,3405,3143,2860,2567,2272,1983,1708,1452,1217,
		  1007,822,663,527,414,321,245,185,138,101,73,53,37,26,18,12,8,5,3,2,1,0]
LEN = len( BUFFER )

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

mcp = MCP4725( i2c = i2c )
mcp.value = 0

_sample_index = 0
def set_sample( timer ):
	""" Just keep track of the next sample index to send.
	    Made it as short as possible. """
	global _sample_index, LEN
	if _sample_index+1 >= LEN:
		_sample_index = 0
	else:
		_sample_index += 1

# Create a timer @ 50_hertz*100_samples = 5000 50_hertz
tim = Timer(6, freq=5000 )
tim.callback( set_sample )

# Main loop emitting the samples as fast as possible
print( "Emitting the Camel wafeform")
_last_emitted = None
try:
	while True:
		# Duplicate the value because continuously update
		_next_to_emit = _sample_index
		# If it was different of last emitted data
		if _next_to_emit != _last_emitted:
			# Go for emit!!!! Using Raw Value emitting (0-4095)
			# for better performance.
			mcp.raw_value = BUFFER[_next_to_emit]
			# Remeber it to not send it twice!
			_last_emitted = _next_to_emit
except:
	# deactivate the timer
	tim.callback( None )

print( "That's all folks")
