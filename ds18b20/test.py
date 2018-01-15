# Utilisation senseur température DS18B20 et ESP8266 MicroPython
#
# Shop: https://shop.mchobby.be/senseur-divers/259-senseur-temperature-ds12b20-extra-3232100002593.html
# Shop: https://shop.mchobby.be/senseur-divers/151-senseur-temperature-ds18b20-etanche-extra-3232100001510.html
#
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython
#
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep_ms

bus = OneWire( Pin(2) )
ds = DS18X20( bus )

# Scanner tous les périphériques sur le bus
# Chaque périphérique à une adresse spécifique
roms = ds.scan()
for rom in roms:
	print( rom )

# Interrogation des senseurs
ds.convert_temp()
# attendre OBLIGATOIREMENT 750ms 
sleep_ms( 750 )

# Lecture des température pour chaque périphérique
for rom in roms:
	temp_celsius = ds.read_temp(rom)
	print( "Temp: %s" % temp_celsius )
