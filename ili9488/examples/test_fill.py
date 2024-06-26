# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
#
# Fill the screen with a rectangle
#
from machine import Pin, SPI
from ili9488 import *
from random import choice

# Raspberry-Pi Pico
spi = SPI( 0, miso=Pin.board.GP4, mosi=Pin.board.GP7, sck=Pin.board.GP6 ,baudrate=40_000_000 ) # 40 Mhz, reduce it to 1 MHz in case of trouble
cs_pin = Pin(5, Pin.OUT, value=1 )
dc_pin = Pin(3, Pin.OUT )
rst_pin = Pin(2, Pin.OUT, value=1 )

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
# Use 3 for landscape mode
lcd = ILI9488( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin ) # w=320, h=480, r=0

colors = [BLACK,NAVY,DARKGREEN,DARKCYAN,MAROON,PURPLE,OLIVE,LIGHTGREY,DARKGREY,
	BLUE,GREEN,CYAN,RED,MAGENTA,YELLOW,WHITE,ORANGE,GREENYELLOW]

while True:
	lcd.fill( choice(colors) )
	lcd.fill_rect( 10,10, 20, 20, choice(colors) )

# lcd.erase()
# Compose a color
# red = color565(255,0,0)
# Fill the screen
# lcd.fill( red )
