[This file also exists in ENGLISH](readme_ENG.md)

# Contrôler une charge de 40V / 10A via I2C avec le breakout HT0740 de Pimoroni (PIM455)

Ce petit breakout est capable de controler un courant de 10A sous 40V (non PWMable).

![ht0740 breakout](docs/_static/ht0740.jpg)

Cette carte offre les fonctionnalités suivantes:
* Pilote de Mosfet HT0740
* Extension de GPIO via I2C TCA9554A
* MOSFET TPN2R304PL
* LED de statu blanche
* Compatible 3.3V ou 5V
* Totalement isolé
* 2 bits d'adresses disponibles (à l'arrière)

# Brancher

## Brancher HT0740 sur le PICO

![HT0740 sur un Pico](docs/_static/ht0740-to-pico.jpg)

## Brancher HT0740 sur le Pyboard

![HT0740 sur un Pyboard](docs/_static/ht0740-to-pyboard.jpg)

# Exemple

L'exemple [test_on_off.py](examples/test_on_off.py) montre comment utiliser la classe HT0740.

``` python
from machine import I2C
from ht0740 import HT0740
from time import sleep

# Pico, sda=GP6, scl=GP7
i2c = I2C(1)
# Pyboard, sda=X10, scl=X9
# i2c = I2C(1)

power = HT0740( i2c )

power.on()
sleep(2)
power.off()
sleep(2)

# Une autre facon d'activer la sortie
power.output( True )
sleep(2)
power.output( False )
print( "That s all Folks!")
```

# Ou acheter
* [HT0740 40V 10A MOSFET breakout](https://shop.mchobby.be/fr/bouton/1990-40v-10a-mosfet-controlable-via-i2c-3232100019904-pimoroni.html) @ MCHobby
* [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html) @ MCHobby
* [Raspberry-Pi PICO](https://shop.mchobby.be/fr/pico-raspberry-pi/2025-pico-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020252.html) @ MCHobby
