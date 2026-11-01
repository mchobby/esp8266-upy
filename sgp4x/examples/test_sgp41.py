""" SGP41 over I2C demonstration with MicroPython 

  The SGP41 is an I2C Air Quality sensor measuring VoC and NOx

* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sgp4x

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import I2C, Pin
from sgp41 import SGP41
import time

# I2C bus on RaspberryPi Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )

# Sensor
sgp = SGP41( i2c, address=0x59 )

sn = sgp.serial_number
print('Serial Number:', sn )

print('Self test...')
sgp.self_test()
print('passed!')

rh_default = 50 # Relative Humidity = 50%
t_default = 25  # temperature = 25 C

try:
  # During conditionning, only VoC reading available
  # Conditionning for 10 sec MAX (otherwise it may degrade sensor)
  start_ms = time.ticks_ms()
  while time.ticks_diff(time.ticks_ms(), start_ms) < 10_000 :
    raw_voc = sgp.conditioning( rh_default, t_default )
    print( 'raw voc:', raw_voc )
    time.sleep_ms(500)
    
  # Start Voc & NOx reading (which stop conditionning)
  while True:
    # we can obtain better NOx compensation when providing real data for rh & t.
    raw_voc, raw_nox = sgp.measure_raw( rh_default, t_default )
    print( 'raw voc:', raw_voc, 'raw NOx:', raw_nox )
    time.sleep_ms(1000)
finally:
  # Go to Idle mode (be sure the conditionning is halted)
  print( 'Turn Heater Off' )
  sgp.heater_off()


