""" Bitmap file format reader.

    bmp file store image with RGB888 (24 bit per pixel)
    Does not support any kind of compression
"""
__version__ = '0.0.1'

import struct

BI_RGB  = 0 # no compression!
BI_RLE8 = 1 # 8bit RLE encoding
BI_RLE4 = 2 # 4bit RLE encoding

class BmpException( Exception ):
	pass

class BmpReader():
	""" Read a RGB888 bitmap file and offer basic pixel reading.
	    Can manage absolute pixel reading and consecutive pixel reading on a line.
		Caller must use seek_pix() to jump from one line to another"""

	def __init__( self, stream, check=True ):
		""" open a BMP file. The stream must be a FileIO opended on target file """
		self.fileio = stream
		self.startbit = None
		self.width    = None # Bitmap size
		self.height   = None
		self.bpp      = None    # Bit per pixels. Either 1, 4, 8, 16, 24
		self.compression = None # Compression algorithm
		self.colors_used = None # Nbre of colors used (with indexing images)

		self.decode_header()
		if check:
			self.check_compatible() # Check if the format is compatible
		self.seek_pix( (0,0) )  # Ready to read first pixel

	def close( self ):
		""" close the file """
		self.fileio.close()

	def decode_header( self ):
		if self.fileio.read(2) != b'BM':
			raise BmpException( 'Not a BMP' )

		self.fileio.seek( 0x0A ) # Data Offset
		self.startbit = struct.unpack('<H', self.fileio.read(2))[0]
		self.fileio.seek( 0x12 )
		self.width = struct.unpack('<H', self.fileio.read(2))[0]
		self.fileio.seek( 0x16 )
		self.height = struct.unpack('<H', self.fileio.read(2))[0]
		# Bit Per Pixel
		self.fileio.seek( 0x1C )
		self.bpp = struct.unpack('<H', self.fileio.read(2))[0]
		# Compression
		self.fileio.seek( 0x1E )
		self.compression = struct.unpack( '<I', self.fileio.read(4))[0]
		# Color used - useful with color index
		self.fileio.seek( 0x2E )
		self.colors_used = struct.unpack( '<I', self.fileio.read(4))[0]

	def check_compatible( self ):
		""" Check if the image format is compatible with reader class otherwise raise exception """
		if self.compression != BI_RGB:
			raise BmpException( "unsupported compression %i" % self.compression )
		if self.bpp != 24:
			raise BmpException( "invalid %i Bits Per Pixel" % self.bpp )

	def seek_pix( self, pos ):
		""" Move the file cursor to read pixel at position pos (x,y) """
		# each line is encoded on a row having a multiple of 4 bytes (padded with 0)
		line_padding =  4-((self.width*3)%4) # for 277 pixels width it gives 4-((277*3)%4) = 4-3 = 1 byte padding per line. 277*3+1 can be devided by 4!
		if line_padding==4: # Was multiple of 4 ==> remove the line padding!
			line_padding=0
		# The TOP image scan-line is stored at the end of the file!
		offset = self.startbit + ((self.height-1-pos[1])*(self.width*3+line_padding)) + (pos[0]*3)
		# print( 'seek_pix @ %s' % hex(offset) ) # Debug
		self.fileio.seek( offset )

	def read_pix( self, pos=None ):
		""" Read color of the next pixel and return a rgb tuple.
		    When initialized, pos may a a tuple of (x,y) pixel to position before reading """
		if pos:
			self.seek_pix( pos )
		return tuple( reversed(self.fileio.read(3)) ) # read 3 bytes for RGB. b'"""'
