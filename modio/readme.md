# Use an Olimex MOD-IO and MOD-IO2 with ESP8266 under MicroPython

## MOD-IO

MOD-IO est une carte d'interface d'Olimex utilisant le port UEXT. Cette carte expose.
* 4 relais,
* 4 entrée digitale opto isolée (compatible avec le 24V industriel)
* 4 entrée analogiques (0 - 3.3V)
* Prévu pour être chainâble
* Interface I2C (adresse 0x58 par défault)
* Addresse modifiable (stockée en EEProm)
* Alimentation: 8-30VDC

__Où acheter__
* Shop: [UEXT Expandable Input/Output board (MOD-IO)](http://shop.mchobby.be/product.php?id_product=1408)
* Shop: [Module WiFi ESP8266 - carte d'évaluation (ESP8266-EVB)](http://shop.mchobby.be/product.php?id_product=1408)
* Shop: [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412)
* Shop: [Câble console](http://shop.mchobby.be/product.php?id_product=144)
* Wiki: not defined yet 

# ESP8266-EVB sous MicroPython
Avant de se lancer dans l'utilisation du module MOD-IO sous MicroPython, il faudra flasher votre ESP8266 en MicroPython.

Nous vous recommandons la lecture du tutoriel [ESP8266-EVB](https://wiki.mchobby.be/index.php?title=ESP8266-DEV) sur le wiki de MCHobby.

Ce dernier explique [comment flasher votre carte ESP8266 avec un câble console](https://wiki.mchobby.be/index.php?title=ESP8266-DEV).

## Port UEXT

Sur la carte ESP8266-EVB, le port UEXT transport le port série, bus SPI et bus I2C. La correspondance avec les GPIO de l'ESP8266 sont les suivantes.

![Raccordements](ESP8266-EVB-UEXT.jpg)

# Raccordement

## MOD-IO 
Pour commencer, j'utilise un [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412) pour dupliquer le port UEXT. J'ai en effet besoin de raccorder à la fois le câble console pour communiquer avec l'ESP8266 en REPL __et__ raccorder le module MOD-IO.

![Raccordements](ESP8266-EVB-UEXT-SERIAL.jpg)

J'ai ensuite effectuer les raccordements suivant sur la carte MOD-IO:

![Raccordements](mod-io-wiring-low.jpg)

* L'opto-coupleur IN3 est activé à l'aide d'une tension de 16V (choisi arbitrairement entre 5 et 24V DC)
* Un potentiomètre de 10K est branché sur l'entrée analogique 2 (AIN-2) avec une tension fixée à 1.129v
* Les relais 1 et 3 (sur les 4 relais à disposition) sont activés.

# Code de test

## MOD-IO
```
# Utilisation du MOD-IO d'Olimex avec un ESP8266 sous MicroPython
#
# Shop: http://shop.mchobby.be/product.php?id_product=1408
# Wiki: not defined yet


from machine import I2C, Pin
from time import sleep_ms
from modio import MODIO

i2c = I2C( sda=Pin(2), scl=Pin(4) )
brd = MODIO( i2c ) # default address=0x58

# === Read Analog Input ===========================
for irelay in range( 4 ):
    print( 'Analog %s : %s Volts' %( irelay,brd.analog(irelay) ) ) 

for irelay in range( 4 ):
    print( 'Analog %s : %s of 1023' %( irelay,brd.analog(irelay, raw=True) ) ) 

# === OptoIsolated Input ==========================
print( 'Read all OptoIsolated input' )
print( brd.inputs() )
print( 'Read OptoIsolated input #3' )
print( brd.input(2) )

# === RELAIS ======================================
# Set REL1 and REL3 to ON (Python is 0 indexed)
brd[0] = True
brd[2] = True
print( 'Relais[0..3] states : %s' % brd.relais ) 
sleep_ms( 2000 )

print( 'one relay at the time')
for irelay in range( 4 ):
    print( '   relay %s' % (irelay+1) )
    brd[irelay] = True # Switch on the relay
    sleep_ms( 1000 )
    brd[irelay] = False # Switch OFF the relay
    sleep_ms( 500 )

print( 'Update all relais at once' )
brd.relais = [True, True, False, True]
sleep_ms( 2000 )
print( 'Switch ON all relais' )
brd.relais = True
sleep_ms( 2000 )
print( 'Switch OFF all relais' )
brd.relais = False
```

# Changer l'adresse I2C de la carte MOD-IO

L'exemple suivant montre comment changer l'adresse courante de la carte MOD-IO (0x58) vers 0x22.

ATTENTION: Il faut maintenir le bouton BUT enfoncé pendant l'exécution de la commande `change_address()` .

```
# Modifier l'adresse de MOD-IO d'Olimex vers 0x22
#
# Shop: http://shop.mchobby.be/product.php?id_product=1408

from machine import I2C, Pin
from modio import MODIO

i2c = I2C( sda=Pin(2), scl=Pin(4) )
brd = MODIO( i2c, addr=0x58 )
brd.change_address( 0x22 )
```

Etant donné que le changement d'adresse est immédiat, la carte produira un ACK sous l'adresse 0x22 alors que la commande est émise sous l'adresse 0x58.
Par conséquent, la réponse ne sera jamais reçue (comme attendue) par le microcontroleur. Il en résulte le message d'erreur `OSError: [Errno 110] ETIMEDOUT` (tout à fait normal dans cette circonstance).

Un `i2c.scan()` permet de confirmer le changement d'adresse.

