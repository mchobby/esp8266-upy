""" test_imu.py - Just load the library and read imu data

See project source @ https://github.com/mchobby/esp8266-upy/imu-a

14 Apr 2024 - domeu - initial writing
"""
from machine import I2C, Pin
from imu_a import IMU_A # 9DoF Imu based on LSM6DS33 + LIS3MDL
import time


i2c = I2C(0, sda=Pin.board.GP8, scl=Pin.board.GP9 )
print( "I2C scan:", i2c.scan() )

imu = IMU_A( i2c )

while True:
	imu.read()
	print( "Acc= %6i, %6i, %6i  :  Mag= %6i, %6i, %6i  :  Gyro= %6i, %6i, %6i  " % (imu.a.values+imu.m.values+imu.g.values) )
	time.sleep( 0.5 )
