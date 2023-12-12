from machine import I2C
from ledseg8 import LedSegment8
from time import sleep

# Raspberry-Pi Pico
i2c = I2C(1) # sda=GP6, scl=GP7
dis = LedSegment8( i2c ) # DFR0646 8 digit LED display

dis.print("halo") # immediate return
sleep(2)
dis.print("14FE") # immediate return
sleep(2)
dis.print("Micropython is great!") # scroll the text.
sleep(2)
dis.print("amigos") # no scroll.
# Switch display off
# dis.off()
