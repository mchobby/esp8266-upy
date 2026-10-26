""" sc16is750 over SPI demonstration with MicroPython 

    Using SC16IS750 and congigure its GPIO 0 as OUTPUT.
    Then a while loop update the GPIO 0 ouput state every second.

  The SC16IS750/760 a SPI/I2C to UART interface with 64 bytes FiFo.
  It offers ONE UART and 8x GPIOs

* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import SPI, Pin
from sc16is7xx import SC16IS750
from sc16is7xx import *
import time

SPI_BAUDRATE = 4000000

# Bring up the SPI bus 
rst = Pin( Pin.board.GP16, Pin.OUT, value=True )
cs = Pin(Pin.board.GP9, Pin.OUT, value=True)
spi = SPI(1, mosi=Pin(Pin.board.GP11), miso=Pin(Pin.board.GP8, Pin.IN), sck=Pin(Pin.board.GP10), baudrate=SPI_BAUDRATE, firstbit=SPI.MSB, polarity=0, phase=0 )

# UART over SPI
uart_expander = SC16IS750( bus=spi, cs_pin=cs, rst_pin=rst, oscillator_hz=3072000 )
# Grab the uart interface (act as machine.UART)
ser1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1 )
# Grab the GPIO pin (act as machine.Pin)
p0 = uart_expander.pin( 0, Pin.OUT )

for i in range(20):
    p0.value( i%2 )
    # Following line demonstrate that output 
    # Pin can have its state read back
    print( "current value", p0.value() )
    time.sleep( 1 )


