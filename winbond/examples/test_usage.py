""" Test Winbond W25Q Flash with Micropython Pico

This test consists of several steps. Not all of them have to be performed
everytime, see the comments of each command.

The flash object is created on SPI2 with a SPI speed of 2MHz, CS on machine
pin 5 and a software reset interface. Check the datasheet of your flash chip.

As a next step a full erase of the complete flash is performed, this is only
required once. If this function is called after something has been stored on
the flash, its content will be permanently lost.
A filesystem will be established with the flash. This step is also only
required once (after a formatting process).

The last step before the flash can be used productively is to mount it at the
desired location. In this case a directory named '/flash' is used.

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

# !!! only required on the very first start (will remove everything)
# takes some seconds/minutes!
flash.format()

# !!! only required on first setup and after formatting takes some seconds to minutes
# Please note that os.VfsLfs2.mkfs(flash) doesn't work
os.VfsFat.mkfs(flash)

# mount the external flash to /flash folder
os.mount(flash, '/flash')

# show all files and folders on the boards root directory
print(os.listdir('/'))
# ['flash', 'boot.py', 'main.py', 'winbond.py']

# save a file named 'some-file.txt' to the external flash or extend it
with open('/flash/some-file.txt', 'a+') as file:
    file.write('Hello World')

# unmount flash
os.umount('/flash')

# show all files and folders on the boards root directory
# the "flash" folder won't be shown anymore
print(os.listdir('/'))
# ['boot.py', 'main.py', 'winbond.py']

# mount the external flash again
os.mount(flash, '/flash')

# show all files and folders on the external flash
os.listdir('/flash')
# ['some-file.txt']

# read back the file from the external flash
with open('/flash/some-file.txt', 'r') as file:
    print(file.readlines())
