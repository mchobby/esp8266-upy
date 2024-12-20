
# Example using PIO to check signals of Quadrature Encoder (rotary button or motor encoder)
# 
# This example uses a Optical Quadrature Encoder for a rotating disk attached to a motor
#
from machine import Pin
from time import sleep_ms
from rp2qenc import PIO_QENC

pinA = Pin(15, Pin.IN, Pin.PULL_UP)
pinB = Pin(16, Pin.IN, Pin.PULL_UP)

qenc = PIO_QENC(0, (pinA, pinB))
print('starting....')
for i in range(120):
    print('iter %3i : Quadrature value = %i' % (i,qenc.read()) )
    sleep_ms(500)
qenc.sm_qenc.active(0)
print('stop')