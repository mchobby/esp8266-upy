# FrameBuffer Digit Blitter - draw digit onto a target FrameBuffer of a SH1106 display
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
#
# Author: Meurisse Dominique
#
import time
from sh1106 import SH1106_I2C
from machine import SPI, I2C, Pin
from fbdigit import *

i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )
lcd = SH1106_I2C(128, 64, i2c, addr=0x3c)

digi = DigitBlitter2538Mono( lcd, format=framebuf.MONO_VLSB ) # use framebuf.MONO_HMSB if 90° rotation
for i in range(10): # 0..9
        lcd.fill(0)
        digi.blit_digit(  0, 0, i ) # Blit digit at given po
        digi.blit_colon(  0+digi.w+digi.spacing, 0 )
        lcd.show()
        time.sleep(1)

