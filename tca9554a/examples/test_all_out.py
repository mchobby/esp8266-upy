# Activate all the output on the TCA9554A
#
# See project repository and library at https://github.com/mchobby/esp8266-upy/tree/master/tca9554a
#
from machine import I2C, Pin
from tca9554a import TCA9554A
from time import sleep

# Pico, sda=GP6, scl=GP7
i2c = I2C(1)
tca = TCA9554A( i2c )

for i in range(8):
	tca.setup( i, Pin.OUT )

print( "All output ON" )
for i in range(8):
	tca.output( i, True )

sleep(2)

print( "All output OFF" )
for i in range(8):
	tca.output( i, False )

print( "That s all Folks!")
