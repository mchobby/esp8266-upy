
# test.py - tare the sensor then use the get_units() combined with set_scale() to return the reading in an appropriate unit. 
#           The scale is calculated based on the gauge scale (eg: 5000 gr or 10 Kg gauge) and gauge calibration.
# 
#
# more details on following URL for calibration process:  https://github.com/mchobby/esp8266-upy/tree/master/hx711 
#
from hx711_gpio import HX711
from machine import Pin
import time

pin_OUT = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(13, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT, gain=128)

hx711.tare()
hx711.set_scale( 404.4715 ) # 5000gr Gauge with 128 bit gain. Output unit will be in grams
while True:
	print( "get_units: %s gr" % hx711.get_units() )
	time.sleep_ms( 500 )
