"""
 modledraw is a RAW CODE PORTAGE to micropython for the MOD-LED8x8RGB Olimex board.

 The aim of this code is to test code against the Matrix with the Olimex buffer
 method before going to MicroPython's FrameBuffer implementation.

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
import time

class ModLedRGBraw():
	""" Class to control a set of width x height Olimex 8x8 LED Matrix (8x8).

		This version of the class is a RAW portage of the Arduino code example"""
	def __init__( self, spi, ss, width=1, height=1 ):
		""" initialize the LED controler

			spi: Initialized SPI
			ss : chip select Pin (initalized as output)

			width: number of columns in the assembly
			height: number of row in the assembly """
		self.spi = spi
		self.ss  = ss
		self.ss.value( 1 ) # Ensure that ChipSelect is already properly initialized

		self.width = width
		self.height = height
		self.matrixes = width * height # Number of matrix in the assembly

		# Video Buffer
		# 24 Bytes per matrix
		# so 192 bits per matrix (of 8x8 = 64 LEDs)
		# so 3 bits per LED RGB (one by color)
		self.buffer = [0]*self.matrixes*24
		self.vclear()

	def vclear( self ):
		for i in range( len(self.buffer) ):
			self.buffer[i] = 0 # all bits to 0 = switch off all matrixes

	def drawPixel( self, x, y, color ):
		""" Set a pixel color, color is coded on 3 bit RGB.

			draw drawPixel at x,y coordinates to MOD-LED8x8RGB 1,1 is upper left corner
		"""
		if not( (y <= self.height*8) and (x <= self.width*8) and (x>0) and (y>0) ):
			return

		if y>8:
			x = (x+self.width*8) * ((y-1)//8)
		y = y % 8
		if y==0:
			y=8

		# p : Position in the buffer
		p = self.matrixes - ((x-1)//8)-1

		# turn off chosen drawPixel
		self.buffer[ 3*(y-1)+24*p   ] &= 0xFF-(1 << ((x-1)%8))
		self.buffer[ 3*(y-1)+1+24*p ] &= 0xFF-(1 << ((x-1)%8))
		self.buffer[ 3*(y-1)+2+24*p ] &= 0xFF-(1 << ((x-1)%8))

		# set color to the drawPixel
		if color & 1: # Red
			self.buffer[ 3*(y-1)+0+(24*p) ] |= (1 << ((x-1)%8) )
		if color & 2: # Green
			self.buffer[ 3*(y-1)+1+(24*p) ] |= (1 << ((x-1)%8) )
		if color & 4: # Blue
			self.buffer[ 3*(y-1)+2+(24*p) ] |= (1 << ((x-1)%8) )

	def show( self ): # Like OLED Driver
		self.ss.value( 0 ) # Start SPI transaction
		for value in self.buffer:
			# Stricly follow Olimex Specs for sending data
			self.spi.write( bytes([value]) )
			time.sleep_us( 10 )
		self.ss.value( 1 )
