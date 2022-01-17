[This file also exists in ENGLISH](readme_ENG.md)

# Utiliser le capteur de pression MPX5700AP sous MicroPython

Le MPX5700AP est un capteur analogique capable de mesurer la pression de l'air entre 15 KPa et 700 Kpa, ce qui représente une très large gamme de mesure.

En comparaison, la pression atmosphérique est de ~1013 hPa (soit 101.3 kPa). Avec 15 KPa, ce capteur est capable de mesurer une dépression très importante par rapport à la pression atmosphérique moyenne.

Le MPX5700AP offre une erreur maximale de 2.5% avec une grande précision et excellente fiabilité... le tout sans besoin de calibration.

![MPX5700AP Grove Kit](docs/_static/mpx5700a-kit.jpg)

SeedStudio propose un kit [Grove - Integrated Pressure Sensor (MPX5700AP)](https://www.seeedstudio.com/Grove-Integrated-Pressure-Sensor-Kit-MPX5700AP-p-4295.html) incluant un une carte MPX5700AP avec amplificateur ainsi qu'une seringue pour simuler pression et dépression.

![MPX5700AP Grove Kit](docs/_static/mpx5700a-grove.jpg)

Le kit s'articule autour d'une carte breakout incluant un amplificateur opérationnel LMV358 et d'un régulateur de tension HX4002 produisant une tension de sortie de 5V (peu importe la tension d'alimentation 3.3V ou 5V). Cette tension de 5V est utilisée pour alimenter le capteur de pression et le l'amplificateur opérationnel.

__Que représente 700 kPa et 500 kPa?__

La pression athmosphérique standard est d'environ 1024 mBar, ou encore 1024 hPa... ou encore __102.4 kPa__ .

La pression au dessus de nos têtes représente donc __102.4 kPa__ (soit un peu plus de 1 Atmosphère).

Avec 500 kPa, nous sommes à 5 fois la pression atmosphérique (et presque 7 fois pour 700 kPa).

__Pression Max pour 3.3V?__

En dessous de 480 kPa, le capteur peut être utilisé directement sur un système 3.3V (voir note de calcul en fin d'article).

480 kPa représente presque 5 fois la pression atmosphérique.

# Brancher

## Raspberry-Pico

Voici comment brancher sur un [Raspberry-Pi Pico](https://shop.mchobby.be/fr/pico-rp2040/2036-pico-header-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020368.html).

![mpx5700a to Raspberry Pico](docs/_static/mp5700ap-to-pico.jpg)

## PYBStick-RP2040

Voici comment brancher le capteur sur un [PYBStick RP2040](https://shop.mchobby.be/fr/pybstick/2331-pybstick-rp2040-26-broches-micropython-c-3232100023314-garatronic.html)

![mpx5700a to Raspberry Pico](docs/_static/mp5700ap-to-pybstick-rp2040.jpg)

# Tester

Le script de [test.py](examples/test.py) suivant effectue:
1. une lecture de la tension sur l'entrée analogique,
2. puis retransforme la tension en rawValue compatible avec l'exemple Arduino (voir note)
3. puis calcule kPa avec la formule `(rawValue-41)*700/(963-41)`

``` python
from machine import Pin, ADC
import time

adc = ADC(Pin(26)) # ADC0 sur GP26

while True:
	raw = adc.read_u16() # 0..65535 pour 0v..3.3v
	v = 3.3*raw/65535 # Transformer en tension
	kpa = (((v*1023)/5)-41)*700/(963-41)
	print( 'V: %8.6f, kPa: %s' % (v, kpa) )
	time.sleep(0.100)
```

Ce qui produit le résultat suivant:

```
V: 0.597913, kPa: 61.7495
V: 0.592273, kPa: 60.87344
V: 0.592273, kPa: 60.87344
V: 0.594690, kPa: 61.24889
V: 0.595496, kPa: 61.37404
V: 0.596301, kPa: 61.49919
V: 0.597107, kPa: 61.62435
V: 0.595496, kPa: 61.37404
V: 0.599524, kPa: 61.99979
V: 0.593884, kPa: 61.12375
V: 0.593079, kPa: 60.99859
```

Pour les amateurs de Thonny IDE et son plotter, vous pouvez utiliser l'exemple [plotter.py](examples/plotter.py) qui se contente de sortir la valeur de la pression en kPa.

# Notes de calculs

## Tension analogique pour 500 kPa et 700 kPa

En consultant le [code Arduino et les mesures du WiKi SeeedStudio](https://wiki.seeedstudio.com/Grove-Integrated-Pressure-Sensor-Kit/), je me suis demandé quelle était la tension max sur l'entrée analogique de l'Arduino pour 500 kPa (et 700 kPa, le maximum du capteur).

__Pour 500 kPa:__

```
500kPa = ((rawValue-offset)*700.0) / (fullScale-offset)

500kPa = ((rawValue-410)*700.0) / (9630-410)

rawValue = 6995.7
```

rawValue représente 10 captures __accumulées__ de valeur ADC d'Arduino. La valeur moyenne est donc de 699.5 (disons 700) sur l'ADC.

Une valeur de 700 sur l'ADC Arduino (5V, 10bits) représente `Vadc = 700 * (500/1024) = 3.41 V`

__Pour 700 kPa:__

En reprenant la formule avec 700kPa, nous avons :

```
700kPa = ((rawValue-410)*700.0) / (9630-410)
```

Ce qui correspond à une tension de 4.0V en signal de sortie du capteur.

__Conclusion:__

Avec une tension de sortie max de 3.41v pour 500 kPa, la tension de sortie du capteur est _presque_ compatible avec un système en logique 3.3V.

En descendant la pression maximale de 500 kPa de ~20 kPa, il serait possible d'utiliser sereinement un tel capteur en logique 3.3V sans aucun artifice.

A noter qu'une pression de 500 kPa représente presque 5 fois la pression atmosphérique donc 5 atmosphères, 5x1024hPa ou encore 5x1024mBar (donc 5 Bar).

A titre de comparaison, la pression au robinet est de 3 bar max (entre 1 et 3 Bar)... essayez d'empêcher l'eau de sortie du robinet revient à appliquer une contre pression équivalente (et dieux seul sait que cela n'est pas facile!).

## Quelle pression max pour 3.3V ?

La grande question est: __Quelle est la pression maximale pour ne pas dépasser 3.3V sur la sortie analogique ?__

En prenant le problème à l'envers, pour 3.3V sur l'entrée ADC, nous avons une valeur ADC = 3.3V * 1024 / 5 = 675.84 sur notre Arduino.

Pour rappel la formule de conversion utilise `rawValue` comme un cumul de 10 acquisitions ADC (soit 10x 675.84).

```
rawValue = 6758   

Pkpa = ((6758-410)*700.00)/(9630-410)

Pkpa = 481.95 kPa
```

Pour ne pas dépasser un signal de sortie de 3.3V sur le capteur, il faut rester sous une pression de 481.95 kPa

## Calcul de rawValue pour un système 3.3V
Si la valeur de `rawValue` n'est pas accumulée 10 fois alors la formule kPa devient `kPa = ((rawValue-41)*700.0) / (963-41)` (juste quelques zero en moins).

Dans la formule `kPa = ((rawValue-41)*700.0) / (963-41)`, la variable `rawvalue` correspond a une valeur entre 0 et 1023 capturée sur l'ADC 5V 10 bits d'un Arduino UNO.

Le problème, c'est que le Pico dispose d'un ADC 3.3V et retourne une valeur 16 bits!

Pour contourner le problème, la valeur lue sur le Pico est transformée en tension (celle produite par le capteur), celle qui serait aussi présente sur l'entrée analogique d'Arduino.

```
v = 3.3*raw/65535
```

Ensuite, on calcule la valeur rawValue correspondant sur l'Arduino

```
Volt = rawValue * 5 / 1023
```

Hors on connais déjà la tension puisqu'elle est mesurée sur l'ADC 3.3v!

Donc:

```
rawValue = Volt * 1023 / 5
```

La formule finale est donc

```
kPa = (( (Volt * 1023 / 5) -41)*700.0) / (963-41)
```

# Où acheter
* [Grove - Integrated Pressure Sensor Kit (MPX5700AP)](https://www.seeedstudio.com/Grove-Integrated-Pressure-Sensor-Kit-MPX5700AP-p-4295.html) @ SeeedStudio
* [Raspberry-Pi Pico](https://shop.mchobby.be/fr/pico-rp2040/2036-pico-header-rp2040-microcontroleur-2-coeurs-raspberry-pi-3232100020368.html) @ MCHobby
* [PYBStick RP2040](https://shop.mchobby.be/fr/pybstick/2331-pybstick-rp2040-26-broches-micropython-c-3232100023314-garatronic.html?search_query=rp2040&results=8) @ MCHobby
