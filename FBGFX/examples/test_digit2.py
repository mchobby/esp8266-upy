# FrameBuffer Digit Blitter - draw time onto a target FrameBuffer of a SH1106 display
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
#
# Author: Meurisse Dominique
#
import time
from sh1106 import SH1106_I2C
from machine import SPI, I2C, Pin, RTC
from fbdigit import *

i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )
lcd = SH1106_I2C(128, 64, i2c, addr=0x3c)

rtc = RTC()
digi = DigitBlitter2538Mono( lcd, format=framebuf.MONO_VLSB ) # use framebuf.MONO_HMSB if 90° rotation
while True:
	dt = rtc.datetime()
        lcd.fill(0)
        digi.blit_time( 0, 0, dt[4], dt[5], colon=(dt[6]%2)==0 ) # hh, mm
        lcd.show()
        time.sleep(1)

