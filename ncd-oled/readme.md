[This file also exists in ENGLISH](readme_ENG.md)

 *** TRADUCTION ***

# Afficher des informations sur écran OLED SSD1306

L'afficheur OLED de NCD (__mini board__) facilite l'affichage de donnée de vos systèmes intégrés. Votre contrôleur peut afficher des données, du texte et même des graphiques sur l'afficheur OLED disposant d'une résolution de 128×64.

![I2COLED sur mini carte NCD](docs/_static/ncd_i2coled.png)

Les afficheurs OLED sont d'excellentes méthodes pour afficher des données variables et messages de débogage .

A prix très abordable, l'afficheur OLED permet de créer et apprendre très facilement...

Fonctionnalités principales:
* Afficheur OLED 2.3cm
* Affichage graphique 128×64
* Contrôleur OLED SSD1306
* Mini module I2C
* OLED disponible en Bleu, Blanc ou Jaune
* Alimenté depuis le bus I2C
* Adresse par défaut: 0x3C

## A propos des modules NCD
Les mini modules et carte I2C de NCD National Control Device / ncd.io sont conçus avec un connecteur standard à 4 broches très pratique. Grâce à ces connecteurs, plus besoin de souder et les modules peuvent être chaînés sur un bus I2C.

Cet afficheur OLED NCD n'a pas besoin de level shifter, ni de régulateur de tension.

# Brancher sur NCD

Il s'agit d'une mini carte I2C (__mini board__) basé sur un connecteur NCD, utilisez une interface appropriée pour vous y connecter. Ce dépôt propose une interface NCD pour [MicroPython Pyboard](https://github.com/mchobby/pyboard-driver/blob/master/NCD/README.md) et [ESP modules](../NCD/readme.md).

![Raccorder sur un Feather ESP8266](../NCD/ncd_feather.png)

![Raccorder sur une Pyboard](docs/_static/ncd_oled_to_pyboard.jpg)

Notez que __National Control Device propose [de nombreuses carte adaptateur](https://store.ncd.io/shop/?fwp_product_type=adapters) __ pour de nombreuses plateformes de développement.

# Tester
Copier le fichier [`ssd1306.py` depuis MicroPython.org](https://raw.githubusercontent.com/micropython/micropython/master/drivers/display/ssd1306.py) et `test.py` sur votre carte MicroPython.

le fichier `test.py` (édité ci-dessous) peut être chargé à la volée dans une session REPL avec `import test`

```
from machine import I2C, Pin
import ssd1306
import time

# Créer un bus I2C en adéquation avec votre plateforme.

# --- ESP8266 ---
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )
# lcd = ssd1306.SSD1306_I2C( 128, 64, i2c , addr=0x78)

# --- PYBOARD ---
# WARNING: sur la pyboard, le pilote ssd1306 est écrit pour machine.I2C (et pas pour pyb.I2C)
#          et le bus I2C doit être instancier avec une configuration spécifique des broches.
#          Voir le topic https://forum.micropython.org/viewtopic.php?f=6&t=4663
# Pyboard: SDA sur Y9, SCL sur Y10. Voir raccordement NCD sur https://github.com/mchobby/pyboard-driver/tree/master/NCD
#
pscl = Pin('Y9', Pin.OUT_PP)
psda = Pin('Y10', Pin.OUT_PP)
i2c = I2C(scl=pscl, sda=psda)
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c )

lcd.fill(1) # Remplir l'écran en blanc
lcd.show()  # Afficher!

# Remplir un rectangle noir
# fill_rect( x, y, w, h, c )
lcd.fill_rect( 10,10, 20, 4, 0 )
lcd.show()  # Afficher!
```

Ce qui affiche un petit rectangle noir sur un écran complètement allumé.


Ce second exemple charge des fichiers '.pbm' (_Portable Bitmap_ format) et les affiches sur l'écran OLED.

![I2COLED sur NCD mini board](docs/_static/ncd-oled-diplay-image.jpg)

 *** TRADUCTION *****

It will be necessary to transfers the `loadbmp.py` script and the `ncd-mch.pbm` & `upy-logo.pbm` files. See the __oled-ssd1306__ folder to see how to produce the `.pbm` files.

```
from machine import I2C, Pin
import ssd1306
import framebuf
import time

# Create the I2C bus accordingly to your plateform.

# --- ESP8266 ---
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )
# lcd = ssd1306.SSD1306_I2C( 128, 64, i2c , addr=0x78)

# --- PYBOARD ---
# WARNING: On pyboard, the ssd1306 driver is written for machine.I2C (not pyb.I2C)
#          and I2C bus must be instanciate against specific Pin configuration
#          see Topic https://forum.micropython.org/viewtopic.php?f=6&t=4663
# Pyboard: SDA on Y9, SCL on Y10. See NCD wiring on https://github.com/mchobby/pyboard-driver/tree/master/NCD
#
pscl = Pin('Y9', Pin.OUT_PP)
psda = Pin('Y10', Pin.OUT_PP)
i2c = I2C(scl=pscl, sda=psda)
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c )

lcd.fill(1) # Rempli l'écran en blanc
lcd.show()  # Afficher!

while True:
	# Code inspired from twobitarcade.net
	#   https://www.twobitarcade.net/article/displaying-images-oled-displays/
	with open('ncd-mch.pbm', 'rb' ) as f:
		f.readline() # Magic number    P4 for pbm (Portable Bitmap)
		f.readline() # Creator comment
		f.readline() # Dimensions
		data = bytearray(f.read())

	fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
	lcd.invert(1)
	lcd.blit(fbuf, 0, 0)
	lcd.show()

	time.sleep(3)

	with open('upy-logo.pbm', 'rb' ) as f:
		f.readline() # Magic number    P4 for pbm (Portable Bitmap)
		f.readline() # Creator comment
		f.readline() # Dimensions
		data = bytearray(f.read())

	fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
	lcd.invert(1)
	lcd.blit(fbuf, 0, 0)
	lcd.show()

	time.sleep(3)
```

# ressources
* See the GitHub [oled-ssd1306](https://github.com/mchobby/esp8266-upy/tree/master/oled-ssd1306) for more details about the SSD1306 driver, its method, etc.

# Where to buy
* NCD-I2COLED : http://shop.mchobby.be/
* NCD-I2COLED : https://store.ncd.io/product/oled-128x64-graphic-display-i2c-mini-module/
