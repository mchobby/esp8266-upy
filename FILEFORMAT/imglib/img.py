""" Toolbox function for the various image reader """

import time, framebuf

__version__ = '0.0.3'

def grayscale( r,g,b ):
	""" Compute grayscale (brightness) 0..232 from r,g,b values (0..255) """
	return int( 0.3*r + 0.6*g + 0.11*b ) # darker image can be created with 0.25*r + 0.5*g + 0.25*b

def charpix( r,g,b ):
	""" Compute a char ' .-+*X' in relation with the grayscale luminosity of a pixel.
	    Would allow to display rudimentary picture on terminal """
	pc = int( grayscale(r,g,b) / 25.5 * 10 ) # In percent for a range 0..255
	return "  ..-+**XXX"[pc//10]

class ClipReader():
	""" Reader that allows to clip reading the original image.
	    Would allow to access a partial content (a "window" of larger image) on
	    an ImageReader.
		Clip reader can manage continuous pixel reading with automatic line return, etc. """

	# See the examples/testbmp.py for example of usage.
	def __init__( self, img_reader ):
		self.reader = img_reader
		# Clip the while image par default
		self.area  = (0,0,self.reader.width,self.reader.height) # x_min, y_min, x_max, y_max
		self.width = self.reader.width  # Clipping area width
		self.height= self.reader.height # Clipping area height
		self.reader.seek_pix( (0,0) )
		# Current reader position in the original picture
		self.x=0
		self.y=0

	def close( self ):
		self.reader.close()

	def read_pix( self, pos=None ):
		""" Read color of the next pixel IN THE CLIPPING AREAD and return a rgb tuple.
		    When initialized, pos may a a tuple of (x,y) pixel to position "in the clipping area" before reading """
		if pos:
			self.x = pos[0]+self.area[0] # Not tested yet : ClipReader.read_pix with pos!=None
			self.y = pos[1]+self.area[1]
			self.reader.seek_pix( (self.x,self.y) )
		_pixel = self.reader.read_pix()

		# Need to reposition cursor in the image file
		_reseek = False
		# Increment pixel reader x,y
		self.x += 1
		if self.x>=self.area[2]: # > X_max?
			self.x = self.area[0] # x_min
			self.y += 1
			_reseek = True
		if self.y>=self.area[3]: # > y_max
			self.y = self.area[1] # restart at the Y begining y_min
			_reseek = True
		# needs a cursor repositionning in the file?
		if _reseek:
			self.reader.seek_pix( (self.x, self.y) )

		return _pixel

	def read_line_into( self, buf, pos=None ):
		""" Read a fukk kube IN THE CLIPPING AREAD and fills the buffer at proper format.
		    When initialized, pos may a a tuple of (x,y) pixel to position "in the clipping area" before reading """
		if pos:
			self.x = pos[0]+self.area[0] # Not tested yet : ClipReader.read_pix with pos!=None
			self.y = pos[1]+self.area[1]
			self.reader.seek_pix( (self.x,self.y) )
		
		self.reader.read_line_into( buf )

		# Need to reposition cursor in the image file
		_reseek = True # always after line reading
		# Increment y line reader (x is constant)
		self.x = self.area[0] # x_min
		self.y += 1

		if self.y>=self.area[3]: # > y_max
			self.y = self.area[3] # stay at max position 
			# note self.area[1] # restart at the Y begining y_min
			_reseek = False
		# needs a cursor repositionning in the file?
		if _reseek:
			self.reader.seek_pix( (self.x, self.y) )

		#return _reseek # return True while another line is available


	def clip( self, x, y, width, height ):
		""" Set the clipping area and get ready to read the first pixel """
		assert x>=0 and y>=0 and width>0 and height>0
		if not( 0<= x < self.reader.width ):
			raise Exception( "Invalid x = %i" % x )
		if not( 0<= y < self.reader.height ):
			raise Exception( "Invalid y = %i" % y )
		if not( 0<= x+width <= self.reader.width ):
			raise Exception( "Invalid width = %i from x = %i" % (width,x) )
		if not( 0<= y+height <= self.reader.height ):
			raise Exception( "Invalid height = %i" % height )
		self.area = (x, y, x+width, y+height )
		self.width = width  # Clipping area width
		self.height= height # Clipping area height
		self.x, self.y = x, y # x,y position read in the whole image
		self.reader.seek_pix( (self.x, self.y) )

	def show( self, reseek=False ):
		""" Display Clip area on the terminal (including image) """
		print( "-"*20 )
		print( "   CLIP AREA" )
		print( "(x,y,W,H) = (%i,%i , %i,%i)" % (self.area[0], self.area[1], self.width, self.height) )
		print( "-"*20 )
		if reseek:
			self.x, self.y = self.area[0], self.area[1]
			self.reader.seek_pix( (self.x, self.y) )
		for line in range( self.height ):
			print( "".join([ charpix( *self.read_pix() ) for col in range(self.width) ]) )

	def copy_to( self, target_fb, x,y, color_fn ):
		"""" Copy the clipped area TO a target FrameBuffer """
		# start copy to position (x,y) in target_fb for the current
		# clipping area width & height. color_fn do transform
		# the clip reader color (r,g,b) to the target_fb color
		for line in range(self.height):
			start = time.ticks_ms()
			for col in range(self.width):
				target_fb.pixel(x+col,y+line,color_fn(self.read_pix()))
			print( "copy line %i ms" % time.ticks_diff(time.ticks_ms(),start) )

	def copy_fast_to( self, target_fb, x, y ):
		"""" Copy the clipped area TO a target FrameBuffer """
		# start copy to position (x,y) in target_fb for the current
		# clipping area width & height. The target_fb and file format must have the same format
		
		# Only handle monochrome image
		byte_size = (self.width//8)+(0 if (self.width%8)==0 else 1 )
		_buf = bytearray( byte_size )
		fbuf = framebuf.FrameBuffer( _buf, self.width, 1, framebuf.MONO_HLSB ) # Should be MONO_HMSB if rotate 90
		# Preallocate a buffer		
		for line in range(self.height):
			start = time.ticks_ms()
			# self.width
			self.read_line_into(fbuf)
			target_fb.blit( fbuf, x, y+line )			
			#print( x, y+line, _buf )
			#print( "copy fast line %i ms" % time.ticks_diff(time.ticks_ms(),start) )

def open_image( filename ):
	""" Helper that detect image type based on file extension. Open the appropriate
	    image reader (eg: BmpReader) and then the ClipReader over the reader.
	    a ClipReader on the target image """
	reader = None
	if '.bmp' in filename:
		_f = open( filename, "rb" )
		from bmp import BmpReader
		reader = BmpReader( _f )
	elif '.pbm' in filename:
		_f = open( filename, "rb" )
		from pbm import PbmReader
		reader = PbmReader( _f )

	if not(reader):
		raise Exception( 'No image reader support available!' )

	# Encapsulate the reader into the clipper
	clip = ClipReader( reader )
	return clip
