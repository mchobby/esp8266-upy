from motorbase import MotorBase

# Channels of the PCA9685 that are driving the motor ports M1, M2, M3 and M4
# Pin configuration on the PCA9685
MOTORSHIELD_PCA_CONFIG = {
	'motors' : {
		1: {'pwm':8,  'in1':10,  'in2': 9}, # Motor 1
		2: {'pwm':13, 'in1':11, 'in2': 12}, # Motor 2
		3: {'pwm':2,  'in1':4,  'in2': 3},  # Motor 3
		4: {'pwm':7,  'in1':5,  'in2': 6}   # Motor 4
	},
	# Motor ports used for each of the two possible stepper motors
	'steppers' : {
		# Stepper 1 with Coil A & Coil B
		1 : { 'a': {'pwm':8,  'in1':10, 'in2': 9},
			  'b': {'pwm':13, 'in1':11, 'in2': 12}  },
		# Stepper 2 with Coil A & Coil B
		2 : { 'a': {'pwm':2,  'in1':4,  'in2': 3} ,
			  'b': {'pwm':7,  'in1':5,  'in2': 6}  }
	}
}

class MotorShield( MotorBase ):
	""" Managing the MotorShield implementation on various boards """

	def __init__( self, i2c, address=0x60, freq=500 ):
		""" :param freq: 24Hz to 1526Hz """
		# pca_config contains the PCA pin definition depending on the MotorShield/Wing implementation.
		super().__init__( MOTORSHIELD_PCA_CONFIG, i2c, address, freq )
