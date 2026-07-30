""" MicroPython driver for the PCF8523 RTC over I2C.

	Set an arbritary datetime into the PCF8523 RTC

	Dominique Meurisse for MCHobby.be - initial portage
"""
from machine import I2C, Pin
from pcf8523 import PCF8523
import time

DAY_NAMES = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1, sda=Pin(6), scl=Pin(7))
pcf_rtc = PCF8523( i2c )

# Year: 2020, month: 6, day: 22, hour: 0, min: 14, sec: 6, weekday: 0 (monday), yearday: 174
# yearday can be set to 0 when setting the date... it will be recomputed
pcf_rtc.datetime = (2020, 6, 22, 0, 0, 14, 6, 0)
time.sleep(1)

# Reread as datetime
print( "y/m/d weekday h:m:s.ms =>", pcf_rtc.datetime )

# Reread as timestamp
_time = pcf_rtc.timestamp
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % DAY_NAMES[weekday] )
