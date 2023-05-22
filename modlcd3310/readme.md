[This file also exists in ENGLISH here](readme_ENG.md)

# Utiliser un afficheur Nokia 3310 avec MicroPython (FrameBuffer)

Cet afficheur LCD de 84 x 48 pixels est toujours disponible aujourd'hui et facile a trouver.

Il utilise une interface SPI (un seul sens) pour communiquer les données vers l'écran, le débit est donc suffisamment rapide pour offrir un affichage fluide et confortable.

![mod-lcd3310](docs/_static/mod-lcd3310-2.jpg)

Le [MOD-LCD3310 d'Olimex](https://shop.mchobby.be/fr/uext/1867-afficheur-noirblanc-84x48-px-nokia-3310-3232100018679-olimex.html) est équipé d'un connecteur UEXT standardisé qui facilite la connexion sur les interfaces disposant déjà du connecteur UEXT.

![mod-lcd3310](docs/_static/mod-lcd3310-back.jpg)

Puisque l'empattement est de 2.54mm, il est possible de connecter facilement cet écran sur un grand nombre de plateforme à l'aide de connecteurs Dupont.

__Note:__ la toute première ligne de l'écran ne peut pas être adressée suite à un décalage d'un bit dans la RAM de l'écran. Cela doit encore être corrigé.

# Bibliothèque

Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/modlcd3310")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/modlcd3310
```

# Brancher

## Pyboard avec connecteur UEXT

Nous proposons le montage d'un connecteurs UEXT standard sur la carte MicroPython Pyboard,  [les raccordements sont décris dans ce dépôt](https://github.com/mchobby/pyboard-driver/tree/master/UEXT).  

![connecteur UEXT sur Pyboard](docs/_static/UEXT-Breakout-LowRes.jpg)

Il ne reste plus qu'à brancher le module sur votre carte.

## Pyboard sur MOD-LCD3310

Voici comment brancher la Pyboard directement sur le connecteur UEXT du MOD-LCD3310.

![connecteur UEXT sur Pyboard](docs/_static/modlcd3310-to-pyboard.jpg)

# Tester

Avant de pouvoir exécuter le code de test, il est nécessaire de copier la bibliothèque `lib/lcd3310.py` sur votre carte MicroPython.

Le pilote LCD3310 hérite de [`framebuf.FrameBuffer`](https://docs.micropython.org/en/latest/library/framebuf.html) et dispose donc de toutes les méthodes de dessin proposé par le FrameBuffer.

L'exemple suivant indique comment mettre exploiter l'écran avec le pilote (toutes les méthodes du FrameBuffer ne sont pas utilisées ici).

``` python
import time
from machine import SPI, Pin
from lcd3310 import LCD3310

# Pyboard - créer les bus et broches nécessaires
ssel = Pin( "Y5", Pin.OUT, value=True ) # Non sélectionner par défaut
lcd_reset = Pin( "Y9", Pin.OUT, value=True ) # Non sélectionné par défaut
lcd_data  = Pin( "Y10", Pin.OUT, value=True ) # Data/Command (Data par défaut)
spi = SPI( 2 ) # y7=mosi, y6=sck

lcd = LCD3310( spi, ssel, lcd_reset, lcd_data )
print( "contrast: %s" % lcd.contrast ) # Afficher le constrat

# Voir aussi les méthodes FrameBuffer pour plus d'information
# https://docs.micropython.org/en/latest/library/framebuf.html
#
lcd.fill( 1 ) # Allumer tous les points
lcd.text( "Hello", 0,0,0 ) # text, x,y, color=0=transparent
lcd.update()
time.sleep( 3 )

lcd.clear()
lcd.text( "MCHobby<3", 3, 12 )
lcd.text( "Micro-", 3, 12+10 )
lcd.text( "   Python", 3, 12+10+10 )
lcd.rect(0,0,83,47,1)
lcd.update()

# Accroître le contrast (0..127)
lcd.contrast = 110
```

# Où acheter
* [MOD-LCD3310 - écran Nokia 3310 84x48 pixels](https://shop.mchobby.be/fr/uext/1867-afficheur-noirblanc-84x48-px-nokia-3310-3232100018679-olimex.html) @ MCHobby
* [MOD-LCD3310 - écran Nokia 3310 84x48 pixels](https://www.olimex.com/Products/Modules/LCD/MOD-LCD3310/open-source-hardware) @ Olimex
* [MicroPython boards](https://shop.mchobby.be/fr/56-micropython) @ MCHobby
