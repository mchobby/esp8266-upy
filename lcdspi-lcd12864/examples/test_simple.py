"""
test_simple.py - Simple test of the SPI_LCD12864 driver

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://shop.mchobby.be/fr/gravity-boson/1878-afficheur-lcd-128x64-spi-3-fils-3232100018785-dfrobot.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  08 march 2021 - Dominique - initial writing
"""

from machine import SPI, Pin
from lcd12864 import SPI_LCD12864
import time

# PYBStick: S19=mosi, S23=sck, S26=/ss
spi = SPI( 1 )
spi.init( polarity=0, phase=1 )
cs = Pin( 'S26', Pin.OUT, value=0 )

lcd = SPI_LCD12864( spi=spi, cs=cs )
lcd.text( "MicroPython !", 10, 25, 1 ) # X=5, Y=20, color=light
lcd.rect(0,0,128,64,1)
lcd.rect(3,3,128-6,64-6,1)
lcd.update() # Show on LCD
