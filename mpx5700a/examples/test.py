"""  test.py - test the mpx5700a analog pressure sensor

	for Grove - Integrated Pressure Sensor Kit (SeeedStudio 110020248)
	https://wiki.seeedstudio.com/Grove-Integrated-Pressure-Sensor-Kit/

Documentation:
   https://github.com/mchobby/esp8266-upy/tree/master/mpx5700ap

Author(s): Meurisse D., MCHobby (shop.mchobby.be).
------------------------------------------------------------------------
History:
  17 january 2022 - Dominique - Add example code
"""

from machine import Pin, ADC
import time

adc = ADC(Pin(26)) # ADC0 on GP26

while True:
	raw = adc.read_u16() # 0..65535 for 0v..3.3v
	v = 3.3*raw/65535 # Transform in voltage
	kpa = (((v*1023)/5)-41)*700/(963-41)
	print( 'V: %8.6f, kPa: %s' % (v, kpa) )
	time.sleep(0.100)
