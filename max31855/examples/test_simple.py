# Read the temperature from Type-K Thermocouple + MAX31855 amplifiers
#
# See project: https://github.com/mchobby/esp8266-upy/tree/master/max31855
#
from machine import Pin, SPI
from max31855 import MAX31855
import time

# Pico - SPI(0) - GP5=CSn, GP4=Miso, GP6=Sck, GP7=Mosi (allocated but not used)
cs = Pin(5, Pin.OUT, value=True ) # SPI CSn
spi = SPI(0, baudrate=5000000, polarity=0, phase=0)

tmc = MAX31855( spi=spi, cs_pin= cs )

while True:
	print( "Temp: %s" % tmc.temperature() )
	time.sleep( 1 )
