""" sc16is750 over SPI demonstration with MicroPython 

    Using SC16IS750 to configure its GPIO 3 as input and 
       configure it to generates an IRQ when GPIO state change.
    IRQ pin must be Pull-up to 3V3 with a 1K resistor.
    IRQ is connected to Pico GP22
    IRQ will go LOW when state changes and will resets on state read.

    Then configure IRQ line the scripot reads the state of its GPIO 3 every seconds.    

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

def on_irq( p ):
    global irq_count
    irq_count += 1   
    # Uncomment to see IRQ calls
    # print( "--------------", irq_count ) 

p22.irq( trigger=Pin.IRQ_FALLING, handler=on_irq )

# === get UART & GPIO ===
# UART over SPI
uart_expander = SC16IS750( bus=spi, cs_pin=cs, rst_pin=rst, oscillator_hz=3072000 )
# Uart interface (act as machine.UART)
ser1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1 )
# GPIO Pin as Input
p3 = uart_expander.pin( 3, Pin.IN )
p3.enable_irq()

# === Main script ===
while True:
    # IRQ processing
    if irq_count>0:
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
        if src==None: # Nothing relevant yet
            continue
        print( "----------------" )            
        print( "IRQ Src   :", src ) # SRC is a list of xxx_IRQ
        if src in IRQ_SOURCE_LABEL:
            print( "IRQ label :", IRQ_SOURCE_LABEL[src] )
        else:
            print( "IRQ label : undefined!" )
        if src==PIN_IRQ:
            # Reading GPIOs will reset the IRQ signal
            print( "GPIO 3 = ", p3.value() )  
        # clear IRQ detection
        irq_count=0

    # Software processing
    idle()    

