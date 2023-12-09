from machine import I2C
from ledseg4 import LedSegment4
from time import sleep

# Raspberry-Pi Pico
i2c = I2C(1, freq=100000 ) # sda=GP6, scl=GP7
dis = LedSegment4( i2c ) # DFR0645 4 digit LED display

dis.print("halo") # immediate return
sleep(2)
dis.print("Pr") # immediate return
sleep(2)
dis.print("Micropython is great!") # scroll the text.
sleep(2)
dis.print("amigos") # scroll the text.
# Switch display off
# dis.off()
