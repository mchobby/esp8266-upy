# Using the DS18B20 temperature sensor with Pyboard, Pico & ESP8266 under MicroPython
#
# Shop: https://shop.mchobby.be/senseur-divers/259-senseur-temperature-ds12b20-extra-3232100002593.html
# Shop: https://shop.mchobby.be/senseur-divers/151-senseur-temperature-ds18b20-etanche-extra-3232100001510.html
#
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep_ms

# PyBoard
bus = OneWire( Pin("Y3") )
# ESP8266
# bus = OneWire( Pin(2) )
# Pico
# bus = OneWire( Pin(2) )

ds = DS18X20( bus )

# Scan all the DS12B20 on the bus (for each of the ROM address).
# Each of the device do have a specific address
roms = ds.scan()
for rom in roms:
	print( rom )

# Request temps from sensors
ds.convert_temp()
# Waits for 750ms (required)
sleep_ms( 750 )

# Display the temp for each device
for rom in roms:
	temp_celsius = ds.read_temp(rom)
	print( "Temp: %s Celcius" % temp_celsius )
