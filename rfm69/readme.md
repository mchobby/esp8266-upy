[This file also exists in ENGLISH](readme_ENG.md)

# Transmettre des donnée par les airs à l'aide du Module RFM69 Packet Radio (SX1231) et de MicroPython

Il est facile de travailler avec le module RFM69. C'est une module bien connu et facile à comprendre.

![Module RFM69](docs/_static/rfm69.jpg)

Module qu'il ne faut pas confondre avec la technologie Radio LoRa certes plus puissante mais aussi plus coûteuse.

Il existe de nombreuses variantes de ce module exploitant différentes fréquences (433 Mhz, 868 Mhz to 915 Mhz) et 2 modulations différentes.

__Le RFM69HW est un module fiable capable d'envoyer des packets de données de 60 octets par les airs__.

Caractéristiques du RFM69HCW:
* Basé sur le module SX1231 exploitant l'interface SPI
* Packet radio, FSK à +20dBm max
* fonctionnalité d'auto-retransmission
* Envoi des données de 200 à 500 mètres avec un simple antenne filaire (et vue dégagée)
* Transmission jusqu'à 2km et même 5Km avec une antenne directionnel bien conçue (avec un vue parfaitement dégagée, une antenne ajustée et paramètres de transmissions adaptés)
* +13 à +20 dBm, avec capacité d'émission jusque 100 mW (puissance de sortie, configuration logicielle)
* Courant en transmission:
 * 50mA (+13 dBm)
 * 150mA (+20dBm)
* Courant en réception: ~30mA.
* Capable de créer un réseau multipoint avec adresse de noeud grâce au protocole RadioHead (entête de 4 octets)
* Transfert de 60 octets max par paquet de donnée.
* Moteur d'encryption de donnée avec AES-128
* Broches d'interruptions configurables (IRQ de G0 à G5)

Les exemples dans ce tutoriel s'appuie sur la version RFM69HCW 433 MHz.

## Distance de transmission

Une transmission à 500 mètres en vue dégagée (sans arbre, bâtiment) et avec une antenne directionnelle adaptée à la fréquence n'est pas un problème dans la configuration par défaut (à +13 dBm).

Souvenez vous qu'en fonction des éléments obstruant la vue en ligne droite (entre émetteur et récepteur), la fréquence et la puissance de sortie, il est tout à fait possible d'obtenir une distance de transmission inférieure.

Mais avec des paramètres choisi avec soin, un vue dégagée et une bonne antenne directionnelle (adaptée à la fréquence de transmission), il est aussi possible d'atteindre une distance de transmission de 2 Km et même de 5 km quand les conditions sont vraiment optimales.

# Bibliothèque

Cette bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les exemples.

Sur une plateforme connectée:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/rfm69")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/rfm69
```

# Brancher

## RFM69 vers un Raspberry-Pico

![RFM69 vers Raspberry-Pi Pico](docs/_static/rfm69-to-pico.jpg)

# Tester

Avant de pouvoir exécuter les scripts d'exemples, il sera nécessaire de copier la bibliothèque [rfm69.py](lib/rfm69.py) sur la carte MicroPython.

## test_config.py - vérifier les raccordements et le module

le script [test_config.py](examples/test_config.py) établit une connexion avec le module RFM69 via le bus SPI puis effectue différentes requêtes pour afficher la configuration du module.

Ce script est une méthode très pratique pour vérifier les raccordements entre le microcontrôleur et le module RFM..

```
RFM version     : 36
Freq            : 433.1
Freq. deviation : 250000.0 Hz
bitrate         : 250000.0 bits/sec
tx power        : 13 dBm
tx power        : 19.95262 mW
Temperature     : 23 Celsius
Sync on         : yes
Sync size       : 1
Sync Word Length: 2 (Sync size+1)
Sync Word       : bytearray(b'-\xd4')
crc on          : 1
Preamble Lenght : 4
aes on          : 1
Encryption Key  : bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08')
```

## test_simple.py - envoi de messages publiques (broadcast)

Un message broadcast est communiqué à tout venant (pas à un destinataire précis). Tous les autres modules RFM69 calés sur la même fréquence et avec la même clé d'encryption recevrons le message.

Le script [test_simple.py](examples/test_simple.py) envoi 10 fois le message "hello world!" puis écoute et affiche les messages entrant.

Il s'agit là du fonctionnement le plus simple du module RFM69 __et aussi fonctionnalité par défaut__ (rfm.destination = _RH_BROADCAST_ADDRESS).

Le fragment de code ci-dessous effectue l'envoi des messages:

``` python
from machine import SPI, Pin
from rfm69 import RFM69
import time

spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )

for i in range(10):
	# La chaîne de caractère (string) est transformé en tableau d'octets 'bytes' (données binaires)
	rfm.send(bytes("Hello world %i!\r\n" % i , "utf-8"))
	time.sleep(1)
```

Le fragment de code ci-dessous réceptionne les messages:

``` python
from machine import SPI, Pin
from rfm69 import RFM69
import time

spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = 433.1
rfm.encryption_key = ( b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )


print("Attente des paquets...")
while True:
	packet = rfm.receive()
	# packet = rfm.receive(timeout=5.0)
	if packet is None:
		print("Rien réceptionné! Ecouter encore...")
	else:
		print( "Réception (octets brutes):", packet )
```

__Pour utiliser correctement le script `test_simple.py` :__
* Il faut avoir un ensemble de 2 cartes RFM69+Pico assemblées et prêts à l'emploi.
* Démarrer le script `test_simple.py` sur une plateforme et attendre que le script passe en mode réception de messages.
* QUAND la première carte vérifie l'arrivée des messages ALORS démarrer le script sur la 2ième plateforme.
* Comme la seconde plateforme envoi immédiatement des messages, la première plateforme (en mode réception) affiche tous ces messages réceptionnés sur le module radio.

Voici les résultats obtenus:

Sur la première plateforme, nous attendons assez longtemps pour voir le message "Waiting for packets..." (en attente des paquets).

```
Temperature     : 23 Celsius
Freq            : 433.1
Freq. deviation : 250000.0 Hz
bitrate         : 250000.0 bits/sec
Sent hello world message 0!
Sent hello world message 1!
Sent hello world message 2!
Sent hello world message 3!
Sent hello world message 4!
Sent hello world message 5!
Sent hello world message 6!
Sent hello world message 7!
Sent hello world message 8!
Sent hello world message 9!
Waiting for packets...       <---- C'est le moment de démarrer le script sur la seconde plateforme
Received nothing! Listening again...
Received nothing! Listening again...
Received nothing! Listening again...
Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 3!\r\n')
Received (ASCII): Hello world 3!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 4!\r\n')
Received (ASCII): Hello world 4!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 5!\r\n')
Received (ASCII): Hello world 5!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 6!\r\n')
Received (ASCII): Hello world 6!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 7!\r\n')
Received (ASCII): Hello world 7!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 8!\r\n')
Received (ASCII): Hello world 8!

Received nothing! Listening again...
Received (raw bytes): bytearray(b'Hello world 9!\r\n')
Received (ASCII): Hello world 9!

Received nothing! Listening again...
Received nothing! Listening again...
Received nothing! Listening again...
Received nothing! Listening again...
Received nothing! Listening again...
```

Démarrer le script sur la seconde plateforme et celui-ci envoi directement les messages (a destination de la première plateforme).
```
Temperature     : 23 Celsius
Freq            : 433.1
Freq. deviation : 250000.0 Hz
bitrate         : 250000.0 bits/sec
Sent hello world message 0!     <--- sera réceptionné par la première plateforme
Sent hello world message 1!
Sent hello world message 2!
Sent hello world message 3!
Sent hello world message 4!
Sent hello world message 5!
Sent hello world message 6!
Sent hello world message 7!
Sent hello world message 8!
Sent hello world message 9!
Waiting for packets...
```

## test_ack_xxx.py - communication avec accusé de réception (acknowledgment)

Le script [test_ack_send.py](example/test_ack_send.py) envoi les messages "Send with ACK!" et demande un accusé de réception au destinataire.

Sur le récepteur, le script [test_ack_rec.py](example/test_ack_rec.py) est configuré pour recevoir les messages ET RENVOYER un message d'acquittement à l'expéditeur.

__La gestion des acquittement (ACK) ne peut pas être utilisé avec les message de type broadcast__. Les acquittement ACK ne sont jamais envoyés pour les message broadcast réceptionnés.

__Les ACKs (_acquittements_) fonctionne sur des plateformes condigurées comme NODEs (_noeuds_)__:
* Les Nodes (_noeuds_) doivent tous partager la même fréquence et même clé d'encryption.
* Chaque Node (_noeuds_) doit avoir une identification unique (de 0 à 254).
* Le message est envoyé vers un _noeud_ destinataire (`destination`) .
* Le Message est envoyé avec `send_with_ack()`. Le message sera renvoyé jusqu'à `ack_retries` fois (ou jusqu'à réception du ACK).
* `send_with_ack()` renvoi True lorsque le message a été acquité par le _noeud_ destinataire (`destination`).
* Le _noeud_ destinataire doit réceptionné les messages avec `receive( with_ack=True )`
* Le _noeud_ de destination ne réceptionnera que les messages suivants:
 * tous les messages broadcast (mais ne renvoi pas d'ACK)
 * tous les messages ayant le numéro de _noeud_ récepteur dans l'entête (renverra l'ACK à l'émetteur du message)

Voici les fragments de code de l'émetteur (SENDER) :

``` python
...
rfm = RFM69( spi=spi, nss=nss, reset=rst )
...
rfm.node    = 111 # Cette instance porte le no de noeud 111

# Envoyer un paquet au noeud 123 avec demande d'acquittement (ACK).
rfm.destination = 123
for i in range(10):
	print("Send with ACK %i!" % i)
	ack = rfm.send_with_ack(bytes("Send with ACK %i!\r\n" % i , "utf-8"))
	print("   +->", "ACK received" if ack else "ACK missing" )
	time.sleep(1)
```

Voici les fragments de code du récepteur (RECEIVER):

``` python
...
rfm = RFM69( spi=spi, nss=nss, reset=rst )
...
rfm.node = 123 # Cette instance porte le no de noeud 123

print("Waiting for packets...") # Attente des paquets
while True:
	packet = rfm.receive( with_ack=True )
	if packet is None:
		print("Received nothing! Listening again...") # Rien recu. Ecoute encore
	else:
		print( "Received (raw bytes):", packet )
```

## test_header_xxx.py - communication entre noeuds avec inspection de l'entête RadioHead

Le script [test_header_send.py](example/test_header_send.py) envoi les messages:
* vers le noeud destinataire
* avec un `identifier` personnalisés (8 bits, 1 octet) envoyé au destinataire dans l'entête radiohead.
* avec des `flags` personnalisés (4 bits) envoyé au destinataire dans l'entête radiohead.

Côté récepteur, le script [test_header_rec.py](example/test_header_rec.py) est configuré pour recevoir et afficher le contenu du message et le contenu de l'entête radiohead .

Voici le résultat obtenu sur le script du récepteur [test_header_rec.py](example/test_header_rec.py)

```
----------------------------------------
Received (RAW)   : bytearray(b'{o\x04\x0bSend message 64!')
destination node : 123  (Hey it is me!)
Sender node      : 111
Identifier       : 4 (a sequence number for reliable datagram)
Flags            : 11 0b1011
   _RH_FLAG_ACK  : no
   _RH_FLAG_RETRY: no
   user defined  : 0xb (lower 4 bits)
Received (ASCII) : Send message 64!
.
----------------------------------------
Received (RAW)   : bytearray(b'{o\x05\x0bSend message 65!')
destination node : 123  (Hey it is me!)
Sender node      : 111
Identifier       : 5 (a sequence number for reliable datagram)
Flags            : 11 0b1011
   _RH_FLAG_ACK  : no
   _RH_FLAG_RETRY: no
   user defined  : 0xb (lower 4 bits)
Received (ASCII) : Send message 65!
.
----------------------------------------
Received (RAW)   : bytearray(b'{o\x06\x0bSend message 66!')
destination node : 123  (Hey it is me!)
Sender node      : 111
Identifier       : 6 (a sequence number for reliable datagram)
Flags            : 11 0b1011
   _RH_FLAG_ACK  : no
   _RH_FLAG_RETRY: no
   user defined  : 0xb (lower 4 bits)
Received (ASCII) : Send message 66!
```

# A propos de l'encryption

Il est fortement recommandé d'activer l'encryption AES lorsque l'on envoi de paquet de données par radio.

La clé d'encryption AES est composée de 16 octets.

Les différents exemples utilisent une définiton de clé binaire que l'on peu décode comme étant `1234567812345678` .

``` python
...
rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.encryption_key = (  b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" )
```

Il est également possible de réécrire la clé sous comme suit afin d'être plus lisible:

 ``` python
 ...
 rfm = RFM69( spi=spi, nss=nss, reset=rst )
 rfm.encryption_key = bytes( [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8] )
 ```

# Liste d'achat
* [RFM69HCW Radio Transponder Breakout - 433 MHz - RadioFruit](https://shop.mchobby.be/product.php?id_product=1390) ADF-3071 @ MCHobby
* [RFM69HCW Radio Transponder Breakout - 433 MHz - RadioFruit](https://www.adafruit.com/product/3071) ADF-3071 @ Adafruit Industries
* [Raspberry-Pi Pico](https://shop.mchobby.be/fr/157-pico-rp2040) @ MCHobby

# Ressources
## Fiche technique
* [Semtech SX1231](https://df.mchobby.be/datasheet/RFM69W_HOPERF_datasheet.pdf)<br />(the underlying RF chip, which much of the RFM69 datasheet is lifted from)

## Versions antérieures
Cette version de la bibliothèque est basées sur les implémentations suivantes:

__rfm69-python by Arko:__<br />The [rfm69-python](https://github.com/arkorobotics/rfm69-micropython) portage original vers Micropython par Arko à EMFCAMP 2016 - Habville. A library to control HopeRF RFM69-series radio modules through SPI and GPIO. Conçue pour la carte MicroPython Pyboard.
Ecris pour être utilisé dans le projet [ukhas.net](http://ukhas.net) .

__Adafruit_CircuitPython_RFM69 par Adafruit Industries:__<br />That [ressources](https://github.com/adafruit/Adafruit_CircuitPython_RFM69)) qui s'est montré être une ressource essentielle pour adapter les fonctionnalités de  la version d'Arko.

La version rfm69-python d' Arko rapporte aux liens/ressources suivantes:
* [rfm69-python](https://github.com/russss/rfm69-python)
* [ukhasnet-rfm69](https://github.com/UKHASnet/ukhasnet-rfm69)
* [UKHASNetPiGateway](https://github.com/dbrooke/UKHASNetPiGateway) (en
  C/Wiring)
* [ukhasnet LPC810 node](https://github.com/jamescoxon/LPC810)
* [Python code for the beaglebone black](https://github.com/wcalvert/rfm69-python)
