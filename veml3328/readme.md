[This file also exists in ENGLISH here](readme_ENG.md)

# Utiliser la capteur RGBCIr VEML3328 / VEML3328sl avec MicroPython

Ce capteur peut être utilisé pour mesurer la couleur de la lumière (R,G,B), lumière blanche (dite __Clear__), lumière infrarouge (dite __IR__) et est même capable de calculer l'éclairement en Lux.

![Breakout VEML3328sl](docs/_static/VEML3328sl-3V3-BRK-00.jpg)

Le breakout [VEML3328sl-3V3-BRK](https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/2877-veml3328sl-capteur-de-couleur-rgb-clair-infrarouge-3v3-i2c-3232100028777.html) est équipé des composants nécessaires pour brancher facilement ce capteur dans vos montages.

Il effectue des mesures sur les canaux R,G,B,Clear,Ir et retourne des entier 16bits (non signé, valeurs de 0..65535).

Grâce à l'ajustement de la sensibilité, du Gain (gain capteur), gain nnumérique et temps d'intégration, ce capteur peut-être utilisé pour une large gamme d'éclairage.

Le composant VEML3328sl peut-être utilisé pour:

* Evaluation de la balance des blancs
* Estimer et élimination des couleurs dominantes bleues et oranges
* Adjuster le rétro-éclairage d'un LCD en fonction des conditions de luminosité ambiante
* Contrôle et correction de la couleur en sortie (Ex: sur des LEDs)
* Détecter des environnements lumineux intérieurs/extérieurs
* Evaluation de la couleur 
* Evaluation de la tempédure d'une couleur (_Correlated Color Temperature_ aussi dite CCT). Voyez les notes applicatives.
* Evaluation de la luminosité en Lux
* Detecter la présence près du capteur (parce que cela modifie les conditions lumineuses près du capteur)

![Courbes de réponses du capteur VEML3328](docs/_static/VEML3328-response-graph.jpg)

Etant donné que la caractéristique spectrale du canal vert est très proche de la réponse de l'oeil humain, ce canal peut être utilisé pour mesurer assez précisément la luminosité en Lux.

En fonction de la configuration du capteur, la mesure de la luminosité (en Lux) peut atteindre un maximum de 150.000 Lux (150 KLux).

![VEML3328 évaluation Lux](docs/_static/VEML3328_lux-00.jpg)

![VEML3328 évaluation Lux](docs/_static/VEML3328_lux-01/jpg)

Le breakout expose les broches d'alimentation et le bus I2C permettant de brancher le capteur sur votre microcontrôleur préféré. La carte breakout dispose également de connecteurs Qwiic/StemmaQt pour un effectuer un raccorement ultra rapide sur une plateforme compatible.

La fiche technique offre de nombreuses informations utiles https://www.vishay.com/docs/84968/veml3328.pdf ([copie disponible ici](docs/veml3328.pdf)).

Les [notes de conception applicative pour VEML3328](docs/designingveml3328.pdf) (pdf) propose également des informations détaillées sur le calcul et surveillance des couleurs.

# Bibliothèque

La bibliothèque doit être copiée sur la carte MicroPython avant d'exécuter les exemples.

## Installer avec MPRemote

Sur une plateforme WiFi:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/veml3328")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/veml3328
```

## Installation manuelle

Vous pouvez également vérifier le contenu du fichier [package.json](package.json) pour identifier les fichiers à copier sur votre carte MicroPython.

# Brancher 

Raccorder le capteur est assez simple. Connnectez simplement le capteur sur un bus I2C. Vous pouvez également connecter le capteur avec un câble Qwiic/StemmaQt.

![VEML3328 sur Raspberry-Pi Pico](docs/_static/VEML3328-to-pico.jpg)

# Tester

## Mesures RGBCIr

Durant l'utilisation de ce capteur, le script peut fixer 4 paramètres d'acquisition:
* `veml.sensitivity( high=True )` : la sensibilité est habituellement haute (`high=True`). Dans les environnement très-très lumineux, il est souhaitable d'utiliser une faible sensibilité  `high=False` (however, les résultats ne seront pas correct dans les environnement à faible luminosité).
* `veml.gain( 4 )` : le gain du capteur avec une valeur de 0.5, 1, 2 ou 4.
* `veml.digital_gain(4)` : le gain numérique avec une valeur de 1, 2 ou 4.
* `veml.integration( 50 )` : plus grand sera le temps d'intégration, meilleur sera la précision mais la valeur retournée sera également plus élevée. Les valeurs possibles sont 50, 100, 200 ou 400 ms.

Le script d'exemple  [test.py](examples/test.py) montre comment configurer le capteur et effectuer des mesures. Les valeurs obtenues sont dans la gamme 0..65535.

```
from machine import I2C, Pin
from veml3328 import *
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
veml = VEML3328( i2c )

print( "Vishay VEML3328 RGBCIR color sensor" )
print( "  value [0..65535]" )
veml.enable()
veml.gain( 4 ) # 0.5, 1, 2, 4
veml.sensitivity( high=True )
veml.digital_gain(4 ) # 1, 2 , 4
veml.integration( 50 ) # 50, 100, 200, 400 ms

time.sleep( 1 )
while True:
	print( "Red  : %i" % veml.red )   # Rouge
	print( "Green: %i" % veml.green ) # Vert
	print( "Blue : %i" % veml.blue )  # Bleu
	print( "Clear: %i" % veml.clear ) # Canal clair
	print( "IR   : %i" % veml.ir )    # Canal InfraRouge
	print( "-"*40 )
	time.sleep_ms( 100 )
```

Voici les données obtenues avec quelques informations complémentaires

```
==== Eclairage direct du soleil (soleil couchant) ====

  veml.gain( 4 )
  veml.sensitivity( high=True )
  veml.digital_gain(4)
  veml.integration( 50 )


Red  : 65535   <<< Capteur saturé! Il faut diminuer le gain.
Green: 65535
Blue : 65535
Clear: 65535
IR   : 65535


  veml.gain( 4 )
  veml.sensitivity( high=True )
  veml.digital_gain(1)
  veml.integration( 50 )

Red  : 23884
Green: 36190
Blue : 16832
Clear: 65535  <<< toujours saturé dans le domaine clair
IR   : 20597


  veml.gain( 1 )
  veml.sensitivity( high=True )
  veml.digital_gain(1)
  veml.integration( 50 )


Red  : 13799  <<< gammes de valeur correctes
Green: 19451
Blue : 8744
Clear: 38222
IR   : 10801

==== Orienté vers l'intérieur de la pièce ====
==== Pas de lumière artificielle       t  ====

  veml.gain( 1 )
  veml.sensitivity( high=True )
  veml.digital_gain(1)
  veml.integration( 50 )


Red  : 88  <<< Très faibles résultats! Acroître les gains ou l'intégration
Green: 123
Blue : 58
Clear: 261
IR   : 121


  veml.gain( 4 )
  veml.sensitivity( high=True )
  veml.digital_gain(4 )
  veml.integration( 50 )


Red  : 963   <<< Valeur très faible en regard du gain. La pièce est sombre.
Green: 1388
Blue : 673
Clear: 2923
IR   : 1225

==== Orienté à l'intérieur de la pièce ====
==== Eclairage articiel LED            ====

  veml.gain( 1 )
  veml.sensitivity( high=True )
  veml.digital_gain(1)
  veml.integration( 50 )


Red  : 195
Green: 264
Blue : 105
Clear: 532
IR   : 122


  veml.gain( 4 )
  veml.sensitivity( high=True )
  veml.digital_gain(4 )
  veml.integration( 50 )


Red  : 2421
Green: 3292
Blue : 1307
Clear: 6594
IR   : 1245
```

## Mesure d'éclairement (Lux)

Le script [test-lux.py](examples/test-lux.py) montre comment effectuer une mesure en Lux avec ce capteur.

Notez qye la résolution Lux est calculée automatiquement en fonction de la configuration du capteur. Changer la configuration du capteur modifie la résolution Lux.

```
from machine import I2C, Pin
from veml3328 import *
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
veml = VEML3328( i2c )

print( "Vishay VEML3328 Lux sensor" )
veml.enable()
veml.gain( 4 )
veml.sensitivity( high=True )
veml.digital_gain( 4 )
veml.integration( 50 )

print( "VEML3328 config: %r" % veml.config )
print( "Lux Resolution : %s lux/cnt" % veml.config.lux_res )

time.sleep( 1 )
while True:
	print( "Lux: %i" % veml.lux )
	time.sleep_ms( 200 )
```

## Mesure haute luminosité

Le script [test_high_luminosity.py](examples/test_high_luminosity.py) configure le capteur en faible sensibilité.

Cette configuration est réservée au environnements très..très lumineux sinon il ne renverra pas de données fiables (pour un environement à faible luminosité).

![Evaluation Lux du VEML3328](docs/_static/VEML3328_lux-01/jpg)

# Liste d'achat

* La capteur [VEML3328sl-3V3-BRK](https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/2877-veml3328sl-capteur-de-couleur-rgb-clair-infrarouge-3v3-i2c-3232100028777.html) est disponible chez MCHobby.
