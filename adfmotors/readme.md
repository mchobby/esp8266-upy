[This file also exists in ENGLISH](readme_ENG.md)

# Adafruit Motor Shield / Motor Wing support pour MicroPython
Cette bibliothèque prend en charge le [Motor Shield d'Adafruit](https://shop.mchobby.be/fr/shields/379-shield-de-controle-moteur-motor-shield-v2-3232100003798-adafruit.html) / [Motor Wing d'Adafruit](https://shop.mchobby.be/fr/feather-adafruit/830-featherwing-moteur-dc-pas-a-pas--3232100008304-adafruit.html) avec différentes plateformes MicroPython.

![MotorShield d'Adafruit](docs/_static/motorshield.jpg)

# Bibliothèque

 Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

 Sur une plateforme connectée:

 ```
 >>> import mip
 >>> mip.install("github:mchobby/esp8266-upy/adfmotors")
 ```

 Ou via l'utilitaire mpremote :

 ```
 mpremote mip install github:mchobby/esp8266-upy/adfmotors
 ```

# Raccordement
La carte Motor Shield (ou Motor Wing) peut être utilisée avec plusieurs cartes microcontrôleur.

Ci-dessous les différents schémas de raccordement de la carte MotorShield sur différentes cartes MicroPython.

Les raccordements des différents moteurs sont repris dans la section test.

## Pyboard
Avec la Pyboard, il faut alimenter la logique du MotorShield et utiliser le bus I2C pour permettre les échanges d'information avec le shield moteur.

![brancher Pyboard sur MotorShield](docs/_static/pyboard-to-motorshield.jpg)

## Pyboard-Uno-R3
Le motor shield peut être branché directement sur l'[adaptateur Pyboard-Uno-R3](https://shop.mchobby.be/fr/micropython/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html) et utilisé en conjonction avec les [bibliothèques Pyboard-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3).

![brancher Pyboard sur MotorShield](docs/_static/pyboard-uno-r3-to-motorshield.jpg)

## Pico - MotorWing
Le motor FeatherWing peut être branché directement sur un [Raspberry-Pi Pico](https://shop.mchobby.be/fr/pico-raspberry-pi/2025-pico-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020252.html) et utilisé en conjonction avec la bibliothèque [motorwing.py](lib/motorwing.py).

![brancher Pico sur Motor FeatherWing](docs/_static/pico-to-motorwing.jpg)

## Pico - MotorShield
Le motor Shield peut être branché directement sur un [Raspberry-Pi Pico](https://shop.mchobby.be/fr/pico-raspberry-pi/2025-pico-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020252.html) et utilisé en conjonction avec la bibliothèque [motorshield.py](lib/motorshield.py).

__ATTENTION: il faut la carte pour la logique 3.3V__

![brancher Pico sur MotorShield](docs/_static/pico-to-motorshield.jpg)

# Tester
Pour pouvoir utiliser cette carte Breakout, il est nécessaire d'installer la bibliothèque sur la carte MicroPython en copiant les fichiers suivants:
* `pca9685.py`
* `motorbase.py`
* `motorshield.py` : pour le MotorShield d'Adafruit
* `motorwing.py` : pour le Motor FeatherWing d'Adafruit

Les divers exemples sont stockés dans le répertoire:
* `examples/motorshield/` pour le MotorShield d'Adafruit (__contient tous les exemples de références__)

## Moteur continu sur Motor Shield
Il est possible de brancher jusque 4 moteurs continu sur les ports M1, M2, M3, M4.

![Brancher un moteur continu sur le MotorShield](docs/_static/motorshield-dcmotor.jpg)

Voici comment prendre le contrôle du moteur M2.

```
from machine import I2C
from motorshield import MotorShield
from motorbase import FORWARD, BACKWARD, BRAKE, RELEASE
from time import sleep

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c )

motor = sh.get_motor(2) # Moteur M2
try:
	motor.speed( 128 ) # Demi vitesse
	motor.run( FORWARD )
	sleep( 2 )
	motor.speed( 255 ) # Pleine vitesse
	motor.run( BACKWARD )

	# Attendre que l'utilisateur arrête le script
	# en pressant Ctrl+C
	while True:
		sleep( 1 )
except KeyboardInterrupt:
	motor.run( RELEASE )
```

Voir aussi l'exemple `examples/motorshield/test_dcmotors.py` qui teste toutes les fonctionnalités sur tous les ports.

## Moteur continu sur le FeatherWing moteur
Il est possible de brancher jusque 4 moteurs continu sur les borniers M1, M2, M3, M4.

__ATTENTION: Ne pas oublier d'utiliser la classe `MotorWing` __ a la place de ` MotorShield`.

![Brancher un moteur sur le FeatherWing moteur](docs/_static/dc-motor-motorwing.jpg)

Le script suivant [motorwing/test_dcmotor_m1.py](examples/motorwing/test_dcmotor_m1.py) met le moteur continu branché sur M1 en mouvement.

```
from machine import I2C
from motorwing import MotorWing
from motorbase import FORWARD, BACKWARD, BRAKE, RELEASE
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
# i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# Raspberry-Pi Pico - SDA=GP8, SCL=GP9
i2c = I2C(0)

sh = MotorWing( i2c )
motor = sh.get_motor(1) # Moteur M1
try:
	motor.speed( 128 ) # configure la vitesse initiale
	motor.run( FORWARD )
	# Attendre que l'utilisateur arrete le script
	# en pressant Ctrl+C
	while True:
		sleep( 1 )
except KeyboardInterrupt:
	motor.run( RELEASE )

print( "That's all folks")
```

La seule différence entre cet exemple pour le MotorWing et le MotorShield est la classe de contrôle `MotorWing` importé depuis `motorwing.py` .

En conséquence: les exemple pour moteur pas-à-pas et moteurs continus fonctionneront aussi avec le FeatherWing moteur. Remplacez simplement la clause d'importation et la classe créee.

## Moteur pas-à-pas sur Motor Shield
Le contrôle d'un moteur pas-à-pas est relativement simple. Voici un exemple de base, d'autres sont décris plus bas.

![Brancher un moteur pas-à-pas sur le MotorShield](docs/_static/motorshield-stepper.jpg)

```
from machine import I2C
from motorshield import MotorShield
from motorbase import SINGLE, DOUBLE, INTERLEAVE, MICROSTEP

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c )

# Moteur pas-à-pas sur S1 (M1+M2)
stepper = sh.get_stepper( 200, 1 )
stepper.speed = 3
stepper.step( 200, dir=FORWARD, style=DOUBLE )
sleep( 2 )
stepper.step( 200, dir=BACKWARD, style=DOUBLE )
```

## test_steppers.py
L'exemple `examples/motorshield/test_steppers.py` teste les différents styles de contrôle du moteur pas-à-pas sur les sorties S1 (M1+M2) + S2 (M3+M4).

Les style de contrôle sont les suivants:
* SINGLE : une seule bobine activée (économie d'énergie)
* DOUBLE : double bobine activée (couple maximal)
* INTERLEAVE : 1/2 pas (meilleure précision)
* MICROSTEP : 1/16 de pas

La [vidéo Youtube suivante](https://youtu.be/mRv0d036vCg) permet de voir les 4 modes de fonctionnements.

Ce qui produit le résultat suivant dans la sortie REPL:

```
MicroPython v1.11-473-g86090de on 2019-11-15; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>> import test_steppers
Stepper S1
 +-> SINGLE coil activation for full turn (energy saving)
 +-> DOUBLE coil activation for full turn (stronger torque)
 +-> INTERLEAVE for half turn (more precise)
 +-> MICROSTEP 1/16 for half turn
 +-> RELEASE motor
Stepper S2
 +-> SINGLE coil activation for full turn (energy saving)
 +-> DOUBLE coil activation for full turn (stronger torque)
 +-> INTERLEAVE for half turn (more precise)
 +-> MICROSTEP 1/16 for half turn
 +-> RELEASE motor
>>>
```

## test_stepper_speed.py sur Motor Shield
L'exemple `examples/motorshield/test_stepper_speed.py` permet de modifier la vitesse de rotation du moteur en utilisant un potentiomètre comme consigne.

La vitesse de rotation est limitée par le débit maximum du bus I2C puisque l'avance de chaque pas fait suite à une communication I2C pour modifier l'état sur les broches du PCA9685.

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

# Test les différentes vitesse du moteur pas-à-pas sur le MotorShield
stepper = sh.get_stepper( 200, 1 )
while True:
	val = adc.read() # Value between 0 et 4095
	rpm = arduino_map( val, 0, 4095, 1, 100 )
	print( "%s RPM" % rpm )
	stepper.speed = rpm
	stepper.step( 40, dir=FORWARD, style=DOUBLE )
```

La [vidéo YouTube suivante](https://youtu.be/9pRrGbrzA4g) permet de voir le script en fonctionnement.

## Servo-Moteur et PWM (sur Motor Shield UNIQUEMENT)

Le carte MotorShield expose 4 sorties PWM portant les libellés #15, #14, #1 et #0.
Ces sorties du PCA9685 peuvent être utilisées pour générer des signaux PWM et contrôler des servo moteurs.

Le graphique ci-dessous présente les deux cas d'utilisations (PWM et servo).

__ATTENTION:__ il ne fait jamais alimenter un servo-moteur avec une tension supérieure à 5 Volts (bien que normalement, 6V soit le maximum absolu).

![Brancher un servo moteur sur le MotorShield](docs/_static/motorshield-servo.jpg)

Le script suivant permet de prendre le contrôle du servo-moteur branché sur la sortie #15

```
from machine import I2C
from motorshield import MotorShield
from time import sleep

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c, freq=50 )

servo = sh.get_servo( 15 )

servo.angle( 90 )
sleep( 2 )
servo.angle( 0 )
sleep( 2 )
servo.angle( 180 )
sleep( 2 )
servo.angle( 90 )
sleep( 2 )

servo.release() # libérer le servo
```

La [vidéo YouTube](https://youtu.be/jKfkatqdVW8) suivante présente le résultat obtenu.

__Note importante__: La fréquence PWM idéale pour la commande de servo moteur est de 50 Hertz (d'où le paramètre `freq=50` lors de la création de l'instance `MotorShield`). __La fréquence PWM par défaut du MotorShield  (500 Hz) est beaucoup trop elevée__ pour le contrôle de servo-moteur (peu de servos fonctionnerons correctement). Suivant la qualité de vos servo-moteurs, vous pourrez opter pour une fréquence PWM entre 100 et 300 Hz, ce qui est un bon compromis lorsque vous utilisez aussi des moteurs continu et moteurs pas-à-pas.

L'exemple ci-dessous montre comment prendre le contrôle des sorties PWMs.

```
from machine import I2C
from motorshield import MotorShield
from time import sleep

# Pyboard & Pyboard-UNO-R3 - SDA=Y10, SCL=Y9
i2c = I2C(2)
sh = MotorShield( i2c )

# PWM sur la sortie  #0
pwm = sh.get_pwm( 0 )

# Signal HAUT
pwm.duty_percent( 100 )
sleep( 2 )
# Signal BAS
pwm.duty_percent( 0 )
sleep( 2 )
# Cycle utile @ 50%
pwm.duty_percent( 50 )
sleep( 2 )

# Le cycle utile peut être finement ajusté avec une valeur entre 0 (BAS) et 4095 (HAUT)
# Cycle utile a 2866 (donc 70%)
pwm.duty( 2866 )
sleep( 2 )

# Relacher controle PWM
pwm.duty( 0 ) # or duty_percent( 0 )
```

A noter que tous les appels des methodes `PWM` sont renvoyées vers la classe `PCA9685` en mentionnant la broche a utiliser.

# Crédit
Ce code est basé sur le travail de [Mr Boulanger de CentralSupélec](https://wdi.supelec.fr/boulanger/MicroPython/AdafruitMotorShield).

La bibliothèque a été adaptée pour se rapprocher de l'interface de programmation du MotorShield Arduino.

# Ressource
* [Description de la classes Adafruit_MotorShield](http://adafruit.github.io/Adafruit_Motor_Shield_V2_Library/html/class_adafruit___motor_shield.html)
* [Code original de Frédéric Boulanger - CentralSupélec](https://wdi.supelec.fr/boulanger/MicroPython/AdafruitMotorShield)

## Où acheter
* [Shield moteur d'Adafruit](https://shop.mchobby.be/fr/shields/379-shield-de-controle-moteur-motor-shield-v2-3232100003798-adafruit.html) disponible chez MCHobby
* [Feather MotorWing d'Adafruit](https://shop.mchobby.be/fr/feather-adafruit/830-featherwing-moteur-dc-pas-a-pas--3232100008304-adafruit.html) disponible chez MCHobby
* [Adaptateur Pyboard-UNO-R3](https://shop.mchobby.be/fr/micropython/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html) disponible chez MCHobby
* [Cartes MicroPython](https://shop.mchobby.be/fr/56-micropython) disponible chez MCHobby
* [Raspberry-Pi Pico](https://shop.mchobby.be/fr/pico-raspberry-pi/2025-pico-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020252.html) available at MCHobby
