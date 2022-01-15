"""  test.py - test the I2C OLED display
               Keeps care of the screen width & height

Driver Documentation:
   https://github.com/mchobby/esp8266-upy/tree/master/oled-ssd1306

Author(s): Meurisse D., MCHobby (shop.mchobby.be).
------------------------------------------------------------------------
History:
  15 january 2022 - Dominique - Add example code
"""

from machine import I2C, Pin
import ssd1306
import time

# Pyboard: sda=Y10, scl=Y9
# i2c = I2C(2)
# lcd = ssd1306.SSD1306_I2C( 128, 64, i2c )

# Feather ESP8266 + Oled FeatherWing: (Adafruit 2821 + )
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# lcd = ssd1306.SSD1306_I2C( 128, 32, i2c )

# MicroMod-RP2040 + Machine Learning Carrier Board + Qwiic Micro Oled
# SparkFun   DEV-17720, DEV-16400, LCD-14532
# i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# lcd = ssd1306.SSD1306_I2C( 64, 48, i2c, addr=0x3D )

# Raspberry-Pi Pico + Qwiic Micro Oled ( SparkFun, LCD-14532)
i2c = I2C( 1 ) # sda=GP6, scl=GP7
lcd = ssd1306.SSD1306_I2C( 64, 48, i2c, addr=0x3D )

# -- Rempli l'écran en blanc --
lcd.fill(1)
lcd.show()  # Afficher!
time.sleep(2)

# Remplis un rectangle en noir
# fill_rect( x, y, w, h, c )
lcd.fill_rect( 10,10, 20, 4, 0 )
lcd.show()  # Afficher!
time.sleep(2)

# -- Dessine un pixel en noir --
lcd.fill(0) # Rempli l'écran en noir
# pixel( x, y, c )
lcd.pixel( 3, 4, 1 )
lcd.show()  # Afficher!
time.sleep(2)

# -- Dessine un rectangle en blanc --
lcd.fill(0) # Rempli l'écran en noir
# rect( x, y, w, h, c )
lcd.rect( 3, 3, lcd.width-2*3, lcd.height-2*3, 1 )
lcd.show()  # Afficher!
time.sleep(2)

# -- Ligne Horizontale et Verticale --
lcd.fill(0) # Rempli l'écran en noir
# Dessine des lignes en blanc.
# Ligne horizontale hline( x,y, w, c )
#   donc fournir la largeur.
# Ligne verticale vline( x,y, h, c )
#   donc fournir la hauteur.
lcd.hline( 0, 18, lcd.width, 1 )
lcd.vline( 30, 0, lcd.height, 1 )
lcd.show()  # Afficher!
time.sleep(2)

# -- Lignes diverses --
lcd.fill(0) # Rempli l'écran en noir
# Dessine des lignes en blanc.
# line(x1,y1,x2,y2,c)
lcd.line(0,0,lcd.width,lcd.height,1)
lcd.line(0,lcd.height,lcd.width,0,1)
lcd.show()  # Afficher!
time.sleep(2)

# -- Afficher texte --
lcd.fill(0) # Rempli l'écran en noir
# Dessine du texte en blanc.
#   text( str, x,y, c )
lcd.text("Bonjour!", 0,0, 1 )
lcd.show()  # Afficher!
time.sleep(2)

# -- Défilement --
# Mise en place en dessinant une croix noir sur fond blanc.
lcd.fill(1) # Rempli l'écran en blanc
lcd.line(0,0,lcd.width,lcd.height,0) # noir
lcd.line(0,lcd.height,lcd.width,0,0) # blanc
lcd.show()  # Afficher!
time.sleep(2)
# Scroll Horizontal de 15 pixels vers la gauche.
lcd.scroll( -15, 0 )
lcd.show()
time.sleep(2)
# Puis Scroll Vertical de 8 pixels vers le bas.
lcd.scroll( 0, 8 )
lcd.show()
time.sleep(2)
