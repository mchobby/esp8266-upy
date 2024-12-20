# rp2cnt.py : Raising Edge Pulse Counter  
#
# Source of dhylands
# See https://forum.micropython.org/viewtopic.php?t=9828
import rp2

@rp2.asm_pio()
def pulse_counter():
    label("loop")
    # We wait for a rising edge
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp(x_dec, "loop")  # If x is zero, then we'll wrap back to beginning


class PulseCounter:
    # 32 Bits counter up to 0xffffffff = 4_294_967_295
    # At 24.4 KHz pulse this can make a continuous count for 48h53m43s.

    def __init__(self, sm_id, pin):
        # pin should be a machine.Pin instance
        self.sm = rp2.StateMachine(sm_id, pulse_counter, in_base=pin)
        # Initialize x to zero
        self.sm.put(0)              # Put 32 bit value into Fifo TX
        self.sm.exec("pull()")      # load 32bits from TX Fifo to Output Shift Register
        self.sm.exec("mov(x, osr)") # copy OutputShiftRegister into x
        # Start the StateMachine's running.
        self.sm.active(1)

    def get_pulse_count(self):
        # 32 Bits counter sur up to 0xffffffff = 4294967295
        self.sm.exec("mov(isr, x)") # Copy x into InputShiftRegister 
        self.sm.exec("push()")      # Push isr to FIFO RX (32 bits ) 
        # Since the PIO can only decrement, convert it back into +ve
        return -self.sm.get() & 0x7fffffff
