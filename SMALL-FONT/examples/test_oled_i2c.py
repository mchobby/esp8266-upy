""" Test the SmallFont drawer over a OLED display (exposing a FrameBuffer interface).

See: https://github.com/mchobby/esp8266-upy/tree/master/SMALL-FONT

domeu, 20 Sept 2020, Initial Writing (shop.mchobby.be)
"""
from machine import Pin, I2C
import time
import ssd1306
from sfont import FontDrawer

i2c = I2C( sda=Pin(23), scl=Pin(22) ) # ESP32
# i2c = I2C( sda=Pin(4), scl=Pin(5) ) # ESP8266

lcd = ssd1306.SSD1306_I2C( 128, 32, i2c )
fd = FontDrawer( lcd, font_color=1, bgcolor=0 )

# Drawing with MicroPython font
lcd.text( "MicroPython! <3", 0, 0 )

# Standard FrameBuffer Drawing (horizontal line)
lcd.hline( 0, 16, 128, 1 ) #x,y, width, color

# Print with small font (use the font drawer)
fd.text( "MicroPython! <3", 0, 20 )

lcd.show()  # display / Afficher!
