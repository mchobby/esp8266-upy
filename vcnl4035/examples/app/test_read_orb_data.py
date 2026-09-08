""" Vishay VCNL4035 sensor for MicroPython

    Evaluate the ZX data + Orb calcultation display its value!
    ZX data are required for Orb & Gesture calculation

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""

from machine import I2C, Pin
from vcnldefs import VCNL4035_PS_IT, VCNL4035_LED_I
from vcnlapp import VCNL4035Application, ZX_DEBUG, NOISE_DEBUG
import time

# set vcnl_app.py NOISE_DEBUG=True for more detail on noise calculation
# set vcnl_app.py ZX_DEBUG   =True for more detail on zx & orb calculation


led = Pin( 25, Pin.OUT, value=False )
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
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
sensor.gesture_recognition = False

print( "gesture_activity_thresold :", sensor.gesture_activity_threshold )
print( "zx_min_thresold :", sensor.zx_min_threshold )

print( "Start sensing..." )
time.sleep(2)
print( "\033[2J" ) # Clear Terminal (but doesn't move the cursor)
sensor.active_mode()
try:
	while True:
		led.toggle()
		sensor.mainloop()

		if sensor.is_zx_data_ready:
			z,x = sensor.zx_data()
			print( "z,x = %s, %s     " % (z,x) )
except KeyboardInterrupt:
	led.off()

