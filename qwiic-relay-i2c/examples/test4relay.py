""" test4relay.py - test the Qwiic Multi Relay I2C module

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Quad Relay      : https://www.sparkfun.com/products/16566
---> Qwiic Dual State Relay: https://www.sparkfun.com/products/16810
---> Qwiic Quad State Relay: https://www.sparkfun.com/products/16833
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

Remark: Have not been tested yet (I don't have testing board.)
------------------------------------------------------------------------

History:
  14 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from machine import I2C, Pin
from relayi2c import MultiRelay, QUAD_DEFAULT_ADDRESS, QUAD_SSR_DEFAULT_ADDRESS, DUAL_SSR_DEFAULT_ADDRESS
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

# Can be used with one of the following depending on Qwiic product in use
#   QUAD_DEFAULT_ADDRESS (4 relais), QUAD_SSR_DEFAULT_ADDRESS, DUAL_SSR_DEFAULT_ADDRESS

rel = MultiRelay( i2c, address=QUAD_DEFAULT_ADDRESS )
print( 'version:', rel.version )

print('--- On/Off --------------')
for relay in range( 4 ): # 0..3
	rel.on(relay+1)      # 1..4
	print( "Relay %i is %s" % (relay+1, rel.state(relay+1)) )
	time.sleep( 2 )

for relay in range( 4 ): # 0..3
	rel.off(relay+1)      # 1..4
	print( "Relay %i is %s" % (relay+1, rel.state(relay+1)) )
	time.sleep( 2 )

print('--- Toggle --------------')
for relay in range( 4 ): # 0..3
	print( "Relay %i is %s" % (relay+1, rel.state(relay+1)) )
	print( "Toggling" )
	rel.toggle(relay+1) # 1..4
	print( "Relay %i is %s" % (relay+1, rel.state(relay+1)) )
	time.sleep( 2 )

print('--- update all at once---')
print( "All off" )
rel.off_all()
time.sleep(2)
print( "All on" )
rel.on_all()
time.sleep(2)
print( "All off" )
rel.off_all()
time.sleep(2)

print('--- Value ---------------')
# Value() method does mimic the Pin class behaviour
rel.value( 2, True )
rel.value( 3, True )
rel.value( 4, True )
time.sleep(2)
rel.value( 2, False )

for relay in range( 4 ): # 0..3
	print( "Relay %i is %s" % (relay+1, rel.value(relay+1) ) )
time.sleep(2)

print('--- Slow PWM ---------------')
# Value() method does mimic the Pin class behaviour
rel.off_all()
rel.slow_pwm( 2, 50 ) # relay 2, duty cycle @ 50% (value 0..100)
print( "Relay 2 at %i Duty Cycle PWM" % rel.slow_pwm(2) )
