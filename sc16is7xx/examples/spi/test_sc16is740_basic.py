""" sc16is740 over SPI demonstration with MicroPython 

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
uart_expander = SC16IS740( bus=spi, cs_pin=cs, rst_pin=rst )

# Grab the uart interface (act as machine.UART)
#
#   baudrate : (required) Calculated from oscillator_hz (default clock at 1843200 Hz, see SC16IS740 constructor)
#   bits     : 5,6,7,8 bits (8 by default)
#   parity   : None, 0=Even, 1=Odd, 10=Forced_0, 11=Forced_1
#   stop     : 1, 1.5, 2 stop bits (1.5 stop bit only works for 5 bit data length)
#
ser1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1 )

# Alternate ser1 creation
#
#  ser1 = uart_expander.uart( 1 )
#  ser1.init( baudrate=9600, bits=8, parity=None, stop=1 )



# =============================================
#
#   WRITE & READ
#
# =============================================


# Check SPI bus communication
print( "--- Display Internal Registers ---")
print( "Reg = Value")
for reg,value in ser1.dump_regs():
	print( hex(reg),'=', hex(value) )

# Sending bytes to TX FIFO
# non blocking under 64 bytes, blocking over 64 bytes
msg = "this is a simple test of sending"
print( "--- Sending bytes ---")
print( "Place a loopback TX->RX to get content in the RX FiFo." )
print( "" )
print( "SENDING: %s" % msg)
print( "" )
ser1.write( msg.encode('ascii') )


print( "--- Receiving bytes ---")
# Reading bytes from RX FIFO
#  Default timeout is 1000ms
#  Default timeout_char is 100ms
data = ser1.read()
print( "data:", data )
print( "text:", data.decode("ascii") )
print("")


print( "--- Timeout on receive ---")
# UART RX FiFo should now be empty --> read() should return None
data = ser1.read()
print( "data:", data )
print("")

print( "--- Sending bytes ---")
msg = "Twinkle, twinkle, little star,"
print( "SENDING: %s" % msg)
print( "" )
ser1.write( msg.encode('ascii') )


print( "--- Read 10 bytes only ---")
# Should be able to read Nth bytes from RX Fifo
data = ser1.read( 10 )
print( "data:", data )
print( "" )

time.sleep_ms(10)
print( "--- Read remaining bytes ---")
data = ser1.read()
print( "data:", data )
print( "" )


print( "--- Sending bytes ---")
msg = "Five little monkeys jumping on the bed,"
print( "SENDING: %s" % msg)
print( "" )
ser1.write( msg.encode('ascii') )


# =============================================
#
#   READ INTO BUFFER
#
# =============================================

buf = bytearray(20)

print( "--- Read 10 bytes into buffer ---")
count = ser1.readinto(buf, 10)
print( "count:", count )
print( "buffer:", buf )
print( "" )

print( "--- Read remaining into buffer ---")
while True:
	# clear buffer
	for i in range(len(buf)): 
		buf[i] = 0x00
	# Next read
	count = ser1.readinto(buf)
	if count==None:
		break
	print( "count:", count )
	print( "buffer:", buf )
print( "" )

print( "--- Read timeout into buffer ---")
for i in range(len(buf)): # clear buffer
	buf[i] = 0x00
count = ser1.readinto(buf)
print( "count:", count ) # Must returns None
print( "" )


# =============================================
#
#   ANY char received
#
# =============================================
# any() : check the RxFifo for pending chars (same as MicroPython)
# any_tx() : check the TxFifo for pending chars to send

print( "--- testing any() on empty FIFO ---")
have_data = ser1.any()
print( "Have Data:", have_data ) # must be False
print( "" )


print( "--- Sending bytes ---")
msg = "Shall I compare thee to a summer's day?"
print( "SENDING: %s" % msg)
print( "" )
ser1.write( msg.encode('ascii') )

# give sometime to the bytes to reach the RX FIFO
time.sleep_ms(10)

print( "--- testing any() on filled FIFO ---")
have_data = ser1.any()
print( "Have Data:", have_data ) # must be False
print( "" )
