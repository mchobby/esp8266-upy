""" MicroPython driver for the PCF8523 RTC over I2C.

	Setting the MCU datetime from PCF8523 RTC. 
	This is the tasks performed when the MCU restart after a powecycle.

	remarks: 
	See the trf_date.py script if you need to initialize the PCF8523 RTC
	date and time..

	Dominique Meurisse for MCHobby.be - initial portage
"""
from machine import I2C, Pin
from machine import RTC as InternalRTC
from pcf8523 import PCF8523
import time

DAY_NAMES = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1, sda=Pin(6), scl=Pin(7))

mcu_rtc = InternalRTC()  # Internal RTC
pcf_rtc = PCF8523( i2c ) # External RTC

print('Transfer PCF RTC datetime -> MCU datetime')
mcu_rtc.datetime( pcf_rtc.datetime )

print(' ')
print('MCU RTC initialized!')

print(' ')
print( "=== MCU datetime ===" )
dt = mcu_rtc.datetime() # returns (y,m,d,weekday,hh,mm,ss,ms)
print( "datetime tuple:", dt )
# Display date time at European format
print( "Belgian format: %i/%i/%i  %i:%i:%i" % (dt[2],dt[1],dt[0],dt[4],dt[5],dt[6]) )

