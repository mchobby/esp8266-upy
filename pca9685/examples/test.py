from time import sleep
from machine import I2C
# Import ServoCtrl, classe pour le controleur PMW
from servoctrl import ServoCtrl

# Initialise le bus I2C(2) on Pyboard Y9,Y10
i2c = I2C( 2 )

# Crée l'objet pour controleur PWM.
# Utilise l'adresse par défaut du controleur 0x40
driver = ServoCtrl( i2c )

# Positionne le servo moteur #15 à un angle de 45 degrés
driver.position( 15, 45 )

sleep(2)

# Positionne le servo moteur #15 à un angle de 180 degrés
driver.position( 15, 180 )

sleep(2)

# Positionne le servo moteur #15 à un angle de 0 degrés
driver.position( 15, 0 )

sleep(2)

# Positionne le servo moteur #15 à un angle de 90 degrés
driver.position( 15, 90 )

print( "That s all folks!")
