""" sc16is750 over SPI demonstration with MicroPython 

    Using SC16IS750 configure to get IRQ on RX FiFo Level & TX FiFo Level
       configure it to generates an IRQ when GPIO state change.
    Connect TX --> RX.
    IRQ pin must be Pull-up to 3V3 with a 1K resistor.
    IRQ is connected to Pico GP22
    IRQ will go LOW when state changes and will resets on state read.

    Then configure IRQ line the script reads the IRQ Source.    

  The SC16IS750/760 a SPI/I2C to UART interface with 64 bytes FiFo.
  It offers ONE UART and 8x GPIOs

* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import SPI, Pin, idle
from sc16is7xx import SC16IS750
from sc16is7xx import *
import time

# time between RX/TX fifo status print
# Use 0 to disable.
DELAY_MS = 500
SPI_BAUDRATE = 4000000

IRQ_SOURCE_LABEL = { CTS_RTS_IRQ:"CTS_RTS_IRQ", XOFF_IRQ:"XOFF_IRQ", PIN_IRQ:"PIN_IRQ", MODEM_IRQ:"MODEM_IRQ", \
        TX_LEVEL_IRQ:"TX_LEVEL_IRQ", RX_LEVEL_IRQ:"RX_LEVEL_IRQ", RX_TIMEOUT_IRQ:"RX_TIMEOUT_IRQ", RX_LINE_ERROR:"RX_LINE_ERROR", None:"None"}

# === Bring up the SPI bus  ===
rst = Pin( Pin.board.GP16, Pin.OUT, value=True )
cs = Pin(Pin.board.GP9, Pin.OUT, value=True)
spi = SPI(1, mosi=Pin(Pin.board.GP11), miso=Pin(Pin.board.GP8, Pin.IN), sck=Pin(Pin.board.GP10), baudrate=SPI_BAUDRATE, firstbit=SPI.MSB, polarity=0, phase=0 )

# === IRQ DETECTION ===
# Input for IRQ pin
irq_count = 0
p22 = Pin(22, Pin.IN )
emit_flag = True # Can Emit data on UART

def on_irq( p ):
    global irq_count, emit_flag
    irq_count += 1   
    # Uncomment to see IRQ signal detection
    # print( "IRQ detected", irq_count ) 


p22.irq( trigger=Pin.IRQ_FALLING, handler=on_irq )

# === get UART & GPIO ===
# UART over SPI
uart_expander = SC16IS750( bus=spi, cs_pin=cs, rst_pin=rst, oscillator_hz=3072000 )
# Uart interface (act as machine.UART)
ser1 = uart_expander.uart( 1, baudrate=300, bits=8, parity=None, stop=1 )
# GPIO Pin as Input
p3 = uart_expander.pin( 3, Pin.IN )

# === Enable IRQ ===
# define the 
#  * rx_level to 8 chars (characters filling the FiFo)
#  * tx_level to 56 spaces available
uart_expander.rxtx_level( rx_level=16, tx_level=56 ) # At least one of the both must ve defines
# activate IRQ.
# Possible values are: 
#   CST_INT, RTS_INT, XOFF_INT, SLEEP_INT
#   MODEM_INT : Modem Status Interrupt
#   LINE_INT  : Receive Line Status interrupt
#   TX_INT    : Transmit Holding Register interrupt
#   RX_INT    : Receive Holding Register interrupt
#
uart_expander.enable_irq( RX_INT | TX_INT )

# === Main script ===
last_stat_ms = time.ticks_ms()
while True:
    # IRQ processing
    if irq_count>0:
        irq_count=0
        # Get IRQ Source (or None)
        #    Constant      : Priority Level
        #    --------------: -----------------
        #    CTS_RTS_IRQ   : 7 Higher Pritority
        #    XOFF_IRQ      : 6
        #    PIN_IRQ       : 5 => must read the pin status
        #    MODEM_IRQ     : 4 => must read modem status
        #    TX_LEVEL_IRQ  : 3
        #    RX_LEVEL_IRQ  : 2
        #    RX_TIMEOUT_IRQ: 2
        #    RX_LINE_ERROR : 1 Lowest priority
        #
        #   Returns None or Highest IRQ source.        
        src = uart_expander.irq_source() 
        if src==None: # Nothing to handle
            continue
        print( "------------------------")
        print( "IRQ Src  :", src )
        print( "IRQ Label:", IRQ_SOURCE_LABEL[src] )

        if src==TX_LEVEL_IRQ:
            # Enough space in TX ?
            # Let's allow emission again
            emit_flag=True
            print("Activates data emission")

        if src==RX_LEVEL_IRQ:
            # Enough chars received in the RX FiFo
            # Let's stop emitting
            emit_flag=False
            print("Stops data emission")

        # Resets IRQ detect
        irq_count=0
        

    # fill the TX FiFo buffer (which is connected
    # in loopback to RX)/
    if emit_flag:
        ser1.write( bytes([65,65,65,65,65,65,65,65,65,65,65,65]) ) # Send a B

    # read the data
    # Note: 
    #   if we test with any(), we will never reach the RX Timeout.
    #   This Timeout will initiate the RX_IRQ.
    #   if ser1.any():
    ser1.read(1) # Read one byte

    if (DELAY_MS>0) and (time.ticks_diff( time.ticks_ms(), last_stat_ms ) > DELAY_MS):
        # Display FiFo stats
        print( "RX: %s, TX: %s" %(ser1.any(), ser1.any_tx()) )
        last_stat_ms = time.ticks_ms()

    # Software processing
    idle()    

