""" Vishay VCNL4035 sensor for MicroPython

    After ZX data + Orb, lets try to evaluate Gesture detection

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""

from machine import I2C, Pin
from vcnldefs import VCNL4035_PS_IT, VCNL4035_LED_I
from vcnlapp import *
import time

# Following constant can be updated in vcnlapp.py 
# This will shows additional debug messages
#  * GESTURE_DEBUG      : to show calculation result
#  * GESTURE_DATA_DEBUG : to show the captured ZX_Data

act_led = Pin( 25, Pin.OUT, value=False ) # Activity LED 
acq_led = Pin( 15, Pin.OUT, value=False ) # Acquisition LED
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )

def data_collect_cb( sensor ):
	act_led.toggle()

def start_collect_cb( sensor ):
	acq_led.on()

def reset_collect_cb( sensor ):
	acq_led.off()


GESTURE_LABELS = {GESTURE_NONE:'None', GESTURE_PUSH:'PUSH', GESTURE_SWIPE_LEFT:'SWIPE LEFT', GESTURE_SWIPE_RIGHT:'SWIPE_RIGHT'}

# configured as Gesture and attached to an interrupt Pin
sensor = VCNL4035Application( i2c=i2c, int_pin=Pin(0) )
sensor.set_ps_integration_time( VCNL4035_PS_IT.PS_IT_400us )
sensor.set_led_current( VCNL4035_LED_I.LED_I_100mA )
print( "Evaluate Noise" )
sensor.calc_gesture_noise( 100 ) # 100 iterations
print( "Noise", sensor.gesture_noise )

# Changes parameter to limit evaluation
sensor.gesture_noise_substract = True
sensor.zx_enable = True
sensor.zx_smooth = False
sensor.orb_detect = True
sensor.gesture_flags.orb_data_cnt_limit = 12 # 12 to 15 events to get gesture detection
sensor.gesture_recognition = True
# Attach callback
sensor.on_data_collect = data_collect_cb
sensor.on_start_collect = start_collect_cb
sensor.on_reset_collect = reset_collect_cb

print( "gesture_activity_thresold :", sensor.gesture_activity_threshold )
print( "zx_min_thresold :", sensor.zx_min_threshold )

print( "Start sensing..." )
time.sleep(2)
sensor.active_mode()
try:
	while True:		
		sensor.mainloop()

		if sensor.is_gesture_recognition_data_ready:
			print( "%s detected" % GESTURE_LABELS[sensor.gesture.recognized] )
		
except KeyboardInterrupt:
	act_led.off()
	acq_led.off()

