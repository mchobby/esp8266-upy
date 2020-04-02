# Adafruit Motor Shield / Motor Wing support
Cette bibliothèque prend en charge le Motor Shield / Motor Wing d'Adafruit avec plusieurs plateformes MicroPython.

__STILL UNDER WRITING__

# Raccordement
La carte Motor Shield (ou Motor Wing) peut être utilisée avec plusieurs cartes microcontrôleur.

## Pyboard
xxxxx

## Pyboard-Uno-R3
Le motor shield peut être branché directement sur l'[adaptateur Pyboard-Uno-R3](https://shop.mchobby.be/fr/micropython/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html) et utilisé en conjonction avec les [bibliothèques Pyboard-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3).

# Tester
Pour pouvoir utiliser cette carte Breakout, il est nécessaire d'installer la bibliothèque sur la carte MicroPython en copiant les fichiers suivants:
* `xxxx.py`

## test_steppers.py
L'exemple `examples/motorshield/test_steppers.py` teste les différents styles de contrôle du moteur pas-à-pas:
* SINGLE : une seule bobine activée (économie d'énergie)
* DOUBLE : double bobine activée (couple maximal)
* INTERLEAVE : 1/2 pas (meilleure précision)
* MICROSTEP : 1/16 de pas

La [vidéo suivante]() permet de voir les 4 modes de fonctionnements.

Le contrôle d'un moteur pas-à-pas est relativement simple

```
from machine import I2C
from motorshield import MotorShield
from motorbase import SINGLE, DOUBLE, INTERLEAVE, MICROSTEP

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c )

# Stepper S1 (M1+M2)
stepper = sh.get_stepper( 200, 1 )
stepper.speed = 3
stepper.step( 200, dir=FORWARD, style=DOUBLE )
sleep( 2 )
stepper.step( 200, dir=BACKWARD, style=DOUBLE )
```

## test_stepper_speed.py
L'exemple `examples/motorshield/test_stepper_speed.py` permet de modifier la vitesse de rotation du moteur en utilisant un potentiomètre comme consigne.

La vitesse de rotation est limitée par le débit maximum du bus I2C puisque l'avance de chaque pas fait suite à une communication I2C pour modifier l'état des broches.

Ce temps de communication n'est pas tenu en compte dans le calcul du RPM et que plus le rapport pas/sec augmente et plus le temps de communication I2C à de l'importance.

```
from machine import I2C
from motorshield import MotorShield
from motorbase import FORWARD, BACKWARD, SINGLE, DOUBLE
from pyb import ADC

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c )

def arduino_map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

adc = ADC('X19')

# Test the various speed for a stepper on the MotorShield
stepper = sh.get_stepper( 200, 1 )
while True:
	val = adc.read() # Value between 0 et 4095
	rpm = arduino_map( val, 0, 4095, 1, 100 )
	print( "%s RPM" % rpm )
	stepper.speed = rpm
	stepper.step( 40, dir=FORWARD, style=DOUBLE )
```

La [vidéo suivante]() permet de voir le script en fonctionnement.

# Crédit
Ce code est basé sur le travail de [Mr Boulanger de CentralSupélec](https://wdi.supelec.fr/boulanger/MicroPython/AdafruitMotorShield).

La bibliothèque a été adaptée pour se rapprocher de l'interface de programmation du MotorShield Arduino.

# Ressource
* [Description de la classes Adafruit_MotorShield](http://adafruit.github.io/Adafruit_Motor_Shield_V2_Library/html/class_adafruit___motor_shield.html)
* [Code original de Frédéric Boulanger - CentralSupélec](https://wdi.supelec.fr/boulanger/MicroPython/AdafruitMotorShield)
