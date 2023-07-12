This file [also existsin English](readme_ENG.md)

#  Lire des tags/cartes ISO14443A / MiFare avec le Chipset PN532 et MicroPython

Le PN532 est un contrôleur RFID/NFC populaire permettant de lire et écrire des tags (cartes RFID).

Grâce à la technologie NFC ce composant peut aussi communiquer et echanger des données avec un Smartphone.

Adafruit industries propose un excellent [breakout PN532](https://shop.mchobby.be/fr/cartes-breakout/528-rfid-nfc-controleur-pn532-3232100005280-adafruit.html) supportant le communication I2C, SPI, UART avec un un hôte (microcontrôleur ou ordinateur).

![Contrôleur RFID / NFC](docs/_static/rfid-nfc-controler.jpg)

La carte contrôleur PN532 NFC/RFID breakout (ADA364) peut être utilisée avec une alimentation 3.3V et des signaux en logique 3.3V.

Grâce a son UART 3.3V, nous pouvons facilement utilisé cette carte sur un microcontrôleur disposant encore d'un UART libre.

# En apprendre plus sur MiFare

Disposer de carte/tag capable de stocker des information est fabuleux.

Cependant, cela n'est pas aussi simple que déposer/glisser un fichier sur un lecteur USB externe.

Voici comment en apprendre plus sur les procédés de stockage de données sur des tags:
* [Cartes et tags MiFare](https://wiki.mchobby.be/index.php?title=PN532-RFID-NFC-Carte-et-tag-MiFare) (_MCHobby Wiki, Français_)
* [Manuel utilisateur PN532](https://www.nxp.com/docs/en/user-guide/141520.pdf) (_NXP, Anglais_)
* [MiFare Cards & Tags](https://learn.adafruit.com/adafruit-pn532-rfid-nfc/mifare) (_Adafruit, Anglais_)

# Bibliothèque

__Limitation de la bibliothèque__ : actuellement, seul la __communication par UART__ est pris en charge par la bibliothèque.

__Sponsor__ : Merci au [Lycée Français Jean Monnet](https://www.lyceefrancais-jmonnet.be/) qui a aimablement sponsorisé le développement de cette bibliothèque MicroPython.

La bibliothèque doit être copiée sur votre carte MicroPython avant d'utiliser les exemples.

Sur un microcontrôleur disposant d'une connectique WiFi:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/pn532-rfid")
```

Ou à l'aide de l'utilitaire `mpremote` depuis un ordinateur:

```
mpremote mip install github:mchobby/esp8266-upy/pn532-rfid
```

# Configuration matérielle

## Configuration série

Avant de brancher la carte breakout PN532 sur le microcontrôleur; le breakout doit être configuré pour utiliser l'UART afin d'interagir avec le MCU.

Les cavaliers SEL0 & SEL1 doivent tous les deux être placés en position OFF.

![Activation UART sur le PN532](docs/_static/pn532-uart-activation.jpg)

# Brancher

## Branchement série sur un Pico

![PN532 sur Pico via UART](docs/_static/pn532-serial-to-pico.jpg)

# Tests

## read_mifare.py

Le script [read_mifare.py](examples/read_mifare.py) accède au tag ISO14443A/MiFare puis:
1. Affiche son UID,
2. Authentification sur le secteur 1 (block_nr 4 à 7) avec la clé KEYA par défaut
3. Lecture des 16 bytes stockés dans le bloc #4

Par défaut, toutes les cartes vierges ont les données du bloc fixées à 0. Cela signifie que les 16 octets devraient être à 0x00.

``` python
$ mpremote run examples/read_mifare.py
{'FIRMWARE': '1.6', 'CHIPSET': 'pn532'}
SAM configured
Waiting for an ISO14443A/MiFare Card ...
Communication Error!
Communication Error!
Communication Error!
Found an ISO14443A card
  UID Length: 4 bytes
  UID Value: b'AA1CC105'
  UID      : AA 1C C1 05
Seems to be a Mifare Classic card (4 byte UID)
Trying to authenticate block 4 with default KEYA value
Sector 1 (Blocks 4..7) has been authenticated
Data Block 4: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

Lorsque le bloc contient des données (voir l'exemple `write_mifare.py` ci-dessous) celui-ci sera affiché comme ceci:

``` python
$ mpremote run examples/read_mifare.py
{'FIRMWARE': '1.6', 'CHIPSET': 'pn532'}
SAM configured
Waiting for an ISO14443A/MiFare Card ...
Communication Error!
Found an ISO14443A card
  UID Length: 4 bytes
  UID Value: b'D5138E71'
  UID      : D5 13 8E 71
Seems to be a Mifare Classic card (4 byte UID)
Trying to authenticate block 4 with default KEYA value
Sector 1 (Blocks 4..7) has been authenticated
Data Block 4: 4D 49 43 52 4F 50 59 54 48 4F 4E 20 48 45 52 45
```

## write_mifare.py

Le script [write_mifare.py](examples/write_mifare.py) accède au tag ISO14443A/MiFare et affiche son UID.

Il s'authentifie sur le bloc #4 à l'aide de la clé KEYA par défaut (secteur 1 du bloc 4..7).

Pour finir, une fois authentifié, le script écrit 16 octets (un bloc de données) dans le bloc #4.

Au démarrage du script, celui-ci affiche également les données qui seront écrites sous différents formats.
La représentation Hexadecimal (la dernière affichée) montre exactement chaque octet tels qu'il sera encodé dans le bloc.
Utilisez le script [read_mifare.py](examples/read_mifare.py) pour relire les données.

``` python
$ mpremote run examples/write_mifare.py
{'FIRMWARE': '1.6', 'CHIPSET': 'pn532'}
SAM configured
Waiting for an ISO14443A/MiFare Card for writing...
--- Data to Write ---
MICROPYTHON HERE
bytearray(b'MICROPYTHON HERE')
4D 49 43 52 4F 50 59 54 48 4F 4E 20 48 45 52 45
---------------------

Communication Error!
Communication Error!
Communication Error!
Found an ISO14443A card
  UID Length: 4 bytes
  UID Value: b'D5138E71'
  UID      : D5 13 8E 71
Seems to be a Mifare Classic card (4 byte UID)
Trying to authenticate block 4 with default KEYA value
Sector 1 (Blocks 4..7) has been authenticated
Block writen... script end!
That's all folks!
```
## memdump_mifare.py

Le script [memdump_mifare.py](examples/memdump_mifare.py) accède au tag ISO14443A/MiFare et affiche son UID.

Lorsqu'un carte MiFareClassic est détectée alors la clé universelle (0xFF,0xFF,0xFF,0xFF,0xFF,0xFF) est utilisé comme clé KEYB pour authentifier le script sur les différents secteurs.

Lorsque l'authentification est réussie les 4 blocs (16 octets chacun) d'un secteur sont affichés sous leur représentation hexadécimale.

Exemple de résultats avec une carte MiFare modifiée à l'aide du script [write_mifare.py](examples/write_mifare.py) (inspecter le contenu du bloc #4):

```
$ mpremote run examples/memdump_mifare.py
{'FIRMWARE': '1.6', 'CHIPSET': 'pn532'}
SAM configured
Waiting for an ISO14443A/MiFare Card for DUMPING ...
Communication Error!
Found an ISO14443A card
  UID Length: 4 bytes
  UID Value: b'D5138E71'
  UID      : D5 13 8E 71
Seems to be a Mifare Classic card (4 byte UID)
Block 00 : D5 13 8E 71 39 08 04 00 03 93 D5 2B 4D 24 70 90
Block 01 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 02 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 03 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 04 : 4D 49 43 52 4F 50 59 54 48 4F 4E 20 48 45 52 45
Block 05 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 06 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 07 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 08 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 09 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 10 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 11 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 12 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 13 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 14 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 15 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 16 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 17 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 18 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 19 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 20 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 21 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 22 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 23 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 24 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 25 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 26 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 27 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 28 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 29 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 30 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 31 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 32 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 33 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 34 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 35 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 36 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 37 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 38 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 39 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 40 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 41 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 42 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 43 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 44 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 45 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 46 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 47 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 48 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 49 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 50 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 51 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 52 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 53 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 54 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 55 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 56 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 57 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 58 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 59 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
Block 60 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 61 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 62 : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 63 : 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
```
# Liste d'achat
* [RFID/NFC Controleur PN532 - v1.6 + Extra (ADA 364)](https://shop.mchobby.be/fr/cartes-breakout/528-rfid-nfc-controleur-pn532-3232100005280-adafruit.html) @ MCHobby
* [RFID/NFC Controleur PN532 - v1.6 + Extra (ADA 364)](https://www.adafruit.com/product/364) @ Adafruit
