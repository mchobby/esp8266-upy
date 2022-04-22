""" MicroPython driver for the PCF8523 RTC over I2C.

	Read the various attributes on the RTC

	Dominique Meurisse for MCHobby.be - initial portage

"""

from machine import I2C
from pcf8523 import PCF8523
import time

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1)

rtc = PCF8523( i2c )

# battery switch-over and battery low detection control
#   0b000 : battery switch-over function is enabled in standard mode; battery low detection function is enabled
#   0b001 : battery switch-over function is enabled in direct switching mode; battery low detection function is enabled
#   0b010, 0b011 : battery switch-over function is disabled - only one power supply (V DD ); battery low detection function is enabled
#   0b100 : battery switch-over function is enabled in standard mode; battery low detection function is disabled
#   0b101 : battery switch-over function is enabled in direct switching mode; battery low detection function is disabled
#   0b110 : not allowed
#   0b111 : battery switch-over function is disabled - only one power supply (V DD ); battery low detection function is disabled
print( "power_management: %s (%s)" % (rtc.power_management,bin(rtc.power_management)) )
# True if the device has lost power since the time was set.
print( "lost power      : %s" % rtc.lost_power )
# True if the interrupt pin will output when alarm is alarming.
print( "alarm interrupt : %s" % rtc.alarm_interrupt )
# True if alarm is alarming. Set to False to reset.
print( "alarm status    : %s" % rtc.alarm_status )
# True if the battery is low and should be replaced.
print( "battery low     : %s" % rtc.battery_low )
