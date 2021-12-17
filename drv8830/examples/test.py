"""
DRV8830 - Control the Channel 2 of Mini I2C Motor driver (SeeedStudio)

See https://github.com/mchobby/esp8266-upy/tree/master/drv8830

"""
from machine import I2C
from drv8830mot import DRV8830
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=100000)

# Motor driver
mot2 = DRV8830( i2c, address=0x60 )
print( 'Move forward full speed' )
mot2.drive( 63 )
print( '  fault:', mot2.fault )
time.sleep( 2 )
print( 'Move backward full speed' )
mot2.drive( -63 )
print( '  fault:', mot2.fault )
time.sleep( 2 )
print( 'Stopping motor' )
mot2.stop()
print( '  fault:', mot2.fault )
