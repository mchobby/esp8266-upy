"""  test DS3231 RTC driver

	Author: Th Monin, Jan 2021
	Copyright Th Monin 2021 Released under the MIT license.
"""
import time

# from pyb import I2C, RTC, LED
from machine import I2C
from ds3231 import DS3231

#from pyb import RTC
#rtc = RTC()
#print("\nSystem datetime: {}".format(rtc.datetime()))

# PYBStick: sda=S3, scl=S5
i2c = I2C(1)
ds3231 = DS3231(i2c)
print("DS3231 datetime: {}\n".format(ds3231.datetime()))
print("DS3231 tempreature: {}°C\n".format(ds3231.temperature()))
