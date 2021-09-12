"""
Test the MicroPython driver for M5Stack U087, Vmeter Unit, I2C grove.

DO NOT EXCEED 16V on the input (because of the ADC gain change)

Mimic the example at https://github.com/m5stack/M5-ProductExampleCodes/blob/master/Unit/V_Meter_Unit/voltmeter/voltmeter.ino

* Author(s):
   08 july 2021: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from vmeter import *
from time import sleep

# Pico - I2C(1) - sda=GP6, scl=GP7
i2c = I2C(1, freq=10000)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

vmeter = Voltmeter(i2c)

# Default configuration @ init
# vmeter.set_gain( PAG_2048 )
# vmeter.set_rate( RATE_128 )
# vmeter.set_mode( SINGLESHOT )

# The order is critical
vmeter.set_gain( PAG_512 ) # ADC Full Scale Range = 512mv, ADC Resolution = 15.625µV
vmeter.set_rate( RATE_8 )
vmeter.set_mode( SINGLESHOT )


print( 'M5Stack - U087 - Voltmeter' )
print( '--------------------------' )
print( '' )
print( 'Max voltage : +/- %i V (depends on ADC gain)' % vmeter.max_voltage )
print( 'Resolution  : %6.5f v/unit' % vmeter.resolution )
print( 'Sample rate : %i SPS' % vmeter.sample_rate )

print( 'Voltage     : %.3f mV' % vmeter.get_voltage(calibration=False) )
print( 'Voltage     : %.3f mV (calibrated)' % vmeter.get_voltage() )
print( 'Raw ADC     : %i' % vmeter.adc_raw )
