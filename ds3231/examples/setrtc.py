""" DS3231 RTC driver - Set the MCU RTC from the DS3231 RTC

"""

from machine import I2C
from ds3231 import DS3231

# PYBStick: sda=S3, scl=S5
from pyb import RTC
i2c = I2C(1)

ds = DS3231( i2c )

RTC().datetime( ds.datetime() )
