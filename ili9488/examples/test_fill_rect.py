# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
# In this sample we will:
# * See the screen axes (in related image)
# * Draw arbitrary lines
#
from machine import SPI,Pin
from ili9488 import *
import urandom

# Raspberry-Pi Pico
spi = SPI( 1, baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(9, Pin.OUT, value=1 )
dc_pin = Pin(12, Pin.OUT )
rst_pin = Pin(13, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, r=1) # w=320, h=480, r=0
lcd.erase()

colors = [NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE, LIGHTGREY,
		DARKGREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE, ORANGE,
		GREENYELLOW ]
color_count = len( colors )

for i in range(300):
	lcd.fill_rect( urandom.randint(0,lcd.width-1), urandom.randint(0,lcd.height-1),
				urandom.randint(1,50), urandom.randint(1,50),
				colors[urandom.randint(0,color_count-1)] )
