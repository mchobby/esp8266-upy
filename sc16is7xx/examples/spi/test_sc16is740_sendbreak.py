""" sc16is740 over SPI demonstration with MicroPython 

    Test advanced UART function like txdone(), flush(), sendbreak(), deinit()

  The SC16IS740 a SPI/I2C to UART interface with 64 bytes FiFo.
  It offers only ONE UART.

* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import SPI, Pin
from sc16is7xx import SC16IS740
from sc16is7xx import *
import time

SPI_BAUDRATE = 4000000

# Bring up the SPI bus 
rst = Pin( Pin.board.GP16, Pin.OUT, value=True )
cs = Pin(Pin.board.GP9, Pin.OUT, value=True)
spi = SPI(1, mosi=Pin(Pin.board.GP11), miso=Pin(Pin.board.GP8, Pin.IN), sck=Pin(Pin.board.GP10), baudrate=SPI_BAUDRATE, firstbit=SPI.MSB, polarity=0, phase=0 )
# cs = Pin(Pin.board.GP5, Pin.OUT, value=True)
# spi = SPI(0, mosi=Pin(Pin.board.GP7), miso=Pin(Pin.board.GP4, Pin.IN), sck=Pin(Pin.board.GP6), baudrate=SPI_BAUDRATE, polarity=0, phase=0 )

# UART over SPI
uart_expander = SC16IS740( bus=spi, cs_pin=cs, rst_pin=rst )
# Grab the uart interface (act as machine.UART)
ser1 = uart_expander.uart( 1, baudrate=1200, bits=8, parity=None, stop=1 )


print( "--- Sending bytes ---")
msg = "Shall I compare thee to a summer’s day? Thou art more lovely" # 60 bytes
print( "SENDING: %s" % msg)
print( "" )
ser1.write( msg.encode('ascii') ) # This will takes 500ms 


print( "wait 200ms..." )
time.sleep_ms(200)

# =============================================
#
#   sendbreak()
#
# =============================================

# sendbreak() send a break condition on the serial line.
#    Breaktime must be at minumum the time for data bits + stop bits + parity bit + 1 start bit.
#    Break time_ms can also be given in parameter.

print( "--- SendBreak ---")
ser1.sendbreak( time_ms=100 ) # Force break of 100ms to see it on the scope

