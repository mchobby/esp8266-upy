# This example is sourced from micropython forum
# see: https://forum.micropython.org/viewtopic.php?t=3003
#
from machine import Pin, SPI
import time

# Pico - SPI(0) - GP5=CSn, GP4=Miso, GP6=Sck, GP7=Mosi (allocated but not used)
cs = Pin(5, Pin.OUT, value=True ) # SPI CSn
spi = SPI(0, baudrate=5000000, polarity=0, phase=0)
# MOSI has to be defined BUT is not needed to read data


def read_temp(cs, spi):
    while True:
        try:
            data = bytearray(4)
            cs.value(0)
            spi.readinto(data)
            cs.value(1)
            print(data)
            temp = data[0] << 8 | data[1]
            if temp & 0x0001:
                return float('NaN')
            temp >>= 2
            if temp & 0x2000:
                temp -= 16384
            print(temp * 0.25)
        except:
            pass
        time.sleep(1)

read_temp(cs, spi)
