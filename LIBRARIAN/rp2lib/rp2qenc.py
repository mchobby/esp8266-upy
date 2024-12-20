# Quadrature encoder for RPi 2040 Pio
# Has to be at address 0 of PIO programm space
#
# Source of rkompass
# See https://forum.micropython.org/viewtopic.php?t=12277
#
# Original version (c) 2021 pmarques-dev @ github
# (https://github.com/raspberrypi/pico-examples/blob/master/pio/quadrature_encoder/quadrature_encoder.pio)
# Adapted and modified for micropython 2022 by rkompass
#
# SPDX-License-Identifier: BSD-3-Clause
#
# This program was reduced to take 'only' 24 of 32 available PIO instructions. 
# 
# Quadrature encoding uses a state table in form of a jump table
#   which is fast and has no interrupts.
# The counter x is permanently pushed nonblockingly to the FIFO.
# To read the actual value empty the FIFO then wait for and get the next pushed value.

# The worst case sampling loop takes 14 cycles, so this program is able to read step
#   rates up to sysclk / 14  (e.g., sysclk 125MHz, max step rate = 8.9 Msteps/sec).
#
from rp2 import PIO, StateMachine, asm_pio

class PIO_QENC:
    def __init__(self, sm_id, pins, freq=10_000_000):
        if not isinstance(pins, (tuple, list)) or len(pins) != 2:
            raise ValueError('2 successive pins required')
        #pinA = int(str(pins[0]).split(')')[0].split('(')[1].split(',')[0])
        pinA = int( str(pins[0]).split(',')[0].split('GPIO')[1] )
        # pinB = int(str(pins[1]).split(')')[0].split('(')[1].split(',')[0])
        pinB = int( str(pins[1]).split(',')[0].split('GPIO')[1] )
        if abs(pinA-pinB) != 1:
            raise ValueError('2 successive pins required')
        in_base = pins[0] if pinA < pinB else pins[1]
        self.sm_qenc = StateMachine(sm_id, self.sm_qenc, freq=freq, in_base=in_base, out_base=in_base)
        self.sm_qenc.exec("set(x, 1)")  # we once decrement at the start
        self.sm_qenc.exec("in_(pins, 2)")
        self.sm_qenc.active(1)
    
    @asm_pio(in_shiftdir=PIO.SHIFT_LEFT, out_shiftdir=PIO.SHIFT_RIGHT)
    def sm_qenc():
        label("decr")
        jmp(x_dec, "read") # 110 : B from 1 to 0, A = 1  => backward
        # ---------------
        label("read")      # 111 : B from 0 to 0         => no change
        mov(osr, isr)      # save last pin input in OSR
        mov(isr, x)
        push(noblock)
        out(isr, 1)        # right bit B' of OSR into ISR, all other 0; needs out_shiftdir=PIO.SHIFT_RIGHT
        in_(pins, 2)       # combined with current reading A B of input pins
        # ---------------
        mov(y, isr)         # use y to perform different jumps
        jmp(y_dec, "next1")
        label("next1")
        jmp(not_y, "decr")  # isr = 001 : B from 0 to 1, A = 0  => backward
        jmp(y_dec, "next2")
        label("next2")
        jmp(y_dec, "next3")
        label("next3")
        jmp(not_y, "incr")  # isr = 011 : B from 0 to 1, A = 1  => forward
        jmp(y_dec, "next4")
        label("next4")
        jmp(not_y, "incr")  # isr = 100 : B from 1 to 0, A = 0  => forward
        jmp(y_dec, "next5")
        label("next5")
        jmp(y_dec, "next6")
        label("next6")
        jmp(not_y, "decr")  # isr = 110 : B from 1 to 0, A = 1  => backward
        jmp("read")
        # ---------------
        label("incr")      # increment x by inverting, decrementing and inverting
        mov(x, invert(x))
        jmp(x_dec, "here")
        label("here")
        mov(x, invert(x))  # we rely on implicit .wrap with micropython
        jmp("read")

    def read(self):
        for _ in range(self.sm_qenc.rx_fifo()):
            self.sm_qenc.get()
        n = self.sm_qenc.get()
        return n if n < (1<<31) else n - (1<<32)



