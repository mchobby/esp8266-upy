""" Test all stepper port on the MotorShield.
    The S1 = M1+M2 port and S2 = M3+M4 """
from machine import I2C
from motorshield import MotorShield
from motorbase import FORWARD, BACKWARD, SINGLE, DOUBLE, INTERLEAVE, MICROSTEP
from motorbase import MICROSTEPS
from time import sleep

def test_stepper( sh, motor_nr ):
	""" Test the various DCMotor functionnalities """
	stepper = sh.get_stepper( 200, motor_nr )
	stepper.speed = 3
	print( ' +-> SINGLE coil activation for full turn (energy saving)' )
	stepper.step( 200, dir=FORWARD, style=SINGLE )
	sleep( 2 )
	print( ' +-> DOUBLE coil activation for full turn (stronger torque)' )
	stepper.step( 200, dir=BACKWARD, style=DOUBLE )
	sleep( 2 )
	# Interleave is more precise... requires twice much steps.
	# Will only move a Half turn.
	print( ' +-> INTERLEAVE for half turn (more precise)' )
	stepper.step( 200, dir=FORWARD, style=INTERLEAVE )
	sleep(2)
	# Go back in the original position with MicroSteppings (a half turn)
	print( ' +-> MICROSTEP 1/%s for half turn' % MICROSTEPS )
	stepper.step( 100*MICROSTEPS, dir=BACKWARD, style=MICROSTEP )
	sleep(2)
	print( ' +-> RELEASE motor ')
	stepper.release()

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Test the various Steppers on the MotorShield
sh = MotorShield( i2c )
for stepper_nr in (1,2):
	print( "Stepper S%s" % stepper_nr )
	test_stepper( sh, stepper_nr )
