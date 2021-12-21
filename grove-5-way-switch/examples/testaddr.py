"""
Grove 5 Way Switch - Change I2C address of module

See https://github.com/mchobby/esp8266-upy/tree/master/grove-5-way-switch

"""
from machine import I2C
from grove5way import Grove5Way

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=400000)

# Open at default address 0x03
sw = Grove5Way( i2c, address=0x03 )
print( 'versions    :', sw.device_version() ) # return the 10 bytes of version
print( 'version     :', sw.version )
print( 'Switch Count:', sw.switch_count )
print( '' )
print( 'Change from default address 0x03' )
print( 'To address 0x04' )

# Unlock protection is required to change address. Place under command to avoids
#    unexpected result.
# sw.unlock()
sw.change_address( 0x04 )
print( 'Changed!')
print( '' )

print( 'Power cycle the module.')
print( 'The module can now be used at address 0x04')
