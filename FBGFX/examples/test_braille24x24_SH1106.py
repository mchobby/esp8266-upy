""" Test braille24x24 font with SH1106 OLED display.

 	braille24x24 font-art is stored into FBGFX/lib-external.
 	It has been designed for learning braille alphabet
 	displayed on a OLED display.

     ^ for Capital indicator (dot 6)
     # for Numeric indicator (dot 3-4-5-6) 
     @ for symbol  indicator (dot 5) 
	 ** to diplay the Braille * (dot 3-5 dot 3-5)


 	Please, report braille error.

* Font Repo: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX 
* SH1106 OLED repo: https://github.com/mchobby/SH1106

* Author: Meurisse Dominique for MCHobby SPRL
"""
from machine import Pin
from sh1106 import SH1106_I2C
from machine import I2C, Pin
from fbtext  import FBText
from braille24x24 import Font24X24 as BrailleFont

# Raspberry-Pi Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )
lcd = SH1106_I2C(128, 64, i2c, addr=0x3c) # SH1106 OLED display
text_drawer = FBText( lcd, lcd.width, lcd.height, BrailleFont() )

lcd.fill( 0 )
# Draw some text on the display FrameBuffer
# ^ is the Capital indicator
text_drawer.text( "^test", 0, 0, 1 ) 

# Use # as number indicator
text_drawer.text( "#1245", 0, 40, 1 ) 

# Send data to display
lcd.show()
time.sleep(5)


lcd.fill(0)
# @ is the symbol indicator (5-6) used
# before ()
text_drawer.text( "@test", 0, 0, 1 ) 
