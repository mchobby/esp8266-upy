""" Vishay VCNL4035 sensor for MicroPython

    Test the interrupt setting with proximity reading
    Connect the "int" pin to GPIO 0 (on RPI Pico)

    *** THIS CODE HANDLE THE INTERRUPT FROM USER SCRIPT ***

    This example will toggle the user led each time the VCNL activate the interrupt.
    The main loop continuously display the current proximity reading.

* Source   : https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

Remarks:
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000 
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import I2C, Pin
from vcnl4035 import VCNL4035
from vcnldefs import VCNL4035_MODES, VCNL4035_PS_IT
import time, micropython

micropython.alloc_emergency_exception_buf(100)

# Adapt thresold depending on your conditions (see your readings)
# Note that Intgration time could also be chaned for higher values
THRESOLD_LOW = 100
THRESOLD_HIGH= 600

led=Pin(25, Pin.OUT, value=False)
int_count=0 # allow main loop to detect IRQ arrival

# === Attach an ISR to the GP0 ===
def vcnl_int( pin ):
	global int_count
	int_count += 1
	print( "int" )

int_pin = Pin( 0, Pin.IN, Pin.PULL_UP )
int_pin.irq( vcnl_int, trigger=Pin.IRQ_FALLING ) # Add  hard=True for quicker reaction

# === Sensor ===
i2c = I2C(1, sda=Pin(6), scl=Pin(7) )
sensor = VCNL4035( i2c=i2c, mode=VCNL4035_MODES.PROXIMITY )
# Default integration time, the value can reach 1_500 to 2_500. This should be enough
# Higher integration time, the value can reach and exceed 32_000.
#
# sensor.set_ps_integration_time( VCNL4035_PS_IT.PS_IT_400us )


# Set the low and high threshold values for the interrupt
sensor.prox_int_thres_low ( THRESOLD_LOW  )
sensor.prox_int_thres_high( THRESOLD_HIGH )


# === Main Loop ===
print( "VCLN4035 version", sensor.version )

last_int_count = int_count
sensor.read_int_flags() # reset last potential interrupt
while True:
	# Interrupt detected
	if int_count!=last_int_count:
		last_int_count = int_count
		led.toggle()
		print( "Interrupt detected" )
		# Read interrupt flag on VCNL (Sets VCNL INT pin back to high)
		sensor.read_int_flags()

	data = sensor.read_data() # return 3 values from gesture sensor
	# Data[0] is the IRED1 led (the top one) in range 0..65535
	print( data[0] )
	time.sleep_ms(10)
