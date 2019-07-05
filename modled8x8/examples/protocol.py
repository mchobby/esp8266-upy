"""
 protocol is a RAW micropython code to test the SPI protocol against MOD-LED8x8RGB Olimex board.

 The aim of this code is to undestand how SPI protocol works to push the data to the Matrix

MOD-LED8x8RGB is 8x8 RGB LED Matrix (7 colors) that can be daisy chained.

MOD-LED8x8RGB board : http://shop.mchobby.be
MOD-LED8x8RGB board : https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware
Arduino code sample : https://github.com/OLIMEX/UEXT-MODULES/tree/master/MOD-LED8x8RGB/ARDUINO%20EXAMPLE

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from machine import Pin, SPI
import time

# Initialize the SPI Bus (on ESP8266-EVB)
# Software SPI
#    spi = SPI(-1, baudrate=4000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# Hardware SPI on Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # low @ 2 MHz
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

def send( lst ):
	""" send a list of bytes to the matrix """
	global ss
	global spi
	ss.value( 0 ) # Start SPI transaction
	for value in lst:
		# Stricly follow Olimex Specs for sending data
		spi.write( bytes([value]) )
		time.sleep_us( 10 )
	ss.value( 1 )

def test_onerow():
	""" bottom row, 8 pixels in RED """
	# one row is made of RED-bits (8 bits) + GREEN-bits (8 bits) + BLUE-bits (8 bits).
	# one bit of each per pixel (from left to right)
	lst = [ 0xFF, 0x00, 0x00 ] # All red LED on, all green led off, all blue leds off.
	send( lst )

def test_rgbrow():
	""" Push Red row, then Green row and finally Blue row.
	so bottom row is RED (first pushed), middle row is green and top row (last pushed) is Blue """
	lst = [ 0xFF, 0x00, 0x00,  # BOTTOM row - pushed first: one row with RED-bits ON, GREEN-bits off, BLUE-bits off
			0x00, 0xFF, 0x00,  # Middle row            : second row with GREEN-bits ON
			0x00, 0x00, 0xFF ] # TOP row - pushed last : Blue-bits ON
	send( lst )

def test_rgbmatrix():
	""" Push all RGB color combination from bottom to top of a single matrix.
	so bottom row is Blue (last pushed), middle row is green and top row (first pushed) is Red """
	lst = [ 0xFF, 0x00, 0x00,  # BOTTOM row - pushed first: one row with RED-bits ON, GREEN-bits off, BLUE-bits off
			0x00, 0xFF, 0x00,  #  next row is GREEN-bits ON
			0x00, 0x00, 0xFF,  #  next row is Blue-bits ON
			0xFF, 0xFF, 0x00,  #  next row is RED+Green = Yellow
			0xFF, 0x00, 0xFF,  #  next row is RED+Blue = MAGENTA
			0x00, 0x00, 0x00,  #  next row is black
			0x00, 0xFF, 0xFF,  #  next row is Green+Blue = CYAN
			0xFF, 0xFF, 0xFF   # TOP row - pushed last
		  ]
	send( lst )

def test_daisy_chain():
	""" Idem as rgbmatrix but add a matrix with 3 additional row (most are off).
	    This push the first matrix at the second position in the daisy chain """
	#                            --- MATRIX 1 : same as test_rgbmatrix()
	lst = [ 0xFF, 0x00, 0x00,  # BOTTOM row - pushed first: one row with RED-bits ON, GREEN-bits off, BLUE-bits off
			0x00, 0xFF, 0x00,  #  next row is GREEN-bits ON
			0x00, 0x00, 0xFF,  #  next row is Blue-bits ON
			0xFF, 0xFF, 0x00,  #  next row is RED+Green = Yellow
			0xFF, 0x00, 0xFF,  #  next row is RED+Blue = MAGENTA
			0x00, 0x00, 0x00,  #  next row is black
			0x00, 0xFF, 0xFF,  #  next row is Green+Blue = CYAN
			0xFF, 0xFF, 0xFF,  # TOP row - pushed last
			0x00, 0x00, 0x00,  # --- MATRIX 2 : Bottom row in BLACK
			0b11110000, 0b10101010, 0b01101101, # Next row is color combination
			0xFF, 0x00, 0x00,  # third row from the bottom is RED
			0x00, 0x00, 0x00,
			0x00, 0x00, 0x00,
			0x00, 0x00, 0x00,
			0x00, 0x00, 0x00,
			0x00, 0x00, 0x00
		  ]
	send( lst )

# test_onerow()
# test_rgbrow()
# test_rgbmatrix()
test_daisy_chain()
