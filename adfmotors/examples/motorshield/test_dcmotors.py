""" Test the 4 DC motor ports, One at the time, with the various features """
from machine import I2C
from motorshield import MotorShield
from motorbase import FORWARD, BACKWARD, BRAKE, RELEASE
from time import sleep

def test_motor( motor_obj ):
	""" Test the various DCMotor functionnalities """
	motor_obj.speed( 128 ) # Initial speed configuration
	print( "Foward")
	motor_obj.run( FORWARD )
	sleep( 3 )
	print( "Backward")
	motor_obj.run( BACKWARD )
	sleep( 3 )
	print( "Brake")
	motor_obj.run( BRAKE )
	sleep( 3 )
	print( "Accelerate" )
	# Warning: Setting speed to 0 will stop motor! New speed() followed by run()
	#          are required to restart motor rotation.
	motor_obj.speed( 1 )
	motor_obj.run( FORWARD )
	for speed in range( 1, 256 ): # 1 to 255
		motor_obj.speed( speed )
		sleep( 0.050 )
	print( "Decelerate" )
	for speed in range( 255, 0, -1 ): # 255 to 1
		motor_obj.speed( speed )
		sleep( 0.050 )
	print( "Speed 128")
	motor_obj.speed( 128 )
	sleep(2)
	print( "RELEASE" )
	motor_obj.run( RELEASE )

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Test the various motors on the MotorShield
sh = MotorShield( i2c )
for motor_nr in (1,2,3,4):
	print( "Motor M%s" % motor_nr )
	motor = sh.get_motor(motor_nr)
	test_motor( motor )
