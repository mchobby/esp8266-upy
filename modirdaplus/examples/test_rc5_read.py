"""
Test the RC5 (Philips) IR Protocol reading with the mod IRDA+
=============================================================

Products:
---> https://shop.mchobby.be/fr/pico-rp2040/2037-interface-hat-pour-raspberry-pi-pico-3232100020375.html
---> https://www.olimex.com/Products/Modules/Interface/MOD-IRDA+/open-source-hardware

MCHobby investit du temps et des ressources pour écrire de la
                documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.
------------------------------------------------------------------------
History:
  06 july 2021 - Dominique - ported from Read_RC5.ino (but not tested)
"""
from machine import I2C
from time import sleep_ms
from irdaplus import IrdaPlus, MODE_RC5

# Pico sda=GP8, scl=GP9
i2c = I2C(0, freq=10000 ) # Slow down the bus to improve communication reliability

irda = IrdaPlus( i2c )
irda.set_mode( MODE_RC5 ) # default is SIRCS

print( "RC5 (PHILIPS) IR Remote decoder" )
print( "Module ID: %i" % irda.get_id() )
while True:
    #  --- Decode the Command & target_device address
    decoded = irda.read_command()
    if decoded:
        print( 'device %i, command %i, toggle %s' % decoded )
    sleep_ms( 300 )
