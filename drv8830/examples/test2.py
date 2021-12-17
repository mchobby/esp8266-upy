"""
DRV8830 - Control the 2 motors of Mini I2C Motor driver (SeeedStudio)

See https://github.com/mchobby/esp8266-upy/tree/master/drv8830

"""
from machine import I2C
from drv8830mot import DRV8830
import time

# Pico - I2C(0), sda=IO8, scl=IO9
i2c = I2C(0, freq=100000)

# Motor driver
mot1 = DRV8830( i2c, address=0x65 ) # Chanel 1
mot2 = DRV8830( i2c, address=0x60 ) # Chanel 2
print( 'Move forward full speed' )
mot1.drive( 63 )
mot2.drive( 63 )
time.sleep( 2 )
print( 'Stop' )
mot1.stop()
mot2.stop()
time.sleep( 1 )
print( 'Move backward Half speed' )
mot1.drive( -32 )
mot2.drive( -32 )
time.sleep( 2 )
print( 'Brake motors' )
mot1.brake()
mot2.brake()
time.sleep( 1 )
print( 'Stop motors' )
mot1.stop()
mot2.stop()
print( 'Thats all folks' )
