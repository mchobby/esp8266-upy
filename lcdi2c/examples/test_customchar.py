"""
test_customchar.py - Show how to create and display a custom char.

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

# Index from 0 to 7. Charmap is made of 8 bytes of 5 bits each.
# Help yourself with customchar creator @ https://maxpromer.github.io/LCD-Character-Creator/
lcd.create_char( 0,
	[ 0b00000,
	  0b01010,
	  0b11111,
	  0b11111,
	  0b11111,
	  0b01110,
	  0b00100,
	  0b00000 ] )

# Write char 0 at position (0,0)
lcd.home()
lcd.write( 0 )
lcd.print( 'MC Hobby', (4,0) )
lcd.set_cursor( (15,0) )
lcd.write( 0 )
