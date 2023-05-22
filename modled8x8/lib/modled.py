import time
#
# --- THIS DRIVER IS UNDER REWRITING AGAINTS THE MICROPYTHON FRAMEBUFFER ---
#
import framebuf

RED     = 0b100 # Accordingly to MODLED definition
GREEN   = 0b010
BLUE    = 0b001
YELLOW  = 0b110
MAGENTA = 0b101
CYAN    = 0b011
WHITE   = 0b111
BLACK   = 0b000

def colorTo3Bit( color ):
	""" transform a color tuple (r_8bit, g_8bit , b_8bit) to 3 bits RGB byte value """
	rbit = 1 if color[0] > 127 else 0
	gbit = 1 if color[1] > 127 else 0
	bbit = 1 if color[2] > 127 else 0
	return (rbit<<2) + (gbit<<1) + bbit

class ModLedRGB( framebuf.FrameBuffer ):
	""" Class to control a set of width x height Olimex 8x8 LED Matrix (8x8) """

	def __init__( self, spi, ss, width=1, height=1 ):
		""" initialize the LED controler

			spi: Initialized SPI
			ss : chip select Pin (initalized as output)

			width: number of matrix columns in the assembly
			height: number of matrix row in the assembly """
		self.spi = spi
		self.ss  = ss
		self.ss.value( 1 ) # Ensure that ChipSelect is already properly initialized

		self.width = width
		self.height = height
		self.matrixes = width * height # Number of matrix in the assembly
		self.pixels   = (self.width*8, self.height*8) # Number of pixels in width and height

		# Video Buffer
		# 24 Bytes per matrix
		# so 192 bits per matrix (of 8x8 = 64 LEDs)
		# so 3 bits per LED RGB (one by color)
		## self.buffer = [0]*self.matrixes*24

		# __init__ the FrameBuffer ancestor
		_bufsize = self.pixels[0] * self.pixels[1] //2
		self._buffer = bytearray( _bufsize ) # 2 pixels per byte when GS4_HMSB
		super().__init__(
				self._buffer,
				self.pixels[0], # pixels width
				self.pixels[1], # pixels height
				framebuf.GS4_HMSB # 4 bits grayscale, recoded with LED8x8RGB bitmapping Bit mapping: unused-bit, Blue-bit, Green-Bit, Red-bit
				)
		self.clear()

	def clear( self ):
		""" just clear the screen """
		self.fill( BLACK )

	def color( self, r, g, b ):
		""" encode the B,G,R bits color inside the 4 bitd color value (of GS4_HMSB storage).
			r,g,b are True/False """
		# Bit mapping: unused-bit, Blue-bit, Green-Bit, Red-bit
		_c = 0
		if r:
			_c += 1
		if g:
			_c += 1<<1
		if b:
			_c += 1<<2
		return _c

	def show( self ): # send buffer to MOD-LEDs
		rowbuff = bytearray(3) # 1 byte red + 1 byte green + 1 byte blue
		self.ss.value( 0 ) # Start SPI transaction
		for row in range( self.height-1,-1, -1): # 2 row -> 1,0
			for col in range( self.width-1, -1, -1 ): # 3 columns -> 2,1,0
				# Send data for matrix row, col
				# DEBUG: print( 'row,col = %s, %s' % (row,col) )
				for line in range( 7, -1, -1 ): # Lines in the maxtrix 7,6,5...1,0
					# Collect GS4_HSMB 4 bytes of data [0rgb|0rgb] [0rgb|0rgb] [0rgb|0rgb] [0rgb|0rgb]
					data = self._extract_8pixbuff( x=col*8, y=row*8+line )
					# Encode RED (right most pixel @ highest weight)
					rowbuff[0]  = (data[0] & 0b01000000)>>6 | (data[0] & 0b00000100)>>1
					rowbuff[0] |= (data[1] & 0b01000000)>>4 | (data[1] & 0b00000100)<<1
					rowbuff[0] |= (data[2] & 0b01000000)>>2 | (data[2] & 0b00000100)<<3
					rowbuff[0] |= (data[3] & 0b01000000)    | (data[3] & 0b00000100)<<5
					# Encode GREEN
					rowbuff[1]  = (data[0] & 0b00100000)>>5 | (data[0] & 0b00000010)
					rowbuff[1] |= (data[1] & 0b00100000)>>3 | (data[1] & 0b00000010)<<2
					rowbuff[1] |= (data[2] & 0b00100000)>>1 | (data[2] & 0b00000010)<<4
					rowbuff[1] |= (data[3] & 0b00100000)<<1 | (data[3] & 0b00000010)<<6
					# Encode BLUE
					rowbuff[2]  = (data[0] & 0b00010000)>>4 | (data[0] & 0b00000001)<<1
					rowbuff[2] |= (data[1] & 0b00010000)>>2 | (data[1] & 0b00000001)<<3
					rowbuff[2] |= (data[2] & 0b00010000)    | (data[2] & 0b00000001)<<5
					rowbuff[2] |= (data[3] & 0b00010000)<<2 | (data[3] & 0b00000001)<<7
					# Stricly follow Olimex Specs for sending data
					for value in rowbuff:
						self.spi.write( bytes([value]) )
						time.sleep_us( 10 )
		self.ss.value( 1 )


	def _extract_8pixbuff( self, x, y ):
		""" Extract a buffer of data for 8 horizontals pixels from position x,y """
		# print( '_extract_8pixbuff @ x,y = %s, %s' % (x,y))
		assert (x % 2) == 0
		pos = ((y*self.pixels[0])+x) // 2 # //2 because 2 pixels per byte
		# DEBUG: display pixel data
		#s = ''
		#for i in range(4):
		#	s += '[%s]' % bin( self._buffer[pos:pos+4][i] )
		#print( s )
		return self._buffer[pos:pos+4] # 4 bytes = 8 pixels

	def _dump( self ):
		""" Dump the content of the Buffer to REPL """
		def pad_bin( s ):
			s = s.replace('0b','')
			s = '0'*(8-len(s))+s
			return s
		print( '--- Dump buffer ---' )
		print( 'Pos: hex : Binary'   )
		for i in range( len(self._buffer) ):
			print( '%3s : %2x  : %5s' % (i, self._buffer[i], pad_bin(bin(self._buffer[i])))  )
