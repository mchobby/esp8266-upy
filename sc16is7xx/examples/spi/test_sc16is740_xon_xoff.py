""" SC16IS740 over SPI demonstration with MicroPython 

    Test UART auto-xon-xoff software flow control.
    The SC16IS7xx allow to define XON1/XOFF1 chars, and also XON2/XOFF2 .
    The SC16IS7xx can work with any of XON1, XON2, "XON1 or XON2" and 
       also "XON1 followed by XON2".
    ------------------------------------------------------------------
    This script allows to spy XON/XOFF flow control by using two 
    SC16IS740 board then executing the one board as SENDER (IS_SENDER=True)
    and the other board as RECEIVER (IS_SENDER=False).
    ------------------------------------------------------------------

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

# Script act as SENDER or RECEIVER
#
#  IS_SENDER=True : the script will flood the line until 
#                   the software flow control suspend it.
#
#  IS_SENDER=False: the script will act as a slow receiver
#                   poping off byte slow enough for the
#                   software flow to take place.
#
IS_SENDER = True

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
#   Activate SOFTWARE Flow Control
#
# =============================================

# Define the standard single charater xon/xoff
ser1.define_xon_xoff( xon=0x11, xoff=0x13 ) # Ctrl+Q & Ctrl+S

# Define a dual characters xon/xoff
# ser1.define_xon_xoff( xon=0x11, xoff=0x13, xon=0x12, xoff=0x14 ) 

# Note: 
#   Trigger values are used for RX FIFO management.
#   When RX FIFO reach the HALT_TRIGGER the XOFF is emitted on TX.
#   When RX FIFO falls to the RESUME_TRIGGER the XON is emitted on TX.
#   When RX receive XOFF, TX FIFO halt transmitting data.
#   When RX Receive XON, TX FIFO resume transmission.
#   Trigger values are required (even when no Workflow is setup on RX).
ser1.auto_xon_xoff( halt_trigger=56, resume_trigger=12, flow_rx=XON1_XOFF1, flow_tx=XON1_XOFF1 )

# Possible values for flow control are the followings
# -------------------------------+-------------------------------+--------------
#  TX                            | RX                            | Description
# -------------------------------+-------------------------------+--------------
#  NO_WORKFLOW or None           |                               | no flow control on TX.
#  XON1_XOFF1                    |                               | TX only send XON1, same for XOFF.
#  XON2_XOFF2                    |                               | TX only send XON2, same for XOFF.
#  XON1_AND_XON2_XOFF1_AND_XOFF2 |                               | TX send XON1 followed by XON2, Same for XOFF.
# -------------------------------+-------------------------------+--------------
#                                | NO_WORKFLOW or None           | no flow control on RX.
#                                | XON1_XOFF1                    | RX sensitive to XON1 & XOFF1.
#                                | XON2_XOFF2                    | RX sensitive to XON2 & XOFF2.
# -------------------------------+-------------------------------+--------------
#  XON1_XOFF1                    | XON1_OR_XON2_XOFF1_OR_XOFF2   | TX only send XON1/XOFF1. RX sensitive to XON1 or XON2 (same for XOFF)
#  XON2_XOFF2                    | XON1_OR_XON2_XOFF1_OR_XOFF2   | TX only send XON2/XOFF2. RX sensitive to XON1 or XON2 (same for XOFF)
#  XON1_AND_XON2_XOFF1_AND_XOFF2 | XON1_AND_XON2_XOFF1_AND_XOFF2 | TX send XON1 followed by XON2. RX expected XON1 followed by XON2 (same for XOFF)
#  NO_WORKFLOW or None           | XON1_AND_XON2_XOFF1_AND_XOFF2 | no flow control on TX. RX expected XON1 followed by XON2 (same for XOFF)
# -------------------------------+-------------------------------+--------------


# =============================================
#
#   Sending Data
#
# =============================================

try:
    if IS_SENDER:
        print( "--- Sending bytes ---")
        counter = 0
        while True:
            msg = "%i-msg" % counter # somes bytes + counter
            print( "SENDING: %s  TX FIFO LEVEL: %s" % (msg, ser1.any_tx()) ) 
            ser1.write( msg.encode('ascii') )
            # make ramdom reads
            counter += 1
    else:
        print( "--- Receiving bytes ---")
        buf = bytearray( 4 )
        while True:
            ser1.readinto( buf )
            print( "RECEIVING; %s  RX FIFO LEVEL: %s" % (buf, ser1.any()) )
            time.sleep_ms(10)

except KeyboardInterrupt:
    print("User abort")

