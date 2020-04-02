""" Demonstrate how to use PWM output on PCA9685 """
from machine import I2C
from pca9685 import PCA9685
from time import sleep

i2c = I2C( 2 )
pca = PCA9685( i2c, freq=1200 ) # PWM frequency
# Set the output 8 @ 50% duty cycle (half of 4095)
pca.duty( 8, 2048 )
sleep( 1 )

# Set the output 8 @ 25% duty cycle (quarter of 4095)
pca.duty( 8, 1024 )
sleep( 1 )

# duty sycle can also be controled with duty_percent()
# set duty cycle @ 33% on output 8
pca.duty_percent( 8, 33 )
