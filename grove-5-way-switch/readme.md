[This file also exists in ENGLISH](readme_ENG.md)

# Utiliser la carte Grove I2C "5 Way Switch" (SeeedStudio) sous MicroPython

Cette carte Grove produite par SeeedStudio présente un Joystick 4 position + click qui peut être interrogé via le bus I2C.

![Grove 5 way switch de SeeedStudio](docs/_static/grove-5-way-switch.jpg)

Ce module de SeeedStudio supporte un mécanisme d'événements permettant de détecter
* simple/double click,
* pression longue,
* événement press/release .

Une fonctionnalité intéressante de cette carte est la possibilité de modifier son adresse I2C par voie logicielle. Il est donc possible de combiner plusieurs périphériques identique sur un même bus I2C (après en avoir au préalable modifié l'adresse I2C).

La classe `Grove5Way` prend en charge les services spécifiques à ce module.

## Aussi module 6 DIPs

La bibliothèque permet également d'utiliser un module DIP I2C de SeeedStudio.

![Grove 6 DIP switch de SeeedStudio](docs/_static/grove-5-dip-switch.jpg)

Cette interface utilisera la classe `Grove6Dip` et accompagnée de l'exemple [testdip.py](examples/testdip.py) .

## Non compatible 3.3V

La tension d'alimentation et celle des signaux I2C est de 5V.

Il __faudra impérativement__ un _Level Shifter_ sur les signaux SDA et SCL si le microcontrôleur n'est pas tolérant 5V (ex: le Pico)

__Note:__ la méthode MicroPython `I2C.scan()` ne retourne aucun résultat pour l'adresse I2C du module. Notez donc bien la nouvelle adresse I2C si celle-ci est modifiée.


# Raccordement

## Raspberry-Pi Pico

Un _level shifter_ est utilisé pour convertir les signaux SDA et SCL du bus I2C de 3.3V (Pico) vers 5V (Grove) et vice-versa.

__Note:__ ce module grove peut aussi être alimenté en 3.3V, auquel cas le _level shifter_ est inutile.

![Grove 5 way switch sur Raspberry-Pi Pico](docs/_static/grove-5-way-switch-to-pico.jpg)

# Tester

Pour pouvoir utiliser ce contrôleur, il est nécessaire d'installer la bibliothèque [`lib/grove5way.py`](lib/grove5way.py) sur la carte MicroPython. Pour utiliser un module "6 DIP Switch", il faut aussi copier la bibliothèque [`lib/grove6dip.py`](lib/grove6dip.py) sur la carte.

L'exemple __le plus complet__ n'est pas présenté dans ce readme mais disponible dans le script [examples/testevent2.py](examples/testevent2.py)

## Mode RAW

Le code de [examples/test.py](examples/test.py) suivant démontre les fonctionnalités de base en testant les positions du joystick. Il exploite le mode RAW (par défaut) afin d'obtenir les états des boutons.

La methode `get_event()` retourne un objet de type `ButtonEvent`. Cet objet permet de tester les propriété `up`, `down`, `left`, `right`, `click` (ou `a`,`b`,`c`,`d`,`e`)

``` python
from machine import I2C
from grove5way import Grove5Way
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

sw = Grove5Way( i2c )
print( 'versions    :', sw.device_version() ) # Retourne 10 octets de version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( 'event mode  :', 'RAW')

# Utiliser des expression lambda pour associer une fonction de test à un libellé
text_n_test = { 'Up'     : lambda ev : ev.up,
				'Down'   : lambda ev : ev.down,
				'Left'   : lambda ev : ev.left,
				'Right'  : lambda ev : ev.right,
				'CLICK!' : lambda ev : ev.click }

while True:
	ev = sw.get_event()
	print( '.' )
	# print( 'has_event', ev.has_event )
	# print( 'a,b,c,d,e', ev.a, ev.b, ev.c, ev.d, ev.e )
	# print( 'up,down,left,right,clicked', ev.up, ev.down, ev.left, ev.right, ev.click )
	if ev.has_event:
		# Approche intéressante pour tester ev.up(), ev.down, ...
		for text, test in text_n_test.items():
			if test( ev ):
				print( text )
	time.sleep(0.250)
```

Ce qui produit le résultat suivant:

```
MicroPython v1.15 on 2021-04-18; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> import test
versions    : 1
version     : 1
Switch Count: 5
event mode  : RAW
.
.
.
.
Up
.
Up
.
Up
.
.
.
Down
.
Down
.
.
Left
.
Left
.
.
.
Right
.
Right
.
.
CLICK!
.
CLICK!
.
.
.
.
CLICK!
.
CLICK!
.
CLICK!
.
```

## Mode EVENT

Le script [examples/testevent.py](examples/testevent.py) permet de détecter les événements sur les bouton UP et CLICK (uniquement ces boutons pour faciliter la lecture du script).

Un exemple complet est disponible dans [examples/testevent2.py](examples/testevent2.py) .

``` python
from machine import I2C
from grove5way import Grove5Way
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

sw = Grove5Way( i2c )
sw.set_event_mode( True )
print( 'versions    :', sw.device_version() ) # Retourne 10 octets de version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( 'event mode  :', 'EVENT')
print( '' )
print( 'ONLY  UP and CLICK buttons')
print( '' )

while True:
	ev = sw.get_event()
	print( '.' )
	if ev.has_event: # Y a t'il un événement pour l'un des boutons ?
		# Tester le bouton UP
		if ev.up_events.has_event:
			print( 'UP' )
			if ev.up_events.single_click :
				print( '  +-> Single click')
			if ev.up_events.double_click :
				print( '  +-> Double click')
			if ev.up_events.long_press :
				print( '  +-> long press')
			if ev.up_events.level_changed :
				print( '  +-> level changed')
		# Tester le bouton CLICK
		if ev.click_events.has_event:
			print( 'CLICK' )
			if ev.click_events.single_click :
				print( '  +-> Single click')
			if ev.click_events.double_click :
				print( '  +-> Double click')
			if ev.click_events.long_press :
				print( '  +-> long press')
			if ev.click_events.level_changed :
				print( '  +-> level changed')

	time.sleep(0.250)
```

Ce qui produit le résultat suivant:

```
>>> import testevent
versions    : 1
version     : 1
Switch Count: 5
event mode  : EVENT

ONLY  UP and CLICK buttons

.
.
UP                    >>> PRESSER le bouton et le maintenir enfoncé
  +-> level changed   >>> Note: lire la propriété "up" pour connaître l'état
.
.
.
.
UP
  +-> long press
.
.
.
UP                   >>> RELACHER le bouton
  +-> level changed
.
.
.
.
UP                   >>> Clicker et relacher le bouton
  +-> Single click
.
.
.
.
UP
  +-> Single click
  +-> level changed  >>> Commencer une opération double click
.
UP
  +-> Double click
  +-> level changed
.
.
.
.
.
CLICK
.
CLICK
.
.
CLICK
.
CLICK
.
.
```

## Changer adresse I2C

Le script de test [examples/testaddr.py](examples/testaddr.py) montre comment exploiter les méthodes `unlock()` et `change_address()` pour modifier l'adresse I2C du module.

__ATTENTION:__ il est important de bien identifier et noter la nouvelle adresse du module.

# Liste d'achat
* [Raspberry-Pi Pico](https://shop.mchobby.be/product.php?id_product=2025
) @ MCHobby
* [4bits level-shifter (I2C compatible)](https://shop.mchobby.be/product.php?id_product=131)
