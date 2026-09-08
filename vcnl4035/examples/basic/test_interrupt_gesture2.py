""" Vishay VCNL4035 sensor for MicroPython

    Test gesture reading WITH INTERRUPT setup
    Connect the "int" pin to GPIO 0 (on RPI Pico)

	*** THIS CODE HANDLE THE INTERRUPT FROM LIBRARY ***

    This example wait for gesture triggering the interrupt then reads and
    displays the IRED1, IRED2 & IRED3 data.

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_PS_IT
import time, micropython

micropython.alloc_emergency_exception_buf(100)

# === Sensor ===
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.GESTURE )
sensor.set_int_pin( Pin(0) )
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

sensor.read_int_flags() # reset last potential interrupt
while True:
	data = sensor.wait_data() # return 3 values from gesture sensor
	# Data[0] is the IRED1 led (the top one) in range 0..65535
	print( "----------------------" )
	print( "IRED1", data[0] )
	print( "IRED2", data[1] )
	print( "IRED3", data[2] )
	# Read interrupt flag on VCNL (Sets VCNL INT pin back to high)
	sensor.read_int_flags()
	# Reset gesture trigger
	sensor.set_ps_trigger()


