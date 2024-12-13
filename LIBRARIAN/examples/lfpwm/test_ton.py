# Low Frequency PWM Driver to control High Inertia Devices
# Test the time ON / time OFF condition for SSR devices
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/lfpwm
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
pwm = LowFreqPWM( pin=led, period=2.5, ton_ms=9, toff_ms=10 ) # period=2.5s, needs 9ms to get activated, 10ms to get it off

pwm.duty_u16( 65535 / 2 ) # 50% duty cycle

# Note: always prefer to use the duty_u16() in priority
#
#pwm.duty_ms( 12 ) # Should stay off because of ton + toff
#pwm.duty_ms( 50 ) # Should get ativated for 50ms
#pwm.duty_ms( pwm.period_ms-8 ) # Should ALWAYS stay on because of toff.
