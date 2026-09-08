""" Vishay VCNL4035 sensor for MicroPython

    Use a timer to place sensor in Power Safe mode
    when no gesture is detected!

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Requires TimeoutTimer classe
   mpremote mip install github:mchobby/esp8266-upy/LIBRARIAN

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnldefs import VCNL4035_PS_IT, VCNL4035_MODES
from vcnlapp import VCNL4035Application
from timetls import TimeoutTimer
import time

TIME_LIMIT_SEC = 5.0

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
# configured as Gesture and attached to an interrupt Pin
sensor = VCNL4035Application( i2c=i2c, int_pin=Pin(0) )
# VCNL Settings Public Variable Settings
sensor.gesture_mode.ps_conf_1.ps_it = VCNL4035_PS_IT.PS_IT_400us
sensor.ps_mode.ps_conf_1.ps_it = VCNL4035_PS_IT.PS_IT_400us
sensor.ps_mode.ps_thdl = 50
sensor.ps_mode.ps_thdh = 300
# VCNL Settings
sensor.gesture_active_threshold = 500
sensor.gesture_noise_subtract = True 
sensor.init( VCNL4035_MODES.GESTURE ) # send config to sensor
# Evaluate noise floor
sensor.calc_gesture_noise(10)

# Reset SW Timmer
power_save_timer = TimeoutTimer()
power_save_timer.set( TIME_LIMIT_SEC ) # start the timer !

print( "Initialized" )

# MainLoop
while True:
	if sensor.is_gesture_activity:
		# Reset timer
		power_save_timer.set( TIME_LIMIT_SEC ) 
	elif power_save_timer.expired:
		print( "Sleep mode" )
		sensor.sleep_mode()

	sensor.mainloop()

	if sensor.is_data_ready:
		data = sensor.read_data()
		print( "Gesture data:", data )
