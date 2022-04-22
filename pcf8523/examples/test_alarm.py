""" MicroPython driver for the PCF8523 RTC over I2C.

	Test the RTC alarm feature by setting it to now + 30 sec

	Dominique Meurisse for MCHobby.be - initial portage
"""

from machine import I2C
from pcf8523 import PCF8523
import time

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1)

rtc = PCF8523( i2c )

# Get the current time
now = rtc.datetime
print( "now   @ Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(now) )

# Calculate Alarm 1 minute in the future
alarm_time = now + 60
alarm_tuple = time.localtime(alarm_time) # Year, month, day, hour, min, sec, weekday, yearday
alarm_minutes = alarm_tuple[4]

# set the alarm for activerate every hour & <alarm_min>
rtc.alarm_weekday( enable=False )
rtc.alarm_day    ( enable=False )
rtc.alarm_hour   ( enable=False )
rtc.alarm_min( alarm_minutes, True )

# set the alarm for activerate every day at 6:30
# rtc.alarm_weekday( enable=False )
# rtc.alarm_day    ( enable=False )
# rtc.alarm_hour   (  6, True )
# rtc.alarm_min    ( 30, True )

# set the alarm for activerate every monday at 8:00
# rtc.alarm_weekday(  1, True ) # 0 = Sunday
# rtc.alarm_day    ( enable=False )
# rtc.alarm_hour   (  8, True )
# rtc.alarm_min    (  0, True )

# Re-read alarm setting
print( "alarm_wday:", rtc.alarm_weekday() )
print( "alarm_day :", rtc.alarm_day() )
print( "alarm_hour:", rtc.alarm_hour() )
print( "alarm_min :", rtc.alarm_min() )

# Activate PCF8523 interrupt pin on alarm. Quite handy to wake-up a microcontroler
#  Interrupt pin goes to 3.3V on alarm
#rtc.alarm_interrupt = True

counter = 0
while True:
	counter += 1
	print('Testing alarm status, pass %i' % counter )
	if rtc.alarm_status:
		print( "Alarm catched!")
		print( "Tuuut Tuuut Tuuut Tuuut Tuuut Tuuut")
		print( "Reset alarm status ")
		rtc.alarm_status = False
	time.sleep( 10 )


print( "That s all Folks!" )
