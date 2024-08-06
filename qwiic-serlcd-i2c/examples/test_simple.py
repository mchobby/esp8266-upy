"""
test_simple.py - test the basic feature of serlcd.py driver (SparkFun LCD-16397).

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

lcd.backlight( (0,255,0) ) # Green
time.sleep_ms(500)
lcd.backlight( (0,0,255) ) # Blue
time.sleep_ms(500)
lcd.backlight( (255,0,0) ) # Red

lcd.print( "Hello" )
time.sleep(2)
lcd.clear()
lcd.print( "World!" )
time.sleep(1)
lcd.display( False ) # Turn off LCD & BackLight
time.sleep(1)
lcd.display( True )  # Turn on LCD & restore backlight

lcd.set_cursor( (9,1) ) #column,line (zero based)
lcd.print("*")

lcd.contrast( 0 ) # Highest contrast. Value (0..255)
#lcd.contrast( 100 ) # should be totaly transparent

# Disable system messages like 'Contrast: 5'
lcd.system_messages( enable=False )

# Save the current LCD as Splash screen
# lcd.save_splash()

# Disable Splash Screen (at Power Up)
lcd.splash( enable=False )

# Change the SerLCD I2C address to a new I2C address (warning it is permanent)
# lcd.set_address( 0x73 )
