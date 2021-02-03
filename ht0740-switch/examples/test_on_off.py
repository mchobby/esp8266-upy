# Cycle the activation of the HT0740 Breakout
#
# See project repository and library at https://github.com/mchobby/esp8266-upy/tree/master/ht0740-switch
#
from machine import I2C
from ht0740 import HT0740
from time import sleep

# Pico, sda=GP6, scl=GP7
i2c = I2C(1)
# Pyboard, sda=X10, scl=X9
# i2c = I2C(1)

power = HT0740( i2c )

power.on()
sleep(2)
power.off()
sleep(2)
power.output( True )
sleep(2)
power.output( False )
print( "That s all Folks!")
