"""
test_firmware.py - Create custom char & display it (SparkFun LCD-16397).

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

# Custom Character Definition
HEART = [
0b00000,
0b01010,
0b11111,
0b11111,
0b11111,
0b01110,
0b00100,
0b00000]

SMILEY = [
0b00000,
0b00000,
0b01010,
0b00000,
0b00000,
0b10001,
0b01110,
0b00000]

FROWNIE = [
0b00000,
0b00000,
0b01010,
0b00000,
0b00000,
0b00000,
0b01110,
0b10001]

ARMS_DOWN = [
0b00100,
0b01010,
0b00100,
0b00100,
0b01110,
0b10101,
0b00100,
0b01010]

ARMS_UP = [
0b00100,
0b01010,
0b00100,
0b10101,
0b01110,
0b00100,
0b00100,
0b01010]


# Adresse par défaut (0x72)
# Ajouter parametre address=0x38 pour une adresse personnalisée
lcd = SerLCD( i2c, cols=16, rows=2 )

lcd.backlight( (255,255,255) ) # white
lcd.contrast( 5 ) # almost max
lcd.right_to_left(False) # from LeftToRight
lcd.cursor( False )

lcd.create_char(0, HEART)
lcd.create_char(1, SMILEY)
lcd.create_char(2, FROWNIE)
lcd.create_char(3, ARMS_DOWN)
lcd.create_char(4, ARMS_UP) # Seems to be drawedd at position 0,0

lcd.clear()
lcd.print( 'I ' )
lcd.write_char( 0 )
lcd.print( ' SerLCD')
