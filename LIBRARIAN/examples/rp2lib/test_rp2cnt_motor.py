# Example using PIO to count pulses on an input pin.
# With pulse generated by a optical encoder (just one of the reader)
#
from machine import Pin
from rp2cnt import PulseCounter
import time

pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
pc = PulseCounter(0, pin16)

start = time.ticks_ms()
while True:
	ms = time.ticks_diff( time.ticks_ms(), start )
	print( "%8i ms ==> Pulses: %5i" % (ms,pc.get_pulse_count())  )
	time.sleep_ms( 100 )
