This file also exist in [English here](readme_ENG.md)

# Utiliser l'unit Encoder (U135) I2C Grove avec MicroPython

Le module "[U135: Encoder Unit I2C](https://shop.m5stack.com/products/encoder-unit)" de M5Stack est un module I2C permettant de créer un contrôleur rotatif I2C à l'aide d'un encodeur 30 impulsions par rotation (clickable) et offre également des LEDs RGB intelligents (SK6812, aussi nommé NeoPixels). Ce module est équipé d'une interface Grove permettant de faciliter les raccordements sur les plateformes exposant cette connectique.

![U135 - Encoder Unit, I2C, Grove interface](docs/_static/u135.jpg)


L'encodeur permet de:
* -32768 <= encoder_position <= 32767
* Detection de l'état du bouton (pressé ou non)
* deux LEDs RGB commandées avec un tuple (R,G,B) de (0,0,0) à (255,255,255)

__A noter:__
* Le module doit être alimenté en 5V (pour les LEDs RGB).
* Les signaux I2C sont en logique 3.3V

# Brancher

## Brancher sur Pico

![U135 to pico](docs/_static/u135-to-pico.jpg)

## Brancher sur M5Stack Core

Rien de plus simple...connectez le sur votre Core/Core2.

![U135 to pico](docs/_static/u135-to-core.jpg)

# Tester

Après avoir copié la bibliothèque [lib/i2cenc.py](lib/i2cenc.py), il est possible d'exécuter les scripts d'exemples.

## test

Le script [test.py](examples/test.py) repris ci-dessous permet de tester les fonctionnalités de base.

``` python
from machine import I2C
from i2cenc import I2CEncoder
from time import sleep

# Pico - I2C(0) - sda=GP8, scl=GP9
i2c = I2C(0)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

enc = I2CEncoder(i2c)

print( "Testing the LEDs" )
enc.color = (255,0,0) # Rouge
sleep( 0.5 )
enc.color = (0,255,0) # Vert
sleep( 0.5 )
enc.color = (0,0,255) # Bleu
sleep( 1 )
enc.color = (0,0,0) # Eteint

print( "Presser un bouton et touner l'encodeur")

last_v = 0
while True:
	if enc.button: # Est-ce que le bouton est actuellement pressé ?
		print( 'Button PRESSE')
		enc.position = 0 # Réinitialiser le comtpeur - ne fonctionne pas!

	v = enc.position # -32768 <= v <= 32767
	if v != last_v: # afficher uniquement si valeur changée
		print( v )
		last_v = v
	sleep( 0.05 )
```

## test_2led
Le script [test_2led.py](examples/test_2led.py) permet de commander les deux LEDs
indépendamment l'une de l'autre.

Ci-dessous les quelques lignes du script permettant de réaliser une telle opération.

``` python
...
enc = I2CEncoder(i2c)

enc.set_led( 1, (255,0,0) ) # Rouge
enc.set_led( 2, (0,255,0) ) # Vert
# Eteindre les deux LEDS
enc.color = (0,0,0)
```

## test_relative
Le script [test_relative.py](examples/test_relative.py) montre comment contourner
la limitation technique rencontrée.

En effet, si la [documentation technique](https://docs.m5stack.com/en/unit/encoder)
indique bien qu'il est possible de réinitialiser le compteur du module I2C Encoder
(en forçant sa position à une valeur arbitraire), dans les faits cela
ne fonctionne pas!

J'ai donc écrit une super class `I2CRelEncoder` avec la méthode `reset()` et
la propriété `rel_position` qui retourne la position depuis le dernier appel à
`reset()`
