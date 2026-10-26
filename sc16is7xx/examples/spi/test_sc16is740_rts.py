""" sc16is740 over SPI demonstration with MicroPython 

    Test UART auto-RTS output signal

    - Set TX --> RX  loopback
    - wire scope to TX
    - Wire scope to RTS

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
ser1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1 )

# =============================================
#
#   Activate Flow Control
#
# =============================================

# RTS (Ready To Send) is an output pin
#   It inform the remote when data can be send (HIGH=send, LOW=halt).
#   RTS goes LOW when Receive FIFO reach the "halt_trigger", the
#     remote must halt transmission.
#   RTS goes HIGH when Receive FIFO falls to the "resume_trigger" and
#     stays below the "halt_trigger". The remote can send data.
# 
ser1.auto_rts( halt_trigger=56, resume_trigger=12 )

# =============================================
#
#   Sending Data
#
# =============================================

print( "--- Sending bytes ---")
try:
    counter = 0
    while True:
        msg = "%i-msg" % counter # somes bytes + counter
        print( "SENDING: %s  RX FIFO LEVEL: %s" % (msg, ser1.any()) ) 
        ser1.write( msg.encode('ascii') )

        # make ramdom reads
        counter += 1
        time.sleep_ms(200)

except KeyboardInterrupt:
    print("User abort")

