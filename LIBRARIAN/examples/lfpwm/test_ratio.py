# Low Frequency PWM Driver to control High Inertia Devices
# Allow to specify a duty cycle in percent ratio (0..100)
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN
#
#
# Compatible with:
#  * Raspberry-Pico : using the only Timer() available.
#
from lfpwm import LowFreqPWM
from machine import Pin
from os import uname

# User LED on Pico
led = None
if uname().sysname == 'rp2': # RaspberryPi Pico
	led = Pin( 25 )
else:
	raise Exception( 'Oups! Not test for plateform %s' % uname().sysname )

# Setup pwm
pwm = LowFreqPWM( pin=led, period=2.5 ) # 2.5s

pwm.duty_ratio( 50 ) # 50% duty cycle
# pwm.duty_u16( 0 ) # always Off
# pwm.duty_u16( 100 ) # always On
# pwm.deinit() # stop everything
