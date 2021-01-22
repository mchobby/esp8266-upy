""" Perform a very basic test of the motor M1 for the Motor FeatherWing"""
from machine import I2C
from motorwing import MotorWing
from motorbase import FORWARD, BACKWARD, BRAKE, RELEASE
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
# i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# Raspberry-Pi Pico - SDA=GP8, SCL=GP9
i2c = I2C(0)

# Test the various motors on the MotorShield
sh = MotorWing( i2c )
motor = sh.get_motor(1) # Motor M1
try:
	motor.speed( 128 ) # Initial speed configuration
	motor.run( FORWARD )
	# Wait the user to stop the script
	# by Pressing Ctrl+C
	while True:
		sleep( 1 )
except KeyboardInterrupt:
	motor.run( RELEASE )

print( "That's all folks")
