"""
test_firmware.py - Display the firmware version on the screen (SparkFun LCD-16397).

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://www.sparkfun.com/products/16397

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  05 august 2024 - Dominique - initial script
"""

from machine import I2C,Pin
from serlcd import SerLCD
import time

# Raspberry-Pi Pico
i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )


# Adresse par défaut (0x72)
# Ajouter parametre address=0x38 pour une adresse personnalisée
lcd = SerLCD( i2c, cols=16, rows=2 )

lcd.backlight( (255,255,255) ) # white
lcd.contrast( 5 ) # almost max
lcd.right_to_left(False) # from LeftToRight
lcd.cursor( False )

# Display the firmware version on the LCD
while True:
	lcd.cmd(ord(','))
	time.sleep_ms( 500 )
