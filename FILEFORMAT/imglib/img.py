""" Toolbox function for the various image reader """

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

	def clip( self, x, y, width, height ):
		""" Set the clipping area and get ready to read the first pixel """
		assert x>=0 and y>=0 and width>0 and height>0
		if not( 0<= x < self.reader.width ):
			raise Exception( "Invalid x = %i" % x )
		if not( 0<= y < self.reader.height ):
			raise Exception( "Invalid y = %i" % y )
		if not( 0<= x+width < self.reader.width ):
			raise Exception( "Invalid width = %i" % width )
		if not( 0<= y+height < self.reader.height ):
			raise Exception( "Invalid height = %i" % height )
		self.area = (x, y, x+width, y+height )
		self.width = width  # Clipping area width
		self.height= height # Clipping area height
		self.x, self.y = x, y # x,y position read in the whome image
		self.reader.seek_pix( (self.x, self.y) )


def open_image( filename ):
	""" Helper that detect image type based on file extension. Open the appropriate
	    image reader (eg: BmpReader) and then the ClipReader over the reader.
	    a ClipReader on the target image """
	reader = None
	if '.bmp' in filename:
		_f = open( filename, "rb" )
		from bmp import BmpReader
		reader = BmpReader( _f )
	if not(reader):
		raise Exception( 'No image reader support available!' )

	# Encapsulate the reader into the clipper
	clip = ClipReader( reader )
	return clip
