""" Test a PWM output (with a LED) wired to the #0 PWM output """
from machine import I2C
from motorshield import MotorShield
from time import sleep

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

# Test the various motors on the MotorShield
# The servo are working best @ 50 Hz PWM, the default 500 Hz PWM is too HIGH
# for most of the servo available on the market. Depending on the servo motor
# electronic, a freq between 100 and 300 Hertz can also be used.
sh = MotorShield( i2c )

# Bring a servo on the available #15,#14,#1 or #0 breakout pins
PWM_NR = 0
print( "Acquire PWM %s" % PWM_NR )
pwm = sh.get_pwm( PWM_NR )

print("Signal HIGH")
pwm.duty_percent( 100 )
sleep( 2 )
print("Signal LOW")
pwm.duty_percent( 0 )
sleep( 2 )
print("Duty cycle @ 50%")
pwm.duty_percent( 50 )
sleep( 2 )
# Duty cycle can be finely tuned with a value between 0 (LOW) and 4095 (HIGH)
print("Duty cycle (0-4095) @ 2866 (so 70%)")
pwm.duty( 2866 )
sleep( 2 )

print("Release PWM")
pwm.duty( 0 ) # or duty_percent( 0 )
print( "That's all folks")
