""" sc16is740 over SPI demonstration with MicroPython 

  The SC16IS740 a SPI/I2C to UART interface with 64 bytes FiFo.
  It offers only ONE UART.

  Attach a GPS-ULTIMATE on the SC16IS740 UART.
  This example use the UART.readline() to acquire the data


* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import SPI, Pin
from sc16is7xx import SC16IS740
from sc16is7xx import *
import time
from machine import idle

SPI_BAUDRATE = 4000000

# Bring up the SPI bus 
rst = Pin( Pin.board.GP16, Pin.OUT, value=True )
cs = Pin(Pin.board.GP9, Pin.OUT, value=True)
spi = SPI(1, mosi=Pin(Pin.board.GP11), miso=Pin(Pin.board.GP8, Pin.IN), sck=Pin(Pin.board.GP10), baudrate=SPI_BAUDRATE, firstbit=SPI.MSB, polarity=0, phase=0 )
# Alternate wiring:
#   cs = Pin(Pin.board.GP5, Pin.OUT, value=True)
#   spi = SPI(0, mosi=Pin(Pin.board.GP7), miso=Pin(Pin.board.GP4, Pin.IN), sck=Pin(Pin.board.GP6), baudrate=SPI_BAUDRATE, polarity=0, phase=0 )

# UART over SPI 
#   rst_pin      : (optional) toggle SC16IS7xx reset if used.
#   oscillator_hz: (optional) SC16IS7xx clock if not 1.8432 MHz crystal
#   bus          : initialized bus object (either SPI, either I2C)
#   cs_pin       : chip select pin object (REQUIRED with SPI bus)
#   address      : I2C address (REQUIRED with I2C bus)
#   timeout      : read timeout (default 1000 ms). See https://docs.micropython.org/en/latest/library/machine.UART.html
#   timeout_char : character timeout after first char (default 100 ms). See https://docs.micropython.org/en/latest/library/machine.UART.html
#
uart_expander = SC16IS740( bus=spi, cs_pin=cs, rst_pin=rst ) # another osc: oscillator_hz=14_745_600 

# Grab the uart interface (act as machine.UART)
#
#   baudrate : (required) Calculated from oscillator_hz (default clock at 1843200 Hz, see SC16IS740 constructor)
#   bits     : 5,6,7,8 bits (8 by default)
#   parity   : None, 0=Even, 1=Odd, 10=Forced_0, 11=Forced_1
#   stop     : 1, 1.5, 2 stop bits (1.5 stop bit only works for 5 bit data length)
#
#   timeout  : wait up to 1500ms to get a complete line with readline
#
ser1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500 ) 

# =============================================
#
#   READLINE
#
# =============================================

while True:
	arr = ser1.readline()
	if arr==None:
		print('.')
		idle
		continue
	print( arr ) # display the bytearray
	print( arr.decode('ascii') ) # Display as string
