"""
Test the SIRCS (Sony) IR Protocol writing with the mod IRDA+
=============================================================

Products:
---> https://shop.mchobby.be/fr/pico-rp2040/2037-interface-hat-pour-raspberry-pi-pico-3232100020375.html
---> https://www.olimex.com/Products/Modules/Interface/MOD-IRDA+/open-source-hardware

MCHobby investit du temps et des ressources pour écrire de la
                documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.
------------------------------------------------------------------------
History:
  06 july 2021 - Dominique - Creation. Working proprely
"""
from machine import I2C
from time import sleep, sleep_ms
from irdaplus import IrdaPlus, MODE_SIRC

# Pico sda=GP8, scl=GP9
i2c = I2C(0, freq=10000 ) # Slow down the bus to improve communication reliability

irda = IrdaPlus( i2c )
print( "SIRCS (SONY) IR Remote send command" )
print( "IRDA Module ID: %i" % irda.get_id() )

irda.set_mode( MODE_SIRC )

# Minimum pause time required for the IRDA+ module to send the command before
# being ready to read the I2C bus again. Below 30ms, multiple write will hang
# the bus.
SEND_PAUSE_MS = 30
print( "Send pause ms = %s" % SEND_PAUSE_MS )

# Send Vol+ to Sony TV
print( "Send Vol+" )
for i in range( 20 ):
    irda.send_command( device=1, cmd=18 ) # Maybe 16 on some Sony TV
    sleep_ms( SEND_PAUSE_MS )

sleep( 1 )

# Send Vol- to Sony TV
print( "send Vol-" )
for i in range( 20 ):
    irda.send_command( device=1, cmd=19 ) # Maybe 17 on some Sony TV
    sleep_ms( SEND_PAUSE_MS )
print( "Done!" )
