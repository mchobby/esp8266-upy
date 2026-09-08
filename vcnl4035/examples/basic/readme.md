# Basic examples for the VCNL4035

Here are the the recommanded order for testing and reading the scripts.

1. [test_sensitivity.py](test_sensitivity.py) : Evaluate combination of integration time and LED poser on the count readings! See [test_sensitivity.result](test_sensitivity.result) for output.
2. [test_proximity2.py](test_proximity2.py) : read the value of IRED1 (top LED) every 250ms. Will return a value from 0 to 65535

## Interrupt based examples

Advanced application requires interrupt handling, so the following example do!

The "int" pin must be is connected to GPIO 0

1. [test_interrupt.py](test_interrupt.py) : implement interrupt handler within user script.
2. [test_interrupt_gesture.py](test_interrupt_gesture.py) : Display IRED1, IRED2, IRED3 values, implement interrupt handler within user script.
3. [test_interrupt_gesture2.py](test_interrupt_gesture2.py) : Same as previous but __INTERRUPT HANDLER MANAGED WITHIN THE LIBRARY!__.
4. [test_gesture_freq.py](test_gesture_freq.py) :  Use an oscilloscope to evaluate the max acquisition speed (about 3.7ms per reading).


