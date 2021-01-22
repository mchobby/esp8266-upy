""" Test a Servo motor wired to the #15 PWM output (MotorShield ONLY) """
from machine import I2C
from motorshield import MotorShield
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# Raspberry-Pi Pico - SDA=GP8, SCL=GP9
# i2c = I2C(0)

# Test the various motors on the MotorShield
# The servo are working best @ 50 Hz PWM, the default 500 Hz PWM is too HIGH
# for most of the servo available on the market. Depending on the servo motor
# electronic, a freq between 100 and 300 Hertz can also be used.
sh = MotorShield( i2c, freq=50 )

# Bring a servo on the available #15,#14,#1 or #0 breakout pins
SERVO_NR = 15
print( "Acquire servo %s" % SERVO_NR )
servo = sh.get_servo( SERVO_NR )

print("Set at 90 degrees")
servo.angle( 90 )
sleep( 2 )
print("Set at 0 degrees")
servo.angle( 0 )
sleep( 2 )
print("Set at 180 degrees")
servo.angle( 180 )
sleep( 2 )
print("Set at 90 degrees")
servo.angle( 90 )
sleep( 2 )

print("Release servo")
servo.release()
print( "That's all folks")
