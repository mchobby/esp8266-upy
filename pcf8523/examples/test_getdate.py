""" MicroPython driver for the PCF8523 RTC over I2C.

	Read the time from the RTC

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

_dt = pcf_rtc.datetime
print( "y/m/d weekday h:m:s.ms =>", _dt )
print( "Day of Week:", DAY_NAMES[_dt[3]])

_time = pcf_rtc.timestamp
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % DAY_NAMES[weekday] )
