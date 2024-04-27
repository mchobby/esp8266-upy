# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
# In this sample we will:
# * Draw lines on the screen
#
# Arbitrary lines implies lot of computation and communications over SPI
# Dranwing this sample may be pretty slow (several minutes)
#
from machine import SPI,Pin
from ili9488 import *

# Raspberry-Pi Pico
spi = SPI( 0, miso=Pin.board.GP4, mosi=Pin.board.GP7, sck=Pin.board.GP6 , baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(5, Pin.OUT, value=1 )
dc_pin = Pin(3, Pin.OUT )
rst_pin = Pin(2, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin) # w=320, h=480, r=0
lcd.erase()

colors = [NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE, LIGHTGREY,
		DARKGREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE, ORANGE,
		GREENYELLOW ]
color_count = len( colors )

for y in range( lcd.height//3 ):
	lcd.line( 0,0, lcd.width, y*3, colors[y % color_count] )

for x in range( lcd.width//3 ):
	lcd.line( 0,0, lcd.width-(x*3), lcd.height, colors[x % color_count] )
