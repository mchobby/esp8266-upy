""" Demonstrate the usage of the lcd3310 is a FrameBuffer based MicroPython
    driver for the Olimex MOD-LCD3310 or Nokia 3310 display.

MOD-LCD3310 : http://shop.mchobby.be/product.php?id_product=1867
MOD-LCD3310 : https://www.olimex.com/Products/Modules/LCD/MOD-LCD3310/open-source-hardware

see project: https://github.com/mchobby/esp8266-upy/tree/master/modlcd3310

Author:
  20 july 2020 - Domeu - initial code writing

The MIT License (MIT) - see LICENSE file
"""

import time
from machine import SPI, Pin
from lcd3310 import LCD3310

# Pyboard - create the bus & Pins
ssel = Pin( "Y5", Pin.OUT, value=True ) # Not selected by default
lcd_reset = Pin( "Y9", Pin.OUT, value=True ) # Not selected by default
lcd_data  = Pin( "Y10", Pin.OUT, value=True ) # Data/Command (Data by default)
spi = SPI( 2 ) # y7=mosi, y6=sck

lcd = LCD3310( spi, ssel, lcd_reset, lcd_data )
print( "contrast: %s" % lcd.contrast )
# See all Framebuffer Method for more information
# https://docs.micropython.org/en/latest/library/framebuf.html
#
lcd.fill( 1 ) # Light-up all points
lcd.text( "Hello", 0,0,0 ) # text, x,y, color=0=transparent
lcd.update()
time.sleep( 3 )

lcd.clear()
lcd.text( "MCHobby<3", 3, 12 )
lcd.text( "Micro-", 3, 12+10 )
lcd.text( "   Python", 3, 12+10+10 )
lcd.rect(0,0,83,47,1)
lcd.update()

lcd.contrast = 110 # 0..127
