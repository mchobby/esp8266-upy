"""
Test the SIRCS (Sony) IR Protocol reading with the mod IRDA+
=============================================================

Products:
---> https://shop.mchobby.be/fr/pico-rp2040/2037-interface-hat-pour-raspberry-pi-pico-3232100020375.html
---> https://www.olimex.com/Products/Modules/Interface/MOD-IRDA+/open-source-hardware

MCHobby investit du temps et des ressources pour écrire de la
                documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.
------------------------------------------------------------------------
History:
  06 july 2021 - Dominique - Creation
"""
from machine import I2C
from time import sleep_ms
from irdaplus import IrdaPlus, MODE_SIRC

# Pico sda=GP8, scl=GP9
i2c = I2C(0, freq=10000 ) # Slow down the bus to improve communication reliability

irda = IrdaPlus( i2c )
print( "SIRCS (SONY) IR Remote decoder" )
print( "IRDA Module ID: %i" % irda.get_id() )

irda.set_mode( MODE_SIRC )
while True:
    # return raw data
    # print( irda.read_data() )
    decoded = irda.read_command()
    if decoded:
        print( 'device %i, command %i' % decoded )
    sleep_ms( 300 )
