# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# Advanced test with FBUtil class (FrameBuffer Utility)
# In this sample we will Use the FrameBuffer Utility to draw advanced shape
# like circle, ovale, filled circle, etc
#
from machine import SPI
from machine import Pin
from ili934x import *
from fbutil import FBUtil
import time

# PYBStick config requires Bit-Banging one-way SPI for Olimex.
# MISO (S26) of standard UEXT connector is used for D/C.
# SPI must declare a MISO! So we used a unused in the project (S16 in this case) as fake pin
# spi = SPI( -1, mosi=Pin("S19", Pin.OUT), miso=Pin("S16", Pin.IN), sck=Pin("S23", Pin.OUT) )
# cs_pin = Pin("S26")
# dc_pin = Pin("S21")
# rst_pin = None

# Raspberry-Pi Pico
spi = SPI( 0 )
cs_pin = Pin(5) # GP5
dc_pin = Pin(3) # GP3
rst_pin = None

# PICO config requires Bit-Banging one-way SPI for Olimex.
# MISO (GP4) of standard UEXT is used for D/C.
# SPI must declare a MISO! So we used a unused MISO pin in the project (GP0 in this case) as fake pin
# spi = SPI( 0, mosi=Pin(7, Pin.OUT), miso=Pin(16, Pin.IN), sck=Pin(6, Pin.OUT) )
# cs_pin = Pin(5) # GP5
# dc_pin = Pin(4) # GP4 (the miso pin)
# rst_pin = None


# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)
lcd.font_name = 'veram_m15'

util = FBUtil( lcd ) # LCD expose a FrameBuffer api

lcd.erase()
util.rrect( x=50, y=50, width=40, height=30, radius=5, color=WHITE )

util.rrect( x=50, y=100, width=80, height=40, radius=16, color=YELLOW )

util.fill_rrect( x=80, y=150, width=40, height=80, radius=9, color=BLUE )
