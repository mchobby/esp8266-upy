[This file also exists in ENGLISH here](readme_ENG.md)

# LSM303 Magnétomètre (boussole) et accéléromètre

Voici un port MicroPython pour le breakout LSM303D de Pololu, boussole et accéléromètre pour Arduino.

![LSM303D de Pololu (2127)](docs/_static/LSM303D-pololu.jpg)

Ce breakout facilite la création de périphérique et permet de lire les données brutes de l'accélérometre et du magnétomètre. La bibliothèque dispose d'une fonction pour calculer l'angle par rapport au Nord magnétique (calcul compensé), très utile pour créer une boussole numérique.

Le LSM303D est également présent sur le [Zumo Robot pour Arduino](https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html) visible dans ce prototype préliminaire de l' [adaptateur PYBOARD-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3).

![LSM303D sur le Zumo Robot](docs/_static/LSM303D-zumo-robot.jpg)

MCHobby à porté ce code spécialement pour le [Zumo Robot pour Arduino](https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html) **fonctionnant avec [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)**

La bibliothèque MicroPython a été créée à partie de deux sources:
* La source Arduino est [la bibliothèque Arduino pour la carte LSM303 de Pololu](https://github.com/pololu/lsm303-arduino) @ GitHub qui contient de nombreuses ressources et références.
* La source CircuitPython est [la bibliothèque CircuitPython d'Adafruit pour LSM303](https://github.com/adafruit/Adafruit_CircuitPython_LSM303_Accel) @ GitHub.

# Raccordement

## Pyboard

![LSM303D vers Pyboard](docs/_static/lsm303d-to-pyboard.jpg)

## Pyboard-UNO-R3

Brancher l'adaptateur [PYBOARD-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3) avec la Pyboard sur le Robot Zumo pour Arduino.

Vous pouvez aussi réaliser les connexions Pyboard --> UNO-R3 comme indiqué sur le schéma [PYBOARD-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3).

# Test

Plusieurs scripts d'exemples sont disponibles pour démontrer l'usage de la bibliothèque. Ces exemples sont disponibles dans le sous-répertoire `examples`.

## Serial

Ce programme lit constamment l'accéléromètre et le magnétomètre, et communique les lectures x,y,z sur la session REPL.

Exemple de sortie:
```
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import serial
Acc:   -172   -179  17397    Mag:  -1088    416 -14702
Acc:   -148   -142  17253    Mag:  -1088    418 -14710
Acc:   -125   -156  17326    Mag:  -1087    422 -14709
Acc:   -168   -139  17309    Mag:  -1097    417 -14715
Acc:   -164   -123  17249    Mag:  -1093    427 -14710

```

Voir les commentaires la bibliothèque Arduino de Pololu pour convertir les données brutes en unit de g et en Gaus.

## Calibrate

Ce programme est similaire à l'exemple Serial, mais à la place d'afficher les lectures récentes, il affiche continuellement les valeurs minimales et maximales pour chaque axe du magnétomètre. Ces valeurs peuvent être utilisée pour calibrer la fonction `heading()` et exemple `heading.py` après avoir bougé le LSM303 dans toutes les orientations possibles.

Lorsque le script est interrompu (en pressant Ctrl+C) alors il affiche les vecteurs min et max pour le magnétomètre (avec les valeurs x,y,z pour chaque vecteur).
```
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import calibrate
Move around to calibrate the magnetometer min & max values
Press Ctrl+C to stop the script and catch the resulting vectors
Mag min:  -1025    446 -14693    max:  -1025    446 -14693
Mag min:  -1025    441 -14697    max:  -1016    446 -14693
...
[WHEN CTRL+C IS PRESSED]


=== Magnetometer Min & Max ===========================
running_min = <Vector -4000,-1253,-15179>
running_max = <Vector 927,4250,-8277>
```

## Heading
Ce script est utilisé pour lire les données de l'accéléromètre et du magnetomètre pour calculer l'orientation du magnétomètre (avec compensation, en degrés relatif au vecteur par défaut). Ces données sont communiquées et affichées dans la session REPL. Le vecteur par défaut est choisi pour pointer le long de la surface de la carte, dans le direction du dessus du texte sur la sérigraphie (c'est l'axe +X sur le breakout LSM303D de Pololu). Vous pouvez utiliser une autre référence de vecteur (voir les commentaires).

Pour un résultat plus précis, il est préférable d'initialiser les valeurs `m_min` et `m_max` en début de script avec les valeurs obtenues par l'exemple `calibrate.py`.

```
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import heading
Heading to north: 290.7362
Heading to north: 290.947
Heading to north: 290.969
Heading to north: 290.9015
```
# Où acheter

* [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/766-micro-python-pyboard-lite-accelerometre-3232100007666.html) @ MC Hobby
* [LSM303D breakout - 3D Compass and Accelerometer ](https://www.pololu.com/product/2127) @ Pololu
* [Robot Zumo pour Arduino](https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html) @ MCHobby
* [Robot Zumo pour Arduino](https://www.pololu.com/product/2510) @ Pololu
* [Convertisseur PYBOARD-UNO-R3 : Pyboard vers UNO-R3](https://shop.mchobby.be/fr/nouveaute/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html) @ MC Hobby
