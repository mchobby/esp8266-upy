""" Test the Bmp class against the color-palette.bmp file to read the data. """

from bmp import BmpReader
from img import ClipReader, open_image

def test_header( filename ):
	f = open( filename, "rb" )
	bmp = BmpReader( f, check=False ) # Disable check compatibility. So can display header info

	print( 'Image size (WxH) : %i x %i' % (bmp.width,bmp.height))
	print( 'Startbit @     : %i' % bmp.startbit )
	print( 'Bit Per Pixels : %i' % bmp.bpp )
	print( 'Compression    : %i' % bmp.compression )
	print( 'Colors used    : %i (for indexed colors)' % bmp.colors_used  )
	f.close()

def test_24bit_bitmap( filename ):
	f = open( filename, "rb" )
	bmp = BmpReader( f )

	print( 'Image size (WxH) : %i x %i' % (bmp.width,bmp.height))
	# Bitmap may have padding bytes in the file, so seek_pix is required before reading each line
	print( '--- Line 1 ---' )
	for i in range( bmp.width ):
		print( "%i : %s" % ( i, bmp.read_pix() ) )
	print( '--- Line 2 ---' )
	bmp.seek_pix( (0,1) ) # x=0, y=1 --> 2th line
	for i in range( bmp.width ):
		print( "%i : %s" % ( i, bmp.read_pix() ) )

	print( '--- Line 6 ---' )
	# Move file cursor to a given pixel
	bmp.seek_pix( (0,5) ) # x=0, y=5 --> 6th line
	for i in range( bmp.width ):
		print( "%i : %s" % ( i, bmp.read_pix() ) )

	f.close()

def test_clip_reading( filename, area1, area2 ):
	""" Perform the reading of a part of the image """
	f = open( filename, "rb" )
	bmp = BmpReader( f )

	clip = ClipReader( bmp )
	for x,y,w,h in [area1,area2]: # area are tuple of (x,y,w,h)
		clip.clip( x,y,w,h  ) # 31,0,6,2 for x,y,width,height
		for i in range(clip.height):
			print( "--- Clipped line %i ---" % i )
			for j in range(clip.width):
				print( "%3i : %s" %(j,clip.read_pix()) )

	f.close()

def test_open_image( filename ):
	""" Test the open_image helper """
	# open_image() returns a ClipReader objet
	clip = open_image( filename )
	clip.clip( 31,0,6,2 ) # x,y, w, h
	for i in range( clip.width ):
		print( "-------------" )
		for j in range( clip.height ):
			print( "(%i,%i) : %s" % (i,j,clip.read_pix()) ) #x,y, color
	clip.close()

# == Test 24 bit uncompressed BMP image ==
#test_header( "color-palette.bmp" )
#test_24bit_bitmap( "color-palette.bmp" )

# == Test clipping ==
# the area clipping (with several areas)
#test_clip_reading( "color-palette.bmp", area1=(31,0,6,2), area2=(68,21,4,2) )

# == Test open_image helper ==
test_open_image( "color-palette.bmp" )
