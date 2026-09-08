""" Vishay VCNL4035 sensor for MicroPython

    Modify the integration time and the IR Led current (IRED2 & IRED3) to check
    the impact on readings. Script displays the current configuration
    and make a reading every 0.5sec before changing the value.

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_PS_IT, VCNL4035_LED_I
import time, micropython

# === Sensor ===
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.GESTURE )

#  Trigger Gesture Data capture
sensor.set_ps_trigger()

# Integration and Current to test
integrations = [ (VCNL4035_PS_IT.PS_IT_125us, "125us"), (VCNL4035_PS_IT.PS_IT_400us, "400us") ]
currents = [ (VCNL4035_LED_I.LED_I_75mA, "75mA"),(VCNL4035_LED_I.LED_I_140mA, "140mA"),(VCNL4035_LED_I.LED_I_200mA, "200mA") ] 

# === Main Loop ===
print( "VCLN4035 version", sensor.version )
print( "Integration Time, IRED2 & IRED3 LED current" )
for int_time, int_str in integrations:
	for current, current_str in currents:
		sensor.set_ps_integration_time( int_time )
		sensor.set_led_current( current )
		print("--- %s, %s -------------------------------" % (int_str,current_str) )

		reads = 20 # 20 reads = 10 seconds
		while reads > 0:
			data = sensor.read_data()
			sensor.set_ps_trigger() # reset trigger
			print( "%.2fsec : %r" % (reads/2, data) )
			reads -= 1
			time.sleep_ms(500)



