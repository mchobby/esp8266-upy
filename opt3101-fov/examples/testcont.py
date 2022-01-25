# Advanced test for the Pololu 3412
#    3-Channel Wide FOV Time-of-Flight Distance Sensor Using OPT3101
#
# Each channel is sampled approximately 41 times per second.
#
# This example shows how to read from all three channels on the OPT3101 and
# store the results in arrays.  It also shows how to use the sensor in a
# non-blocking way: instead of waiting for a sample to complete.
#
# --------------------------------------------------------------------
#   IN ADDITION TO THE USUAL POWER AND I2C CONNECTIONS, YOU WILL NEED
#   TO CONNECT THE **GP1** PIN TO AN INTERRUPT ON YOUR MICROCONTROLER.
# --------------------------------------------------------------------
#
# The sensor code runs quickly so that the main loop can take care of other
# tasks at the same time.
#
# See project repository and library at https://github.com/mchobby/esp8266-upy/tree/master/opt3101-fov
#
# History:
#   12/01/2022 - DMeurisse - Initial portage from Arduino code
#
from machine import I2C, Pin
from opt3101 import OPT3101, BRIGHTNESS_ADAPTIVE, CHANNEL_AUTO_SWITCH

import micropython
micropython.alloc_emergency_exception_buf(100)

# Some testing code for Pico
i2c = I2C(0)
# for PYBStick-RP2040
# i2c = I2C(0, sda=Pin(16), scl=Pin(17))

irqPin = Pin( 10, Pin.IN ) # Additional IRQ pin to be IRQed when data is ready

data_ready = False # global flag
def on_data_ready(p):
	global data_ready
	data_ready = True

# Attach irq handler
irqPin.irq( trigger=Pin.IRQ_RISING, handler=on_data_ready )

sensor = OPT3101( i2c )

amplitudes = list([0,0,0])
distances  = list([0,0,0]) # in mm

sensor.set_continuous_mode();
sensor.enable_data_ready_output( gpPin=1 )
sensor.set_frame_timing( 32 )
sensor.set_channel( CHANNEL_AUTO_SWITCH ) # Looping between channels automatically
sensor.set_brightness( BRIGHTNESS_ADAPTIVE )
sensor.enable_timing_generator( enabled=True )

# Main program loop
print( '           :     TX0 :     TX1 :     TX2' )
print( '-'*40 )
try:
	while True:
		if data_ready :
			data_ready = False
			sensor.read_output_regs() # Read data from board
			# stored into array
			amplitudes[sensor.channel_used] = sensor.amplitude
			distances[sensor.channel_used] = sensor.distance # in mm
			# Display data (or perform processing on the data)
			if sensor.channel_used == 2: # if we did read the 3 sensors
				print( 'Amplitudes : %7i : %7i : %7i' % (amplitudes[0], amplitudes[1], amplitudes[2]) )
				print( 'Distancess : %7i : %7i : %7i' % (distances[0], distances[1], distances[2]) )
				print( '-'*40 )


	# Perform other tasks here
except:
	# If program stopped, we disable the IRQ generator
	sensor.enable_timing_generator( enabled=True )
