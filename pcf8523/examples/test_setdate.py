""" MicroPython driver for the PCF8523 RTC over I2C.

	Set the RTC time to a fixed date

	Dominique Meurisse for MCHobby.be - initial portage

"""

from machine import I2C
from pcf8523 import PCF8523
import time

# PYBStick - S3=sda, S5scl
i2c = I2C(1)

rtc = PCF8523( i2c )

# Year: 2020, month: 6, day: 22, hour: 0, min: 14, sec: 6, weekday: 0 (sunday), yearday: 174
rtc.datetime = (2020, 6, 22, 0, 14, 6, 0, 174)
time.sleep(1)

# Reread time from RTC
_time = rtc.datetime
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )

days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % days[weekday] )
