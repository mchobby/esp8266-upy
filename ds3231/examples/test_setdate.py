""" DS3231 RTC driver - Init DS3231 time with a fixe datetime value

"""

from machine import I2C
from ds3231 import DS3231
import time

# PYBStick: sda=S3, scl=S5
i2c = I2C(1)

ds = DS3231( i2c )
# Year: 2020, month: 6, day: 22, hour: 0, min: 14, sec: 6, weekday: 0 (monday), yearday: 174
ds.datetime( (2020, 6, 22, 0, 14, 6, 0, 174) )

# Reread time from RTC
_time = ds.datetime()
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )

days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % days[weekday] )
