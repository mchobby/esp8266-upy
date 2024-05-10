""" Test Winbond W25Q Flash with Micropython Pico

Get information about the attached W25Q Winbond flash attached

See https://github.com/mchobby/esp8266-upy/winbond

Sourced from:
  https://github.com/brainelectronics/micropython-winbond
"""

from machine import SPI, Pin
import os
import winbond

# highest possible baudrate is 40 MHz for ESP-12
# SPI must have phase=1, polarity=1
spi = SPI(1, mosi=Pin.board.GP11, miso=Pin.board.GP12, sck=Pin.board.GP10, baudrate=20000000 )
flash_cs = Pin( Pin.board.GP20, Pin.OUT, value=1 )

flash = winbond.W25QFlash(spi=spi, cs=flash_cs, software_reset=True)
print( "Capacity   : %i Bytes" % flash.capacity )

# JEDEC Manufacturer ID for Winbond is 0xEF = Winbond Serial Flash
print( "Manufact.ID: %s" % hex(flash.manufacturer) )
if flash.manufacturer == 0xEF:
	print( "  +-> Winbond Serial Flash" )

# Supported mem_types are [0x40, 0x60, 0x70] only the 0x40 have been tested
print( "Mem type   : %s" % hex(flash.mem_type) )

# Identify the chip used

#  W25Q64FW         -> ??  0x6017
#  W25Q32BV AIG     -> ??  4016h
#  W25Q16JV-IQ/JQ   -> 14h 4015h
#  W25Q16JV-IM*/JM* -> 14h 7015h
print( "Device type: %s" % hex(flash.device) )

print( "SECTOR SIZE: %s" % flash.SECTOR_SIZE )
print( "BLOCK  SIZE: %s" % flash.BLOCK_SIZE )
print( "PAGE   SIZE: %s" % flash.PAGE_SIZE )
