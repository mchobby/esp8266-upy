[This file also exists in ENGLISH](readme_ENG.md)

# Interface SPI/I2C vers Série (UART) sous MicroPython

Ce pilote couvre le support SPI pour les composants suivants:

* SC16IS740IPW : un UART
* SC16IS750 : un UART + 8 GPIOs. SPI @ 4 Mb/S max.
* SC16IS760 : un UART + 8 GPIOs. SPI @ 15 Mb/S max.

# Bibliothèque

Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/sc16is7xx")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/sc16is7xx
```

# Brancher

## Pico vers MicroE SC16IS740 (RS232)
Le MicroE utilise un transceiver MAX3237 et un connecteur femelle DB9.

![Mikroe SC16SI740 avec connecteur DB9](docs/_static/db9-rs232.jpg)

Le câblage suivant est utilisé entre le bus SPI et le Pico

![Pico vers MikroE SC16IS740 MIKROE-3349](docs/_static/sc16is7xx-Mikroe-to-pico.jpg)

## Pico vers breakout SC16IS740/SC16IS750 (UART)

L'image suivante présente le raccordement entre le SC16IS750 et un Pico. Notez que le signal Reset est optionnel.

![Pico vers breakout SC16IS750](docs/_static/sc16is750-breakout-to-pico.jpg)

Ci après, le câblage indique comment brancher la broche d'interruption (IRQ) et le MCU.

![Pico vers breakout SC16IS750 avec IRQ](docs/_static/sc16is750-irq-to-pico.jpg)

# Exemples

## Les basiques

L'exemple [test_sc16is740_basic.py](examples/spi/test_sc16is740_basic.py) montre comment utiliser les fonctions de bases pour envoyer et recevoir des données via une ligne série.

L'UART du SC16IS7xx expose une interface identique à la classe __machine.UART__ . Par conséquent l'objet instancié peut être utilisé en lieu et place d'un UART MicroPython.

## Readline

L'exemple ci-dessous utilise un _GPS Ultimate_ et récupère les lignes de données émisent par le récepteur GPS.

L'exemple [test_sc16is740_readline.py](examples/spi/test_sc16is740_readline.py) montre comment utiliser la méthode `readline` de l'UART. Readline retourne un objet `bytearray` affiché dans la session REPL ainsi que sa conversion sous forme de `string`.

Ci-dessous, un extrait du résultat produit. Ce dernier peut être consulté dans le fichier [test_sc16is740_readline.result](examples/spi/test_sc16is740_readline.result) .

```
bytearray(b'$GPGGA,004212.000,5041.4423,N,00424.0377,E,1,03,3.20,102.6,M,47.4,M,,*69\r\n')
$GPGGA,004212.000,5041.4423,N,00424.0377,E,1,03,3.20,102.6,M,47.4,M,,*69

bytearray(b'$GPGSA,A,2,08,02,10,,,,,,,,,,3.35,3.20,1.00*0D\r\n')
$GPGSA,A,2,08,02,10,,,,,,,,,,3.35,3.20,1.00*0D

bytearray(b'$GPGSV,1,1,03,08,73,193,35,02,68,285,30,10,42,054,31*4F\r\n')
$GPGSV,1,1,03,08,73,193,35,02,68,285,30,10,42,054,31*4F
```

## Extra

Le script d'exemple [test_sc16is740_extra.py](examples/spi/test_sc16is740_basic.py) présente les fonctionnalités avancées  the basic script instruction to send and receive data over the serial line.

Les fonctions avancées sont:

* __any()__ : vérifie le nombre de caractères dans le RX FIFO.
* __any_tx()__ : vérifie le nombre de caractères dans le TX FIFO.
* __txdone()__ : vérifie s'il y a encore des données à envoyer.
* __fush()__ : attend que toutes les données soient expédiées.
* __sendbreak()__ : envoi une condition d'arrêt (break) sur la ligne TX.

## Sendbreak

La condition d'arrêt "Break" est un cas spécial qui maintient le signal TX un temps supérieur à celui nécessaire à l'envoi d'un simple caractère.

L'exemple [test_sc16is740_sendbreak.py](examples/spi/test_sc16is740_sendbreak.py) envoi un message à 1200 bauds, ce qui nécessite environ 500ms. 

![Message envoyé à 1200 bauds](docs/_static/sendbreak_0.jpg)

Une fois le message envoyé dans le TX FIFO, le script attend 200ms et force un long signal d'arrêt de 100ms. Cet appel `sendbreak()` s'insère  forcement durant l'émission du message!

![Message avec condition d'arrêt visible](docs/_static/sendbreak_1.jpg)

## Activation Auto-RTS

Tester le signal de sortie auto-RTS sur l'UART nécessite les branchements suivants:

* Brancher TX --> RX  (loopback)
* Brancher l'oscilloscope sur TX
* Brancher l'oscilloscope sur RTS

Le script [test_sc16is740_rts.py](examples/spi/test_sc16is740_rts.py) active l' AUTO-RTS puis surcharge la RX Fifo avec des messages.

L'exemple fixe le niveau __halt_trigger__ qui suspend la transmission et le niveau __resume_trigger__ qui reprend la transmission. Les deux niveaux doivent se situer dans la gamme 4..64 octets (par increment de 4 octets).

Ce qui produit les signaux suivants:

![RTS passe à LOW quand RX FiFo atteint le niveau halt](docs/_static/enable_rts.jpg)

RTS (Ready To Send) est une broche en sortie!

Il informe l'appareil distant lorsque des données peuvent être expédiés vers notre UART (HIGH=envoi, LOW=arrêt).

* RTS passe à LOW lorsque RX FIFO atteind le niveau "halt_trigger". L'appareil distant DOIT arrêter sa transmission.
* RTS passe à HIGH lorsque RX FIFO descend jusqu'au niveau "resume_trigger" et reste sous le niveau "halt_trigger". L'appareil distant peut émettre des données.

## Activation Auto-CTS

L' Auto-CTS désactive la transmission TX de l'UART lorsque CTS est placé au niveau HIGH par un signal externe.

Tester le signal d'entrée auto-CTS de l'UART nécessite les branchements suivants:

* Brancher un oscilloscope sur TX
* Brancher un oscilloscope sur CTS
* Un fil + résistance 1K connectés sur la broche CTS permet de placer le niveau logique de CTS soit sur 5V (HIGH), soit sur GND (LOW).

Le script [test_sc16is740_cts.py](examples/spi/test_sc16is740_cts.py) active l'AUTO-CTS. 

Le script expédie un très long flux de données à 300 bauds, ce qui nécessite environ 4 seconds. Ce laps de temps est suffisant pour pour manipuler le signal CTS à la main.

Ci-dessous, la capture du test effectué.

![TX est suspendu pendant que CTS est sur LOW](docs/_static/enable_cts.jpg)

## Auto-XOn/XOff

Le script [test_sc16is740_xon_xoff.py](examples/spi/test_sc16is740_xon_xoff.py) active le __contrôle automatique du flux logiciel__ (XON/XOFF).

Le script peut être exécuté comme émetteur (placer `IS_SENDER=True`) sur une carte. L'autre carte exécute le script en tant que récepteur (placer `IS_SENDER=False`).

Enfin, un oscilloscope est utilisé pour capturer les signaux RX et TX sur l'émetteur (sender). Il sera possible d'y voir le contrôle de flux xon/xoff en pleine action.

![auto XON-XOFF avec SC16IS740](docs/_static/enable_xon_xoff.jpg)

## Manipulation de GPIO

Les composants SC16IS750/760 disposent de GPIOs qui peuvent être configurés soit en entrée (pas de pull-up/down interne disponible), soit en sortie.

Voir les quelques exemples suivants pour plus d'informations:

* [test_sc16is750_read_pin.py](examples/spi/test_sc16is750_read_pin.py) : configure un GPIO en entrée puis lit l'état de la broche.
* [test_sc16is750_write_pin.py](examples/spi/test_sc16is750_write_pin.py) : configure un GPIO comme sortie puis modifie l'état de la sortie.
* [test_sc16is750_irq_pin.py](examples/spi/test_sc16is750_irq_pin.py) : obtenir un signal d'interruption lorsqu'une entrée change d'état.

## Signal d'interruption

Le SC16IS7xx expose une broche d'interruption (IRQ) qui peut être capturé par le microcontrôleur lorsque des conditions spécifiques sont rencontrées. 

Voir [ce schéma de branchement avec IRQ](docs/_static/sc16is750-irq-to-pico.jpg) utilisé avec les scripts d'exemples ci-dessous.

Note: Configurer le déclenchement d'IRQ peut s'avérer plus ou moins complexe. La bibliothèque prend en charge les cas de figure les plus répandu.

* [test_sc16is750_irq_pin.py](examples/spi/test_sc16is750_irq_pin.py) : déclencher une interruption lorsque le signal change sur une entrée.
* [test_sc16is750_irq_rxtx.py](examples/spi/test_sc16is750_irq_rxtx.py) : déclencher un interruption lorsque le rx/tx FIFO atteind un certain niveau. Démontre uniquement la configuration, la capture de l'interruption et le décodage de l' _IRQ Source_ .


## Un autre oscillateur?

La classe de base SC16IS7XX définit la fréquence de l'oscillateur à 1.8432 MHz (fréquence par défaut). 

Le script [test_sc16is740_osc.py](examples/spi/test_sc16is740_osc.py) montre comment instancier la classe avec une fréquence d'hrologe différente (certaines cartes peuvent être équipé avec des fréquences d'horloge différentes).