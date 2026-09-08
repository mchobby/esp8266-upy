# Applicative examples of the VCNL4035

Advanced examples based on Vishay VCNL4035 Application Notes.

Application examples __use interrupt request__ mechanism. So __int pin must be connected__ to the MCU!

Here are the the recommanded order for testing and reading the the app scripts.

1. [test_gesture_noise.py](test_gesture_noise.py) : Evaluate the gesture noise & display it!
2. [test_gesture_timeout.py](test_gesture_timeout.py) : Use a timer to place sensor in Power Safe mode when no gesture is detected!
3. [test_read_data.py](test_read_data.py) : wait for a minimal gesture thresold to be reached before displaying the data.
4. [test_read_zx_data.py](test_read_zx_data.py) : Evaluate the ZX data & display its value!
5. [test_read_orb_data.py](test_read_orb_data.py) :  Evaluate the ZX data + Orb calcultation display its value! Such data are required for Gesture calculation
6. [test_read_gesture.py](test_read_gesture.py) : After ZX data + Orb, lets try to evaluate Gesture detection (PUSH, SWIPE_LEFT, SWIPE_RIGHT)
