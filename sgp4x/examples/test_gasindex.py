""" SGP41 over I2C demonstration with MicroPython 

  The SGP41 is an I2C Air Quality sensor measuring VoC and NOx

* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sgp4x

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import I2C, Pin
from sgp41 import SGP41
from gasindex import VocGasIndex, NoxGasIndex
import time

# I2C bus on RaspberryPi Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )

# Sensor
sht = None # tp perform measurement of %RC & T
sgp = SGP41( i2c, address=0x59 )

voc_calc = VocIndexAlgorithm()
nox_calc = NoxIndexAlgorithm()

print('SGP Self test...')
sgp.self_test()
print('passed!')

print( "VOC Gas Index Algorithm parameters" )
for k,v in voc_index.get_tuning_parameters():
  print( "  %s : %s" % (k,v) )
print( "NOx Gas Index Algorithm parameters" )
for k,v in nox_index.get_tuning_parameters():
  print( "  %s : %s" % (k,v) )


rh_default = 50 # Relative Humidity = 50%
t_default = 25  # temperature = 25 C
conditioning_sec = 10 # Number of seconds of conditionning
while True:

  # Variable declaration
  #   humidity = 0.0     # %RH
  #   temperature = 0.0  # degreeC
  raw_voc = 0
  raw_nox = 0

  # Value used for compensation when reading SGP41
  rh = 0 
  t  = 0 

  # 1. Sleep: Measure every second (1Hz), as defined by the Gas Index
  time.sleep_ms( 1000 )

  # 2. Measure temperature and humidity for SGP internal compensation
  if sht != None:
    # sht4x.measureHighPrecision(temperature, humidity)
    t, rh = sht.measure()
  else:
    t = t_default
    rh = rh_default 
  # Compensation parameter must be integer
  t = int(t)
  rh = int(rh)
  print( 'Temperature : %i C' % t )
  print( 'Humidity    : %i RH' % rh )


  # 3. Measure SGP4x signals
  if conditioning_sec > 0:
    # During NOx conditioning (10s) RAW NOx will remain 0
    raw_voc = sgp.conditioning( rh, t )
    conditioning_sec -= 1 
  else:
    raw_voc, raw_nox = sgp.measure_raw( rh, t )
  
  
  # 4. Process raw signals by Gas Index Algorithm to get the VOC and NOx
  #    index values  
  voc_index = voc_calc.process( raw_voc )
  nox_index = nox_calc.process( raw_nox )
  
  print( "VoC Index:", voc_index )
  print( "NOx Index:", nox_index )

