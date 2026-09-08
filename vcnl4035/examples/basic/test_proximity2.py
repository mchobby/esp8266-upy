""" Vishay VCNL4035 sensor for MicroPython

    Test the proximity reading
    Use wide integration time to largest possible (8T)

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_PS_IT
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.PROXIMITY )
# With default integration time, the value can reach 1_500 to 2_500.
# With Higher integration time, the value can reach and exceed 32_000.
sensor.set_ps_integration_time( VCNL4035_PS_IT.PS_IT_400us )
print( "VCLN4035 version", sensor.version )
while True:
	data = sensor.read_data() # return 3 values from gesture sensor
	# Data[0] is the IRED1 led (the top one) in range 0..65535
	print( data[0] )
	time.sleep_ms(250)
