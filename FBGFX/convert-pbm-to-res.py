#!/usr/bin/env python3
"""
This Python3 script converts a binary pbm file to python code ressource
allowing fbutils.py:draw_bitmap() function to display it!

obj_name is the object name as it appears in the created ressource code.

Example:
  convert-pbm-to-res.py minesweeper.pbm LOGO

Usage:
  convert-pbm-to-res.py <in_filename>  <obj_name> [--show] [--debug]
  convert-pbm-to-res.py (-h | --help)
  
Options:
  --show    Show the extracted images in the output.
  --debug   Show debugging messages
  
"""
from docopt import docopt 
from os.path import basename

#WHITE_COLOR = (255,255,255)
#BLACK_COLOR = (0,0,0)

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

		# Byte offset
		self.offset = None

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
		size = None
		comment = self.fileio.readline().decode('utf-8')
		if len(comment)==0: 
			pass # let's consider it as an empty comment
		elif comment[0]=='#':
			pass # it is indeed a comment!
		else:
			# It is already the size information
			size = comment.split() 
		
		if size==None:
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
		self.offset = self.startbit + (pos[1]*(self.width+line_padding))//8 + (pos[0]//8)
		# print( 'seek_pix @ %s' % hex(offset) ) # Debug
		self.fileio.seek( self.offset )

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

		return 1 if _r else 0 # True/False

	def read_line_into( self, buf ):
		# read an image line at frameBuffer format. Store the data into buf.
		self.fileio.seek( self.offset ) # Bit per bit read_pix already load the first byte. So we must reseek
		return self.fileio.readinto(buf) # return number of bytes read, 0 for EOF, None when no data, negative for error


def export_pbm( in_filename, obj_name, bshow=False, bdebug=False ):
	with open(in_filename, 'rb' ) as f:
		reader=PbmReader( f )
		reader.check_compatible()
		print( "Size: %i x %i pixels" %(reader.width,reader.height) )
		print( "")
		data = []
		for y in range( reader.height ):
			data_line = []
			data.append( data_line )
			bits = 0
			val = 0
			for x in range( reader.width ):
				val = (val<<1)+reader.read_pix()
				bits += 1
				if bits==8:
					data_line.append( val )
					val = 0
					bits= 0
			# Eject last byte ?
			if bits>0:
				while bits<8:
					val = val<<1
					bits += 1
				data_line.append( val )

	# Create output stream
	data.reverse()
	print( '# %s - %i x %i pixels' % (basename(in_filename),reader.width,reader.height) )
	print( '# Ressource for FBGFX fbutil.py : FBUtil.draw_bitmap() ')
	print( '# Call fbutil_obj.draw_bitmap( x, y, %s, %i, %i, 1 )' %(obj_name, reader.width, reader.height) )
	data_line = data.pop()
	print( '%s = [ %s%s' % (obj_name, ','.join([ str(val) for val in data_line ]), "," if len(data)>0 else "" ) )
	while len(data)>0:
		data_line = data.pop()
		print( '\t%s%s' % (','.join([ str(val) for val in data_line ]), "," if len(data)>0 else "]" ) )


if __name__=="__main__":
    arguments = docopt(__doc__)
    if arguments['--debug']:
        print("Arguments :", arguments )
    
    
    if len('<in_filename>')>0:
        export_pbm( in_filename=arguments['<in_filename>'],
                      obj_name=arguments['<obj_name>'],
                      bshow=arguments['--show'],
                      bdebug=arguments['--debug'] )
    print( '' )
    print( 'Done!' )