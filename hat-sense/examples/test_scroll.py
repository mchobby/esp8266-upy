# Test scroll a text message on the Sense Hat.
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author: Meurisse D. for Shop.mchobby.be
#
from machine import I2C
from sensehat import SenseHat
import time

# PYBStick, Hat-Face: Sda=S3, Scl=S5
# Pyboard, Sda=X10, Scl=X9
# i2c = I2C( 1 )
# Raspberry-Pi Pico, Sda=GP8, Scl=GP9
i2c = I2C( 0 )
hat = SenseHat( i2c )

# See the FrameBuffer doc @ https://docs.micropython.org/en/latest/library/framebuf.html
#
hat.clear()
hat.scroll( "Sense-Hat running under MicroPython!" )
