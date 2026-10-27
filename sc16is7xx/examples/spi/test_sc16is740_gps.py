""" sc16is740 over SPI demonstration with MicroPython 

  The SC16IS740 a SPI/I2C to UART interface with 64 bytes FiFo.
  It offers only ONE UART.

  Attach a GPS-ULTIMATE on the SC16IS740 UART.
  Use the SC16IS740.UART as reference for the GPS library.
  The GPS library will use the UART.readline() to acquire the NMEA stream (from GPS module).
  The GPS library will see the SC16IS740 UART as an machine.UART .

  requires the GPS-Ultimate library available @ https://github.com/mchobby/esp8266-upy/tree/master/gps-ultimate


* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from machine import SPI, Pin
from sc16is7xx import SC16IS740
from sc16is7xx import *
import adafruit_gps
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
uart_expander = SC16IS740( bus=spi, cs_pin=cs, rst_pin=rst, oscillator_hz=14_745_600 ) # another osc: oscillator_hz=14_745_600 

# Grab the uart interface (act as machine.UART)
#
#   baudrate : (required) Calculated from oscillator_hz (default clock at 1843200 Hz, see SC16IS740 constructor)
#   bits     : 5,6,7,8 bits (8 by default)
#   parity   : None, 0=Even, 1=Odd, 10=Forced_0, 11=Forced_1
#   stop     : 1, 1.5, 2 stop bits (1.5 stop bit only works for 5 bit data length)
#
#   timeout  : wait up to 1500ms to get a complete line with readline
#
uart1 = uart_expander.uart( 1, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500 ) 

# =============================================
#
#   Using GPS Library on top of SPI-->UART
#
# =============================================

gps = adafruit_gps.GPS(uart1)

# Active les infos basiques GGA et RMC
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Mise-à-jour une fois par seconde (1hz)
gps.send_command('PMTK220,1000')

# Boucle principale
last_print = time.ticks_ms()
while True:
    gps.update()
    # Afficher chaque seconde
    current = time.ticks_ms()
    if time.ticks_diff(current, last_print) >= 1000:
        last_print = current

        if not gps.has_fix:
            print('Waiting for fix...')
            continue

        print('=' * 40)  
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc[1],  
            gps.timestamp_utc[2],
            gps.timestamp_utc[0],
            gps.timestamp_utc[3],
            gps.timestamp_utc[4],
            gps.timestamp_utc[5]))
        print('Latitude: {} degrees'.format(gps.latitude))
        print('Longitude: {} degrees'.format(gps.longitude))
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.track_angle_deg is not None:
            print('Speed: {} km/h'.format(gps.speed_knots*1.8513))