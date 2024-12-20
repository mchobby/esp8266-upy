# Example using PIO to count pulses on an input pin.
#
# The following assumes Pin 17 is jumper to Pin 16
#

from machine import Pin
from rp2cnt import PulseCounter

pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
pin17 = Pin(17, Pin.OUT)
pin17.low()


pc = PulseCounter(0, pin16)
print("pulse count =", pc.get_pulse_count())

pin17.high()
pin17.low()

print("pulse count =", pc.get_pulse_count())

pin17.high()
pin17.low()

print("pulse count =", pc.get_pulse_count())
