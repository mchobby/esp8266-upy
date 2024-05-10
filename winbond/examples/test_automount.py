""" Winbond W25Q Flash with Micropython Pico - Typical mounting  at startup/boot

This consists of several steps. Not all of them have to be performed
everytime, see the comments of each command.

See https://github.com/mchobby/esp8266-upy/winbond

Sourced from:
  https://github.com/brainelectronics/micropython-winbond
"""

from machine import SPI, Pin
import os
from winbond import W25QFlash

spi = SPI(1, mosi=Pin.board.GP11, miso=Pin.board.GP12, sck=Pin.board.GP10, polarity=1, phase=1, baudrate=20000000 )
flash_cs = Pin( Pin.board.GP20, Pin.OUT, value=1 )

flash = W25QFlash(spi=spi, cs=flash_cs, software_reset=True)

flash_mount_point = '/flash'

try:
    os.mount(flash, flash_mount_point)
except Exception as e:
    if e.errno == 19:
        # [Errno 19] ENODEV aka "No such device"
        # create the filesystem, this takes some seconds (approx. 10 sec)
        print('Creating filesystem for external flash ...')
        print('This might take up to 10 seconds')
        os.VfsFat.mkfs(flash)
    else:
        # takes some seconds/minutes (approx. 40 sec for 128MBit/16MB)
        print('Formatting external flash ...')
        print('This might take up to 60 seconds')
        # !!! only required on the very first start (will remove everything)
        flash.format()

        # create the filesystem, this takes some seconds (approx. 10 sec)
        print('Creating filesystem for external flash ...')
        print('This might take up to 10 seconds')
        # !!! only required on first setup and after formatting
        os.VfsFat.mkfs(flash)

    print('Filesystem for external flash created')

    # finally mount the external flash
    os.mount(flash, flash_mount_point)
