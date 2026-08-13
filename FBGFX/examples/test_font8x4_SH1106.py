""" Test font8x4 with SH1106 OLED display.

 	font8x4, font5x4 and other font-art stored into FBGFX/lib-external 
 	can also be used with any FrameBuffer based library (eg: OLED screen)

* Font Repo: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX 
* SH1106 OLED repo: https://github.com/mchobby/SH1106

* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from sh1106 import SH1106_I2C
from machine import I2C, Pin
from fbtext  import FBText

# The Font can be changed by uncommencing
#  one of the following lines.
#
# font5x4.py & font8x4 can be copied from /lib folder
# Other fonts are located in /lib-external folder
#
from font8x4 import Font8X4 as TheFont
# from font5x4 import Font5X4 as TheFont
# from font14x14 import Font14X14 as TheFont
# from digit24x24 import Font24X24 as TheFont

# Raspberry-Pi Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )
lcd = SH1106_I2C(128, 64, i2c, addr=0x3c) # SH1106 OLED display
text_drawer = FBText( lcd, lcd.width, lcd.height, TheFont() )

lcd.fill( 0 )
# Draw some text on the display FrameBuffer
text_drawer.text( "Hello world", 0, 0, 1 ) 
text_drawer.text( "12.:45!", 0, 40, 1 ) 
# Send data to display
lcd.show()