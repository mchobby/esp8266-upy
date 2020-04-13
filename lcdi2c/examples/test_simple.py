"""
test_simple.py - test the basic feature of lcdi2c.py driver (LiquidCrystal_I2C portage to MicroPython).

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-backpack-i2c-3232100008823.html
---> https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html
	 The two transistor must be removed.
---> https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  12 april 2020 - Dominique - initial script
"""
from machine import I2C
from lcdi2c import LCDI2C
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Initialise l'ecran LCD
lcd = LCDI2C( i2c, cols=16, rows=2 )
lcd.backlight()

# display a message (no automatic linefeed)
lcd.print("Hello, from MicroPython !")
sleep( 2 )
# horizontal scrolling
for i in range( 10 ):
	lcd.scroll_display()
	sleep( 0.500 )

# backlight control
for i in range( 3 ):
	lcd.backlight(False)
	sleep( 0.400 )
	lcd.backlight()
	sleep( 0.400 )

# Clear screen
lcd.clear()

# Move the cursor + print
lcd.set_cursor( (4, 1) ) # Tuple with Col=4, Row=1, zero based indexes
lcd.print( '@' )
# or do positionning+print with a single print() call
lcd.print( '^', pos=(10,0) )
lcd.print( '!', pos=(10,1) )
sleep( 2 )

# Clear screen
lcd.clear()
lcd.home()  # Cursor at home position
lcd.cursor()
lcd.blink() # Blinking cursor
lcd.print( "Cursor:" )
