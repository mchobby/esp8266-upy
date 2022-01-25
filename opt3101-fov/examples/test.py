# Basic test for the Pololu 3412
#    3-Channel Wide FOV Time-of-Flight Distance Sensor Using OPT3101
#
#  Most interesting columns are:
#   * 2th column : brighness for low/high emitting level
#   * last column: distance in mm (quite reliable)
#
# See project repository and library at https://github.com/mchobby/esp8266-upy/tree/master/opt3101-fov
#
# History:
#   12/01/2022 - DMeurisse - Initial portage from Arduino code
#

from machine import I2C
from opt3101 import OPT3101, BRIGHTNESS_ADAPTIVE
import time

# Some testing code for Pico
i2c = I2C(0)
# for PYBStick-RP2040
# i2c = I2C(0, sda=Pin(16), scl=Pin(17))

sensor = OPT3101( i2c )

# This tells the OPT3101 how many readings to average
# together when it takes a sample.  Each reading takes
# 0.25 ms, so getting 256 takes about 64 ms.
# The library adds an extra 6% margin of error, making
# it 68 ms.  You can specify any power of 2 between
# 1 and 4096.
sensor.set_frame_timing( 256 )

# 1 means to use TX1, the middle channel.
sensor.set_channel( 1 )

# Adaptive means to automatically choose high or low brightness.
# Other options you can use here are High and Low.
sensor.set_brightness( BRIGHTNESS_ADAPTIVE )

print( "channel, brightness, temperature, ambiant, _i, _q, amplitude, distance(mm)")
while True:
	sensor.sample()
	print( "%s, %s, %s, %s, %s, %s, %s, %s" % (sensor.channel_used, sensor.brightness_used,
	           sensor.temperature, sensor.ambient, sensor._i, sensor._q, sensor.amplitude, sensor.distance) )
	time.sleep_ms(200)
