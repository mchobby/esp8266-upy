""" MicroPython driver for the PCF8523 RTC over I2C.

	Read the time from the RTC

	Dominique Meurisse for MCHobby.be - initial portage

"""

from machine import I2C
from pcf8523 import PCF8523
import time

# PYBStick - S3=sda, S5scl
i2c = I2C(1)

rtc = PCF8523( i2c )

_time = rtc.datetime
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )

days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % days[weekday] )
