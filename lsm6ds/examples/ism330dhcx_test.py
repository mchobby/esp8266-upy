from machine import I2C, Pin
from ism330dh import *

# Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )

ism = ISM330DHCX( i2c )
accel = ism.accel_sensor
gyro = ism.gyro_sensor
temp = ism.temp_sensor

# Grab information on Sensor Type
accel.print_sensor_details()
gyro.print_sensor_details()
temp.print_sensor_details()
