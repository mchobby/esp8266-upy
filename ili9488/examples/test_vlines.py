# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
# In this sample we will:
# * See the screen axes (in related image)
# * Draw a vertical lines (hline optimized)
#
from machine import SPI,Pin
from ili9488 import *

# Raspberry-Pi Pico
spi = SPI( 0, miso=Pin.board.GP4, mosi=Pin.board.GP7, sck=Pin.board.GP6, baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(5, Pin.OUT, value=1 )
dc_pin = Pin(3, Pin.OUT )
rst_pin = Pin(2, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin )  # w=320, h=480, r=0
lcd.erase()

# Correct positionning
lcd.pixel( 80, 130, YELLOW ) # x=80, y=130
lcd.vline( 80, 131, 20, BLUE )

# Half height of screen
lcd.vline( 120,0, lcd.height//2, GREEN )

lcd.vline( 130, 0, lcd.height//2, PURPLE, tick=3 )
