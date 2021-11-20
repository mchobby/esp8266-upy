"""
Test the MicroPython driver for M5Stack U087, Vmeter Unit, I2C grove.

READ DIFF INPUT WITH HACKED VMETER MODULE
See https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u087

Just make a read of the voltage on the differential input directly wired to the
terminal block.

* Author(s):
   19 nov 2021: Meurisse D. (shop.mchobby.be) - Initial Writing
"""

from machine import I2C
from vmeter import *
from time import sleep

# Pico - I2C(1) - sda=GP8, scl=GP9
i2c = I2C(1, freq=10000)
# M5Stack core
# i2c = I2C( sda=Pin(21), scl=Pin(22) )

vmeter = Voltmeter(i2c, ads1115_addr=0x4b, eeprom_addr=0x51 ) # Addr-->Scl
while True:
	# read ADC voltage (in millivolts)
	print( 'ADC Voltage: %5.3f mV' % vmeter.adc_mv )
	sleep( 0.3 )
