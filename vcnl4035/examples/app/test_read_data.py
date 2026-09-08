""" Vishay VCNL4035 sensor for MicroPython

    Evaluate the ZX data & display its value!
    ZX data are required for Orb & Gesture calculation

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""

from machine import I2C, Pin
from vcnldefs import VCNL4035_PS_IT, VCNL4035_LED_I
from vcnlapp import VCNL4035Application
import time

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
sensor.zx_enable = False
sensor.zx_smooth = False
sensor.orb_detect = False
sensor.gesture_recognition = False

print( "Start sensing" )
sensor.active_mode()
try:
	while True:
		led.toggle()
		sensor.mainloop()

		# Sensor data reached the minimum thresold (after noise
		# cancelation) to start zx & orb calculation.
		if sensor.is_gesture_activity:
			print( "Reached activity" )
		# Data were fully processed by calc_moving_mean,calc_zx_data,
		#  calc_orb and also gestire recognition
		if sensor.is_data_ready:
			print( "sensor_data = %r" % (sensor.sensor_data) )

except KeyboardInterrupt:
	led.off()

