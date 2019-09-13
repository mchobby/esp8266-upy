import time
from machine import I2C

# Import ServoCtrl, classe pour le controleur PMW
from servoctrl import ServoCtrl

# Initialise le bus I2C(2) on Pyboard Y9,Y10
i2c = I2C( 2 )

# Crée l'objet pour controleur PWM.
# Utilise l'adresse par défaut du contrôleur 0x40
driver = ServoCtrl( i2c )

# Passer d'un angle de 10 à 170° par pas de 10 degrés
for i in range( 1, 18 ):
     driver.position( 15, i*10 )
     time.sleep( 1 ) # Attendre une seconde

print( "That s all folks")
