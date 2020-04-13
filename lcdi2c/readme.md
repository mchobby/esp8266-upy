[This file also exists in ENGLISH here](readme_ENG.md)

# Utiliser un afficheur LCD I2C (cristaux liquides) avec MicroPython PyBoard

La bibliothèque proposée ci-dessous fonctionne avec l'afficheur [LCD 16x2](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/176-lcd-16x2-extra-blanc-sur-bleu-3232100001763.html) + [backpack I2C](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008823.html), le [LCD 20x4 équipé d'un backpack I2C](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html) ou avec l'[afficheur LCD I2C de DFRobot](https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html) ([lien vers DFRobot](https://www.dfrobot.com/product-135.html?search=dfr0063&description=true)).

![afficheur LCD avec backpack I2C](docs/_static/lcd-i2c-example.jpg)

Cette bibliothèque `lcdi2c.py` permet de contrôler facilement ces afficheurs.

# Raccordement

## MicroPython Pyboard

Comme la Pyboard est 5V tolérant, il est possible de raccorder directement l'afficheur sur la Pyboard.

![Afficheur LCD I2C sur MicroPython Pyboard](docs/_static/LCD-I2C-to-pyboard.jpg)

L'adresse du module sur le bus I2C dépend:
* Du circuit utilisé PCF857AT ou PCF8574T
* Et des pontages d'adresse A0, A1, A2

Vous pouvez très facilement déduire ces informations à partir de l'image suivante:

![Afficheur LCD I2C adresse I2C](docs/_static/LCD-I2C-addresses.jpg)

L'adresse I2C par défaut du pilote est 0x27. Si celle-ci est différente, elle peut être précisée durant la création de l'instance du pilote.

```
# Adresse par défaut (0x27)
lcd = LCDI2C( i2c, cols=16, rows=2 )

# Adresse personnalisée
lcd = LCDI2C( i2c, cols=16, rows=2, address=0x38 )
```

## Utiliser l'afficheur LCD I2C de DFRobot

Il est également possible d'utiliser l'afficheur [LCD I2C de DFRobot](https://www.dfrobot.com/product-135.html?search=dfr0063&description=true) avec une Pyboard.

![Exemple afficheur LCD I2C de DFRobot](docs/_static/customchar_dfrobot.jpg)

Le breakout doit être légèrement modifié pour enlever les deux transistors Q1 et Q2 qui perturbent la communication I2C avec la Pyboard.

Il faut également enlever les 3 cavaliers d'adresses pour revenir à l'adresse par défaut 0x27.

![DFRobot LCD I2C, modification pour Pyboard](docs/_static/DFRobot-LCD-I2C-modification-1.jpg)

puis le raccordement sur la Pyboard se réduit aux connexions suivantes

![DFRobot LCD I2C sur Pyboard](docs/_static/DFRobot-LCD-I2C-modification-2.jpg)

# Code de test

Pour pouvoir utiliser l'afficheur, il est nécessaire d'installer la bibliothèque `lcdi2c.py` sur la carte MicroPython.

L'exemple ci-dessous, également disponible dans le script [`test_simple.py`](examples/test_simple.py) exploite la plupart des fonctions de la bibliothèque.

```
from machine import I2C
from lcdi2c import LCDI2C
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)

# Initialise l'ecran LCD
lcd = LCDI2C( i2c, cols=16, rows=2 )
lcd.backlight()

# Affiche un messagee (sans retour à la ligne automatique)
lcd.print("Hello, from MicroPython !")
sleep( 2 )
# Défillement horizontal
for i in range( 10 ):
	lcd.scroll_display()
	sleep( 0.500 )

# Contrôle du rétro-éclairage
for i in range( 3 ):
	lcd.backlight(False)
	sleep( 0.400 )
	lcd.backlight()
	sleep( 0.400 )

# Effacer l'écran
lcd.clear()

# Déplacer le curseur + affichage
lcd.set_cursor( (4, 1) ) # Tuple avec Col=4, Row=1, index de 0 à N-1
lcd.print( '@' )
# ou faire un positionnage + affichage avec un seul appel à print()
lcd.print( '^', pos=(10,0) )
lcd.print( '!', pos=(10,1) )
sleep( 2 )

# Effacer l'écran
lcd.clear()
lcd.home()  # Curseur à la position "home"
lcd.cursor() # Afficher curseur
lcd.blink()  # Curseur clignotant
lcd.print( "Cursor:" )
```

L'exemple ci-dessous indique comment créer un caractère personnaliser et l'afficher sur l'afficheur. Ce code est disponible dans le script ['test_customchar.py'](examples/test_customchar.py)

Il est possible de créer facilement des caractères personnalisés en utilisant le site "[LCD Custom Character Generator](https://maxpromer.github.io/LCD-Character-Creator/)".

```
from machine import I2C
from lcdi2c import LCDI2C

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Initialise l'ecran LCD
lcd = LCDI2C( i2c, cols=16, rows=2 )
lcd.backlight()

# Index de 0 à 7. Définition du caractère (charmap) composé de 8 octets de 5 bits chacun.
# Utiliser le générateur de caractère sur https://maxpromer.github.io/LCD-Character-Creator/
lcd.create_char( 0,
	[ 0b00000,
	  0b01010,
	  0b11111,
	  0b11111,
	  0b11111,
	  0b01110,
	  0b00100,
	  0b00000 ] )

# Afficher le caractère 0 à la position (0,0)
lcd.home()
lcd.write( 0 )
lcd.print( 'MC Hobby', (4,0) )
lcd.set_cursor( (15,0) )
lcd.write( 0 )
```

Autres exemples
* [`test_raw.py`](examples/test_raw.py) : indique comment envoyer des données brutes vers l'afficheur
* [`test_autoscroll.py`](examples/test_autoscroll.py) : demontre l'usage de l'option autoscroll.

# Où acheter
* [Gamme MicroPython](https://shop.mchobby.be/fr/56-micropython) chez MC Hobby
* [LCD 16x2](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/176-lcd-16x2-extra-blanc-sur-bleu-3232100001763.html) + [backpack I2C](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008823.html) chez MC Hobby.
* [LCD 20x4 équipé d'un backpack I2C](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html) chez MC Hobby
* [afficheur LCD I2C de DFRobot](https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html) chez MC Hobby
* [afficheur LCD I2C de DFRobot](https://www.dfrobot.com/product-135.html?search=dfr0063&description=true) chez DFRobot
