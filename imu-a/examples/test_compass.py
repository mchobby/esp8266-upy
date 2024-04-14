""" test_compass.py - Just load the IMU and Compass to read North position

See project source @ https://github.com/mchobby/esp8266-upy/imu-a

14 Apr 2024 - domeu - initial writing
"""
from machine import I2C, Pin
from imu_a import IMU_A
from compass import Compass
import time


i2c = I2C(0, sda=Pin.board.GP8, scl=Pin.board.GP9 )
print( "I2C scan:", i2c.scan() )

imu = IMU_A( i2c ) # Start with auto detection
compass = Compass( imu, samples=120 )

print("Starting calibration...")
print("   rotate it on himself to find compass min and max")
compass.calibrate()
print("calibration done")
print( 'Compass min: %s ' % compass.min )
print( 'Compass max: %s ' % compass.max )

while True:
	heading = compass.average_heading()
	print( 'Heading %s degrees' % heading )
	time.sleep( 0.5 )
