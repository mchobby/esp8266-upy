""" PBM (Portable Bit Map) a 2 color bitmap file format reader.

    bpm file store image with 1 bit per pixel
    Does not support any kind of compression
"""
__version__ = '0.0.1'

WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)

class PbmException( Exception ):
	pass


class PbmReader():
	""" Read a BPM Portable Bit Map file and offer basic pixel reading.
	    Can manage absolute pixel reading and consecutive pixel reading on a line.
		Caller must use seek_pix() to jump from one line to another"""

	def __init__( self, stream, check=True ):
		""" open a PBM file. The stream must be a FileIO opended on target file """
		self.fileio = stream
		self.startbit = None # Start bit of data
		self.width    = None # Bitmap size
		self.height   = None
		self.bpp      = 1 # 1 Bit per pixel
		self.compression = None # Compression algorithm
		self.colors_used = None # No color indexing image

		# Bit reader
		self._next_pix = None # Current pixel to read
		self._curr_byte= None # Current byte tp extract the pixel
		self._next_mask= None # Next mask to use to read the next pixel (next bit)

		self.decode_header()
		if check:
			self.check_compatible() # Check if the format is compatible
		self.seek_pix( (0,0) )  # Ready to read first pixel

	def close( self ):
		""" close the file """
		self.fileio.close()

	def decode_header( self ):
		if self.fileio.read(2) != b'P4':
			raise PbmpException( 'Not a binary PBM' )
		self.fileio.readline() # finish to read magic key
		self.fileio.readline() # Creator comment

		size = self.fileio.readline().decode('utf-8').split()
		self.width = int(size[0])
		self.height= int(size[1])
		self.startbit= self.fileio.tell() # Current position = start of data

	def check_compatible( self ):
		""" Check if the image format is compatible with reader class otherwise raise exception """
		if self.compression != None:
			raise PbmException( "unsupported compression %i" % self.compression )
		if self.bpp != 1:
			raise BmpException( "invalid %i Bits Per Pixel" % self.bpp )

	def seek_pix( self, pos ):
		""" Move the file cursor to read pixel at position pos (x,y) """
		# each line is encoded on a row of byte, each byte encoding 8 pixels (padded with 0)
		line_padding =  8-(self.width%8) # for 277 pixels width it gives 3 pixels (3 bits) padding.
		if line_padding==8: # Was multiple of 8 ==> remove the line padding!
			line_padding=0
		# The TOP image scan-line is stored at the end of the file!
		offset = self.startbit + (pos[1]*(self.width+line_padding))//8 + (pos[0]//8)
		# print( 'seek_pix @ %s' % hex(offset) ) # Debug
		self.fileio.seek( offset )

		# Initialize Bit reader
		self._next_pix = pos[0] # Current pixel to read
		self._curr_byte= self.fileio.read(1)[0] # Current byte to extract the pixel
		bit_pos = pos[0] % 8
		self._next_mask= 0x01 << (7-bit_pos) # Next mask to use to read the next pixel (next bit)


	def read_pix( self, pos=None ):
		""" Read color of the next pixel and return a rgb tuple.
		    When initialized, pos may a a tuple of (x,y) pixel to position before reading """
		if pos:
			self.seek_pix( pos )
		# Signal for read the next byte?
		if self._curr_byte == None:
			self._curr_byte = self.fileio.read(1)[0]
		# Apply bit mask
		_r = (self._curr_byte & self._next_mask) > 0
		# Move bit mask to right (for next pixel)
		self._next_mask >>= 1
		self._next_pix += 1
		# Move to next byte ?
		if (self._next_mask == 0) or (self._next_pix >= self.width):
			self._next_mask = 0x80
			self._curr_byte = None # Signal reading @ Next read_pix() round
			if self._next_pix >= self.width:
				# rewind to next line
				self._next_pix = 0

		return WHITE_COLOR if _r else BLACK_COLOR # True/False

#    with open('upy-logo.pbm', 'rb' ) as f:
#        f.readline() # Magic number    P4 for pbm (Portable Bitmap)
#        f.readline() # Creator comment
#        f.readline() # Dimensions
#        data = bytearray(f.read())
#
#    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
#    lcd.invert(1)
#    lcd.blit(fbuf, 0, 0)
#    lcd.show()
#
#    time.sleep(3)
