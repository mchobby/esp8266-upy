# Basic demo for accelerometer/gyro readings from ISM330DHCX
#
# Based on Adafruit Implementation for Arduino
# https://github.com/adafruit/Adafruit_LSM6DS/blob/master/examples/adafruit_ism330dhcx_test/adafruit_ism330dhcx_test.ino

from machine import Pin, I2C
from ism330dh import ISM330DHCX
from lsm6ds import * # constant

# Pico I2C(1) onn GP6 & GP7
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
ism = ISM330DHCX( i2c )

accel = ism.accel_sensor
gyro = ism.gyro_sensor
temp = ism.temp_sensor

#=== Grab Sensor Setting ===

# ism.set_accel_range(LSM6DS_ACCEL_RANGE_2_G)
print("Accelerometer range set to: ")
value = ism.get_accel_range()
if value==LSM6DS_ACCEL_RANGE_2_G:
	print("\t+-2G")
elif value==LSM6DS_ACCEL_RANGE_4_G:
	print("\t+-4G")
elif value==LSM6DS_ACCEL_RANGE_8_G:
	print("\t+-8G")
elif value==LSM6DS_ACCEL_RANGE_16_G:
	print("\t+-16G")
else:
	print("\tUndefined")


print("Gyroscope range set to: ")
value = ism.get_gyro_range()  
if value==LSM6DS_GYRO_RANGE_125_DPS:
	print("\t125 degrees/s");
elif value==LSM6DS_GYRO_RANGE_250_DPS:
	print("\t250 degrees/s");
elif value==LSM6DS_GYRO_RANGE_500_DPS:
	print("\t500 degrees/s");
elif value==LSM6DS_GYRO_RANGE_1000_DPS:
	print("\t1000 degrees/s");
elif value==LSM6DS_GYRO_RANGE_2000_DPS:
	print("\t2000 degrees/s");
elif value==ISM330DHCX_GYRO_RANGE_4000_DPS:
	print("\t4000 degrees/s");
else:
	print( "\tUndefined" )



# ism.set_accel_datarate(LSM6DS_RATE_12_5_HZ)
print("Accelerometer data rate set to: ");
value = ism.get_accel_datarate()
if value==LSM6DS_RATE_SHUTDOWN:
	print("\t0 Hz")
elif value==LSM6DS_RATE_12_5_HZ:
	print("\t12.5 Hz")
elif value==LSM6DS_RATE_26_HZ:
	print("\t26 Hz")
elif value==LSM6DS_RATE_52_HZ:
	print("\t52 Hz")
elif value==LSM6DS_RATE_104_HZ:
	print("\t104 Hz")
elif value==LSM6DS_RATE_208_HZ:
	print("\t208 Hz")
elif value==LSM6DS_RATE_416_HZ:
	print("\t416 Hz")
elif value==LSM6DS_RATE_833_HZ:
	print("\t833 Hz")
elif value==LSM6DS_RATE_1_66K_HZ:
	print("\t1.66 KHz")
elif value==LSM6DS_RATE_3_33K_HZ:
	print("\t3.33 KHz")
elif value==LSM6DS_RATE_6_66K_HZ:
	print("\t6.66 KHz")
else:
	print("\tUndefined")


# ism330dhcx.set_gyro_datarate(LSM6DS_RATE_12_5_HZ)
print("Gyro data rate set to: ")
value = ism.get_gyro_datarate()
if value==LSM6DS_RATE_SHUTDOWN:
	print("\t0 Hz")
elif value==LSM6DS_RATE_12_5_HZ:
	print("\t12.5 Hz")
elif value==LSM6DS_RATE_26_HZ:
	print("\t26 Hz")
elif value==LSM6DS_RATE_52_HZ:
	print("\t52 Hz")
elif value==LSM6DS_RATE_104_HZ:
	print("\t104 Hz")
elif value==LSM6DS_RATE_208_HZ:
	print("\t208 Hz")
elif value==LSM6DS_RATE_416_HZ:
	print("\t416 Hz")
elif value==LSM6DS_RATE_833_HZ:
	print("833 Hz")
elif value==LSM6DS_RATE_1_66K_HZ:
	print("1.66 KHz")
elif value==LSM6DS_RATE_3_33K_HZ:
	println("3.33 KHz")
elif value==LSM6DS_RATE_6_66K_HZ:
	print("6.66 KHz")
else:
	print("\tUndefine")


ism.config_int1(False, False, True) # accelerometer DRDY on INT1
ism.config_int2(False, True, False) # gyro DRDY on INT2

accel = SensorEvent()
gyro  = SensorEvent()
temp  = SensorEvent()
while True:
	ism.get_event( accel, gyro, temp)

	print("Temperature %s deg C" % temp.temperature )

	# Display the results (acceleration is measured in m/s^2) 
	print("Accel X: %s \tY: %s \tZ: %s m/s^2" % (accel.acceleration.x, accel.acceleration.y, accel.acceleration.z) )

	# Display the results (rotation is measured in rad/s)
	print("Gyro X: %s \tY: %s \tZ: %s radians/s" % (gyro.gyro.x, gyro.gyro.y, gyro.gyro.z) )
	time.sleep_ms(100)
