""" Vishay VCNL4035 sensor for MicroPython

    check the max interrupt freq achieved for a gesture reading.
    MODIFIED VERSION of test_interrupt_gesture.py WITHOUT prints.
    HOOKUP oscilloscope on "int" pin and read signal frequency.

    The "int" pin is connected to GPIO 0 (on RPI Pico)

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Results:
   Raspberry Pico 1: IRQ period=~3.7ms, IRQ freq=~270 Hz

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_PS_IT
import time, micropython

micropython.alloc_emergency_exception_buf(100)

int_count=0 # allow main loop to detect IRQ arrival

# === Attach an ISR to the GP0 ===
def vcnl_int( pin ):
	global int_count
	int_count += 1
	# Uncomment the following to check when interrupt is raised
	# print( "int ISR called" )

int_pin = Pin( 0, Pin.IN, Pin.PULL_UP )
int_pin.irq( vcnl_int, trigger=Pin.IRQ_FALLING ) # Add  hard=True for quicker reaction

# === Sensor ===
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.GESTURE )
# Default integration time, the value can reach 1_500 to 2_500. This should be enough
# Higher integration time, the value can reach and exceed 32_000.
#
sensor.set_ps_integration_time( VCNL4035_PS_IT.PS_IT_400us )
sensor.read_int_flags() # reset interrupt flags
time.sleep_ms(10)
#  Trigger Gesture Data capture
sensor.set_ps_trigger()


# === Main Loop ===
print( "VCLN4035 version", sensor.version )
print( "capture started. Hookup the oscilloscope probe on INT pin!" )

last_int_count = int_count
sensor.read_int_flags() # reset last potential interrupt
while True:
	# Interrupt detected
	if int_count!=last_int_count:
		data = sensor.read_data() # return 3 values from gesture sensor
		# Nothing displayed (spare processing time)

		# Read interrupt flag on VCNL (Sets VCNL INT pin back to high)
		last_int_count = int_count
		sensor.read_int_flags()
		# Reset gesture trigger
		sensor.set_ps_trigger()


