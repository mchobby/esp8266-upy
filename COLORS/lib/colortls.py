
def grayscale( r,g,b ):
	""" Compute grayscale (brightness) 0..232 from r,g,b values (0..255) """
	return int( 0.3*r + 0.6*g + 0.11*b ) # darker image can be created with 0.25*r + 0.5*g + 0.25*b

def charpix( r,g,b ):
	""" Compute a char ' .-+*X' in relation with the grayscale luminosity of a pixel.
	    Would allow to display rudimentary picture on terminal """
	pc = int( grayscale(r,g,b) / 25.5 * 10 ) # In percent for a range 0..255
	return "  ..-+**XXX"[pc//10]

# From ColorSys @ https://raw.githubusercontent.com/python/cpython/2.7/Lib/colorsys.py
# HSV: Hue, Saturation, Value
# H: position in the spectrum
# S: color saturation ("purity")
# V: color brightness
def rgb_to_hsv(r, g, b):
	maxc = max(r, g, b)
	minc = min(r, g, b)
	v = maxc
	if minc == maxc:
		return 0.0, 0.0, v
	s = (maxc-minc) / maxc
	rc = (maxc-r) / (maxc-minc)
	gc = (maxc-g) / (maxc-minc)
	bc = (maxc-b) / (maxc-minc)
	if r == maxc:
		h = bc-gc
	elif g == maxc:
		h = 2.0+rc-bc
	else:
		h = 4.0+gc-rc
	h = (h/6.0) % 1.0
	return h, s, v

def hsv_to_rgb(h, s, v):
	if s == 0.0:
		return v, v, v
	i = int(h*6.0) # XXX assume int() truncates!
	f = (h*6.0) - i
	p = v*(1.0 - s)
	q = v*(1.0 - s*f)
	t = v*(1.0 - s*(1.0-f))
	i = i%6
	if i == 0:
		return v, t, p
	if i == 1:
		return q, v, p
	if i == 2:
		return p, v, t
	if i == 3:
		return p, q, v
	if i == 4:
		return t, p, v
	if i == 5:
		return v, p, q
	# Cannot get here
