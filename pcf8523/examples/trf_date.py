""" MicroPython driver for the PCF8523 RTC over I2C.
	Setting up date time of PCF8523 RTC with MCU datetime.

	* Transfert the MicroControler internal datetime to the PCF8523 RTC.

	* The microcontroler internal datetime can be first updated with mpremote
	  (official micropython utility).
   
		mpremote rtc --set

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

print( "=== MCU datetime ===" )
dt = mcu_rtc.datetime() # returns (y,m,d,weekday,hh,mm,ss,ms)
print( "datetime tuple:", dt )
# Display date time at European format
print( "Belgian format: %i/%i/%i  %i:%i:%i" % (dt[2],dt[1],dt[0],dt[4],dt[5],dt[6]) )

print( " " )
print( " " )

print( "Write MCU time to PCF8523 RTC...")
# PCF8523 time setting must also follow the datetime tuple format
#    (y,m,d,weekday,hh,mm,ss,ms)
# 	 weekday & ms can be set to 0 when setting the date... it will be recomputed
pcf_rtc.datetime = (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6], 0)
# The line above could also be written as follow 
#   pcf_rtc.datetime_tuple = dt

print( " " )
print( " " )

# Reread time from RTC
print( "=== PCF8523 RTC datetime ===" )
print( "RTC tuple:", pcf_rtc.datetime )


_timestamp = pcf_rtc.timestamp
print( "TimeStamp     :", _timestamp, "sec")
_ltime = time.localtime(_timestamp) # Transform into Python time tuple (format different from MicroPython DateTime tuple !!!)
print( "localtime     : Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % _ltime )
print( "Belgian format: %i/%i/%i  %i:%i:%i" % (_ltime[2],_ltime[1],_ltime[0],_ltime[3],_ltime[4],_ltime[5]) )
# Weekday 
weekday = _ltime[6]
print( 'Day of week   : %s' % DAY_NAMES[weekday] )
