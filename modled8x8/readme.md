[This file also exists in ENGLISH here](readme_ENG.md)

# Créer un affichage LED avec les dalles MOD-LED8x8RGB
![MOD-LED8x8RGB - matrice LED 8x8 RGB avec une interface SPI](docs/_static/modled8x8.png)

Le __MOD-LED8x8RGB__ est un module LED 8x8 avec interface SPI créé par [Olimex](https://www.olimex.com).

Les modules peuvent être chainés pour créer un affichage numérique ou une dalle d'affichage LED RGB (3 couleurs fondamentales + combinaisons) ou dalles de LED blanches.

![MOD-LED8x8RGB - Matrice LED 8x8 RGB avec interface SPI](docs/_static/modled8x8-2.png)

Comme décrit dans la [fiche technique](https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware), les modules utilisent un protocol open-source simple et __le bus SPI dans un seul sens__.

Le module MOD-LED8x8RGB fait partie de la catégorie UEXT bien qu'il n'expose pas -in fine- le connecteur UEXT. Le connecteur UEXT est replacé avec un connecteur de type PinHeader permettant de chaîner les matrices ensembles. Il est également possible réaliser un simple câble de conversion pour obtenir une connextion UEXT sur une dalle (voir plus loin).

Ces modules peut être trouvés ici:
* [MOD-LED8x8RGB](https://shop.mchobby.be/fr/138-uext) @ MCHobby
* [MOD-LED8x8RGB](https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware) @ Olimex.com

# Implémentation FrameBuffer

Le pilote ModLedRGB hérite de la classe FrameBuffer de MicroPython. Par conséquent, toutes les méthodes de FrameBuffer son disponibles sur ModLedRGB et la classe ModLedRGB peut être fournie comme paramètre à n'importe quelle routine réclament un objet de type FrameBuffer.

Voir [Frame buffer manipulation @ MicroPython.org](http://docs.micropython.org/en/latest/library/framebuf.html) pour plus d'informations.

Attention, les __AXES X et Y de l'implémentation FrameBuffer__ est différent de l'implémentation Arduino originale (voir documentation technique dans le sous répertoire docs)!

Les axes FrameBuffer sont positionnés comme suit:

![MOD-LED8x8RGB - Axes FrameBuffer](docs/_static/modled8x8-framebuffer-axis.jpg)

L'instance de ModLedRGB peut être créé comme suit pour une seule dalle:
```
modled = ModLedRGB( spi, ss ) # Juste UNE dalle LED-8x8RGB
```

Une matrice peut être créée en faisant un chaînage de matrices en suivant le schéma ci-dessous

![Chaîner les module MOD-LED8x8RGB](docs/_static/modled8x8-framebuffer-chaining.jpg)

Avec deux lignes (2 rows) de trois colonnes (3 columns), l'assemblage de la matruce ModLedRGB doit être instancié comme suit:
```
modled =  ModLedRGB( spi, ss, width=3, height=2 ) # 6x LED-8x8RGB
```

# Bibliothèque

Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/modled8x8")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/modled8x8
```

# Raccordement

## Adaptateur MOD-LED8x8RGB vers UEXT
Voici un simple câble de connexion permettant de connecter le MOD-LED8x8RGB sur n'importe quel connecteur UEXT.

![UEXT to MOD-LED8x8RGB converter](docs/_static/uext_to_modled.png)

## Port UEXT
Si vous avez l'adaptateur tel que décrit ci-dessous alors vous pouvez utiliser le connecteur UEXT de votre plateforme favorite.

* Le raccordement d'un connecteur UEXT sur un ESP8266 est décris dans le [répertorie UEXT](../UEXT/readme_eng.md) de ce dépôt GitHub.
* L' [adaptateur UEXT pour MicroPython Pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT) qui est disponible sur le dépôt [Pyboard-Driver](https://github.com/mchobby/pyboard-driver).

## Connexion directe sur une Pyboard
Un branchement direct sur la Pyboard a été réalisé durant les premières expérimentations do MOD-LED8x8RGB. Voici le schéma utilisé!

![MOD-LED8x8RGB vers MicroPython Pyboard](docs/_static/modledrgb_to_pyboard.png)

_Note: Ce branchement est pleinement compatible avec [l'adaptateur UEXT pour MicroPython Pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT)_

# Tester

## Utiliser le FrameBuffer
MicroPython propre la classe FrameBuffer pour gérer efficacement les données envoyées vers les afficheurs.

Le pilote `ModLedRGB` (modled.py) a été développé sur la classe FrameBuffer et, par conséquent, hérite de tous les avantages offerts par la [manipulation du FrameBuffer](http://docs.micropython.org/en/latest/library/framebuf.html) comme dessiner des lignes, du texte, etc.

## Examples simples

Copier le fichier `modled.py` et le fichier de test `test.py` sur votre carte MicroPython.

Le fichier `test.py` (visible ci-dessous) peut être chargé dans la sessions REPL avec `import test`.

```
from machine import Pin, SPI
from modled import *

# Bus SPI matériel sur la Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # low @ 2 MHz
# Nous devons gérer le signal SS nous même
ss = Pin( Pin.board.Y5, Pin.OUT )

modled = ModLedRGB( spi, ss ) # Une seule dalle LED-8x8RGB

modled.rect(0,0,8,8,RED) #x,y, width, Height = x,y, Largeur, Hauteur
modled.rect(1,1,6,6,GREEN)
modled.rect(2,2,4,4,BLUE)
modled.rect(3,3,2,2,MAGENTA)
modled.show()
```

Ce qui produit le résultat suivant

![chaîner les MOD-LED8x8RGB](docs/_static/modled8x8-framebuffer-axis.jpg)

Le second exemple utilise une combinaison de 6 matrices

```
from machine import Pin, SPI
from modled import *

# Bus SPI matériel sur la Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # réduit @ 2 MHz
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

modled = ModLedRGB( spi, ss, width=3, height=2 )

modled.fill_rect(0,0,8,8,RED)
modled.fill_rect(8,0,8,8,GREEN)
modled.fill_rect(16,0,8,8,BLUE)
modled.fill_rect(0,8,8,8,BLUE)
modled.fill_rect(8,8,8,8,GREEN)
modled.fill_rect(16,8,8,8,RED)
modled.show()
time.sleep( 2 )

# Voir ce qu'il y a dans la mémoire FrameBuffer
# modled._dump()

colors = [ RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, WHITE, BLACK ]
for color in colors:
	y, y_sign = 0, 1
	for x in range( modled.pixels[0] ): # PixelWidth
		modled.clear()
		modled.vline( x, 0, modled.pixels[1], color )
		modled.hline( 0, y, modled.pixels[0], color )
		y += y_sign
		if (y >= modled.pixels[1]) or (y<0):
			y_sign *= -1
			if y<0:
				y = 0
			else:
				y = modled.pixels[1]-1 # Height
		modled.show()
		time.sleep(0.050)

# dessine des point
modled.clear()
modled.pixel( 2,2, GREEN ) # vert
modled.pixel( 3,3, BLUE ) # Bleu
modled.pixel( 4,6, YELLOW ) # Rouge + Vert = Jaune
modled.pixel( 7,6, MAGENTA ) # Rouge + Bleu  = Magenta
modled.pixel( 8,5, CYAN ) # Vert + Bleu  = Cyan
modled.pixel( 9,4, WHITE ) # Rouge + Vert + Bleu  = Blanc
modled.text( "MCH",0,8,MAGENTA) # font 8x8 pixels

modled.show()
```
Ce qui produit le résultat suivant:

![MOD-LED8x8RGB chaining](docs/_static/modled8x8-framebuffer-chaining.jpg)

# Exemple de Scrolling

Cet exemple va initialiser une matrice de 2x3 dalles RGB (donc 24px large et 16px haut).

Il ouvre alors le fichier `olimex.bmp` (correctement dimensionné avec 24 pixels de larges) et fait défiler son contenu sur le la matrice en utilisant la technique de clipping (voir [le readme de FILEFORMAT](https://github.com/mchobby/esp8266-upy/tree/master/FILEFORMAT) ).

Copier la bibliothèque `modled.py`, le fichier `test2x3pict.py` et l'image  `olimex.bmp` sur votre carte MicroPython.

__Bibliothèques supplémentaires requises:__ il est également nécessaire de copier les bibliothèques `bmp.py` et `img.py` en provenance de /FILEFORMAT/imglib/ . Ces fichiers sont destinés a lire des images bitmap en couleur 24 bits.

![Mise en place des dalles MOD-LED8x8RGB et de la Pyboard](docs/_static/test2x3pict-setup.jpg)

Le fichier `test2x3pict.py` (affiché ci-dessous) peut être chargé depuis une session REPL avec `import test2x3pict.py`.

Le script ouvre une image à l'aide de fonction _helper_ puis une opération de clipping intervient tout le long de l'image (sur sa hauteur).
A chaque opération de _clipping_ , le contenu du _clip area_ est envoyé -pixel par pixel- dans le l'objet MODLED (dans son FrameBuffer).
Ensutie la méthode `show()` est utilisée pour envoyer le contenu du FrameBuffer vers la matrice d'affichage.

[Le résultat peut être vu sur cette vidéo YouTube](https://youtu.be/EMIY1aa8jOM)

```
from machine import Pin, SPI
from modled import *
from time import sleep

from img import open_image

# Bus SPI matériel sur la Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # réduire @ 2 MHz
# Nous devons gérer le signal SS nous même
ss = Pin( Pin.board.Y5, Pin.OUT )

# 6 dalles LED-8x8RGB organisées en 2 lignes de 3 colones. Donc 24x16 pixels
modled = ModLedRGB( spi, ss, width=3, height=2 )

modled.clear()
modled.show()

# ClipReader ouvrant le fichier bitmap de 24x91 pixels
clip = open_image( "olimex.bmp" )

# 96-16 est le nombre de lignes à faire défiler sur l'afficheur
for y_scroll in range( 91-16 ):

	# Clip de l'image à y = y_scroll
	clip.clip( 0, y_scroll, 24, 16 )

	# Copier la zone clippée vers le FrameBuffer de MOD-LED8x8RGB
	for line in range( clip.height ): # 16 pixels de haut
		for row in range( clip.width ): # 24 pixels de large
			# Lire le pixel = color (r,g,b) --> convertir en couleur 3 bits --> dessiner le pixel dans le frameBuffer
			c = clip.read_pix()
			modled.pixel( row, line, colorTo3Bit(c) )
	modled.show()

# Fermer le fichier
clip.close()

sleep( 1 )
modled.clear()
modled.show()
```

# Où Acheter
* [MOD-LED8x8RGB @ MCHobby](https://shop.mchobby.be/fr/nouveaute/1625-mod-led8x8rgb-matrice-led-rgb-8x8-3232100016255-olimex.html) 8x8 RGB LED Matrix
* [MOD-LED8x8RGB @ Olimex](https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware) 8x8 RGB LED Matrix
* [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)
* [Gamme de produits UEXT](https://shop.mchobby.be/fr/138-uext)
