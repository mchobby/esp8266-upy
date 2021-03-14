"""
test_icon.py - Draw simple icon onto the LCD

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

HEART_ICON = [
  [0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,1,1,0,1,1,1,0,0],
  [0,1,1,0,1,1,1,1,1,1,0],
  [0,1,0,1,1,1,1,1,1,1,0],
  [0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,1,1,1,1,1,1,0,0],
  [0,0,0,1,1,1,1,1,0,0,0],
  [0,0,0,0,1,1,1,0,0,0,0],
  [0,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0] ]

def draw_icon( lcd, from_x, from_y, icon ):
    for y, row in enumerate( icon ):
        for x, color in enumerate( row ):
            if color==None:
                continue
            lcd.pixel( from_x+x,
                       from_y+y,
                       color )

def randrange( max ):
    assert max < 256
    import urandom
    r = urandom.getrandbits(8)
    while r > max:
        r = urandom.getrandbits(8)
    return r

def random_icon( lcd, icon, count ):
    range_x = lcd.width - len(icon[0])
    range_y = lcd.height - len(icon)
    for i in range( count ):
        draw_icon( lcd,
           randrange( range_x ),
           randrange( range_y ),
           icon
           )

lcd = SPI_LCD12864( spi=spi, cs=cs )
# Random draw of 10 icons
while True:
	lcd.clear()
	random_icon( lcd, HEART_ICON, 10)
	lcd.update() # Show on LCD
	time.sleep(2)
