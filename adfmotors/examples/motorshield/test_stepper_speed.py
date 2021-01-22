""" Change the speed of a stepper motor on S1 (M1+M2).
	Test speed from 0 to 100 RPM.

	WARNING:
	I2C communication is not taken into account for calculating wait time
	between steps. For higher speed I2C communication time will create a
	buttleneck and time between steps should be reduced to compensate ii
	properly.

 	"""
from machine import I2C
from motorshield import MotorShield
from motorbase import FORWARD, BACKWARD, SINGLE, DOUBLE
from pyb import ADC

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# Raspberry-Pi Pico - SDA=GP8, SCL=GP9
# i2c = I2C(0)

def arduino_map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

adc = ADC('X19')
# Test the various speed for a stepper on the MotorShield
sh = MotorShield( i2c )
stepper = sh.get_stepper( 200, 1 )
while True:
	val = adc.read() # Value between 0 et 4095
	rpm = arduino_map( val, 0, 4095, 1, 100 )
	print( "%s RPM" % rpm )
	stepper.speed = rpm
	stepper.step( 40, dir=FORWARD, style=DOUBLE )
