
def grayscale( r,g,b ):
	""" Compute grayscale (brightness) 0..232 from r,g,b values (0..255) """
	return int( 0.3*r + 0.6*g + 0.11*b ) # darker image can be created with 0.25*r + 0.5*g + 0.25*b

def charpix( r,g,b ):
	""" Compute a char ' .-+*X' in relation with the grayscale luminosity of a pixel.
	    Would allow to display rudimentary picture on terminal """
	pc = int( grayscale(r,g,b) / 25.5 * 10 ) # In percent for a range 0..255
	return "  ..-+**XXX"[pc//10]
