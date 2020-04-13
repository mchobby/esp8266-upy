"""
test_autoscroll.py - test the autoscroll feature of lcdi2c.py driver (LiquidCrystal_I2C portage to MicroPython).
                     Autoscroll, automaticagically scrool each character printing to the left or to the right

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-backpack-i2c-3232100008823.html
---> https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html
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

# Show the cursor (blink it)
lcd.cursor()
lcd.blink()

# Write everything on the right of the cursor
lcd.autoscroll( False )
lcd.set_cursor( (8,0) )
sleep(3)
lcd.print( 'data1')
sleep(3)

lcd.clear()
sleep(3) # Wait 3 second to show the cursor

# Write everything on the left of the cursor
lcd.autoscroll( True )
lcd.set_cursor( (8,0) )
lcd.print( 'data2' )
