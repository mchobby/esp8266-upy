# I2C Bus on PYBOARD

# WARNING: On pyboard, the ssd1306 driver is written for machine.I2C (not pyb.I2C)
# and I2C bus must be instanciate against specific Pin configuration
# see Topic https://forum.micropython.org/viewtopic.php?f=6&t=4663
import machine
pscl = machine.Pin('Y9', machine.Pin.OUT_PP)
psda = machine.Pin('Y10', machine.Pin.OUT_PP)
i2c = machine.I2C(scl=pscl, sda=psda)

import ssd1306
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c )

lcd.fill(1) # Rempli l'écran en blanc
lcd.show()  # Afficher!

# Remplis un rectangle en noir
# fill_rect( x, y, w, h, c )
lcd.fill_rect( 10,10, 20, 4, 0 )
lcd.show()  # Afficher!
