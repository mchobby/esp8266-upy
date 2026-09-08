""" Vishay VCNL4035 sensor for MicroPython

    Evaluate the gesture noise & display its value!

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""

from machine import I2C, Pin
from vcnldefs import VCNL4035_PS_IT
from vcnlapp import VCNL4035Application
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
# configured as Gesture and attached to an interrupt Pin
sensor = VCNL4035Application( i2c=i2c, int_pin=Pin(0) )
sensor.set_ps_integration_time( VCNL4035_PS_IT.PS_IT_400us )

sensor.calc_gesture_noise( 100 ) # 100 iterations

print( "Gesture Noise LDR1, LDR2, LDR3", sensor.gesture_noise ) 
