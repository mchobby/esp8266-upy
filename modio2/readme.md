# Use an Olimex MOD-IO2 with ESP8266 under MicroPython

# MOD-IO2
MOD-IO2 est une carte d'interface d'Olimex utilisant le port UEXT. 

![La carte MOD-IO2](mod-io2.png)

Cette carte expose.
* 2 Relais 
* 7 GPIOs reconfigurables - 3.3V max
** 5 entrées analogiques (résolution 10 bits)
** 2 sorties PWM (100 KHz, résolution 8 bits)
* Prévu pour être chainâble
* Interface I2C (adresse 0x21 par défault)
* Addresse modifiable (stockée en EEProm)
* Alimentation: 12VDC max

__Où acheter__
* Shop: [UEXT Expandable Input/Output board (MOD-IO2)](http://shop.mchobby.be/product.php?id_product=1409)
* Shop: [Module WiFi ESP8266 - carte d'évaluation (ESP8266-EVB)](http://shop.mchobby.be/product.php?id_product=668)
* Shop: [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412)
* Shop: [Câble console](http://shop.mchobby.be/product.php?id_product=144)
* Wiki: not defined yet 

## Details de la carte

![Raccordements](mod-io2-details.png)

# ESP8266-EVB sous MicroPython
Avant de se lancer dans l'utilisation du module MOD-IO sous MicroPython, il faudra flasher votre ESP8266 en MicroPython.

Nous vous recommandons la lecture du tutoriel [ESP8266-EVB](https://wiki.mchobby.be/index.php?title=ESP8266-DEV) sur le wiki de MCHobby.

Ce dernier explique [comment flasher votre carte ESP8266 avec un câble console](https://wiki.mchobby.be/index.php?title=ESP8266-DEV).

## Port UEXT

Sur la carte ESP8266-EVB, le port UEXT transport le port série, bus SPI et bus I2C. La correspondance avec les GPIO de l'ESP8266 sont les suivantes.

![Raccordements](ESP8266-EVB-UEXT.jpg)

# MOD-IO2 Raccordement

Pour commencer, j'utilise un [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412) pour dupliquer le port UEXT. J'ai en effet besoin de raccorder à la fois le câble console pour communiquer avec l'ESP8266 en REPL __et__ raccorder le module MOD-IO.

![Raccordements](ESP8266-EVB-UEXT-SERIAL.jpg)

J'ai ensuite effectuer les raccordements suivant sur la carte MOD-IO2:

![Raccordements](mod-io2-wiring-low.png)

# Code de test

## Bibliothèque modio2

Avant d'utiliser le script d'exemple, il est nécessaire de transférer la __bibliothèque modio2__ sur votre carte micropython.
* Copiez le fichier `modio2.py` sur la carte micropython.

Vous pouvez également transférer le script de test `test2.py`  sur la carte PyBoard. 

La bibliothèque offre les fonctionalités suivantes

__Membres:__
* `carte.relais[index] = True` : (indexed property) Fixe l'état du relais.
* `v = carte.relais[index]`    : (indexed property) Retourne l'état du relais.
* `carte.relais`          : (property) Retourne l'état de tous les relais.
* `carte.relais = True`   : (property) Change l'état de tous les relais (accepte également une liste de 4 entrées).
* `carte.gpios.pin_modes` : (property) Retourne une liste avec le pin_mode IN/OUT de chaque GPIO.
* `carte.gpios.status`    : (property) retourne une liste avec les niveaux logiques True/False pour les broches IN/OUT (pas fiable pour broches PWM, Analogique).

__Methodes:__
* `carte.change_address( 0x22 )` : méthode qui change l'adresse I2C de la carte MOD-IO sur le bus. Fixe la nouvelle adresse à 0x22 (à la place de la valeur par défault 0x58). __Le bouton "BUT" doit être maintenu enfoncé pendant l'envoi de la commande!
* `carte.gpios.pin_mode( gpio, pinmode, pull_up=None )` : Define a GPIO as Pin.IN/Pin.OUT, allow to activate a Pin.PULL_UP resistor.
* `carte.gpios.analog( gpio, raw = False )` : Lit une entrée analogique en volts sur un GPIO. Raw retourne une valeur 10 Bit (0 à 1023).
* `carte.gpios.pwm( gpio, cycle )` : Active le generateur PWM sur une broche et assigne la valeur 8 bits du cycle utile (0 à 255).
* `carte.gpios.pwm_close( gpio )` : Cloture la fonctionnalité PWM (transforme la broche en entrée). 

## Exemple avec MOD-IO2
```
# Utilisation du MOD-IO2 d'Olimex avec un ESP8266 sous MicroPython
#
# Shop: [UEXT Expandable Input/Output board (MOD-IO2)](http://shop.mchobby.be/product.php?id_product=1409)
# Wiki: not defined yet

from machine import I2C, Pin
from time import sleep_ms
from modio2 import MODIO2

i2c = I2C( sda=Pin(2), scl=Pin(4) )
brd = MODIO2( i2c ) # default address=0x21

# === Manipulate GPIO =============================
print( "Pin_modes")
print( brd.gpios.pin_modes )

print( "GPIO 5 - Analog read")
brd.gpios.pin_mode( 5, Pin.IN )
for i in range(10):
    volt = brd.gpios.analog(5)
    print( "AN7 = %s v" % volt )
    val  = brd.gpios.analog(5, raw=True )
    print( "AN7 = %s / 1023" % val )
    sleep_ms( 1000 )

# GPIO 0 - OUT
print( "GPIO 0 - OUT (On then Off)" )
brd.gpios.pin_mode( 0, Pin.OUT )
brd.gpios[0] = True
sleep_ms( 2000 )
brd.gpios[0] = False

print( "GPIO 1,2,3 - IN" )
brd.gpios.pin_mode( 1, Pin.IN )
brd.gpios.pin_mode( 2, Pin.IN )
brd.gpios.pin_mode( 3, Pin.IN, Pin.PULL_UP ) # pull up mandatory on Pin 3
print( "Pin_modes")
print( brd.gpios.pin_modes )
print( "All inputs state (1/0)" )
print( brd.gpios.states )

# === RELAIS ======================================
# Set REL1 and REL2 to ON (Python is 0 indexed)
print( 'Set relay by index' )
brd.relais[0] = True
brd.relais[1] = False
print( 'Relais[0..1] states : %s' % brd.relais.states ) 
sleep_ms( 2000 )
# switch all off
brd.relais.states = False 

print( 'one relay at the time')
for irelay in range( 2 ):
    print( '   relay %s' % (irelay+1) )
    brd.relais[irelay] = True # Switch on the relay
    sleep_ms( 1000 )
    brd.relais[irelay] = False # Switch OFF the relay
    sleep_ms( 500 )

print( 'Update all relais at once' )
brd.relais.states = [False, True]
sleep_ms( 2000 )
print( 'Switch ON all relais' )
brd.relais.states = True
sleep_ms( 2000 )
print( 'Switch OFF all relais' )
brd.relais.states = False

print( "That's the end folks")
```

Ce qui produit le résultat suivant :

```
MicroPython v1.9.4-8-ga9a3caad0 on 2018-05-11; ESP module with ESP8266
Type "help()" for more information.
>>> import test2
Pin_modes
['IN', 'IN', 'IN', 'IN', 'IN', 'IN', 'IN']
GPIO 5 - Analog read
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
AN7 = 1.86452 v
AN7 = 578 / 1023
GPIO 0 - OUT (On then Off)
GPIO 1,2,3 - IN
Pin_modes
['OUT', 'IN', 'IN', 'IN', 'IN', 'IN', 'IN']
All inputs state (1/0)
36
[False, False, True, False, False, True, False]
Set relay by index
Relais[0..1] states : [True, False]
one relay at the time
   relay 1
   relay 2
Update all relais at once
Switch ON all relais
Switch OFF all relais
That's the end folks
>>>
```
## Exemple PWM avec MOD-IO2
Contenu de l'exemple disponible dans le fichier `test2pwm.py`.

PWM est uniquement disponible sur les GPIO GPIO 5 & 6.

Dans l'exemple ci-dessous, une lecture analogique est réalisée sur le GPIO 5 (lecture en RAW).

Fixer le cycle utile PWM du GPIO 6 (0 à 255) avec la valeur analogique du GPIO 5 (0 à 1024) qui sera divisée par 4.


```
# Test PWM sur le MOD-IO2 d'Olimex avec un ESP8266 sous MicroPython
#
# Shop: [UEXT Expandable Input/Output board (MOD-IO2)](http://shop.mchobby.be/product.php?id_product=1409)
# Wiki: not defined yet



# Changer l'adresse I2C de la carte MOD-IO

L'exemple suivant montre comment changer l'adresse courante de la carte MOD-IO (0x58) vers 0x22.

ATTENTION: Il faut maintenir le bouton BUT enfoncé pendant l'exécution de la commande `change_address()` .

```
# Modifier l'adresse de MOD-IO2 d'Olimex vers 0x22
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

