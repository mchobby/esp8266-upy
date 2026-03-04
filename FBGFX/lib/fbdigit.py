# FrameBuffer Digit Blitter - draw digit onto a target FrameBuffer
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
#
# Author: Meurisse Dominique
#
# Remarks:
#  Digit segments are organized as follow:
#
#   --A--
#  |     |
#  F     B
#  |     |
#   --G--
#  |     |
#  E     C
#  |     |
#   --D--
#
import math, framebuf, array

__version__ = '0.0.1'

class Size:
	__slot__ = ['w', 'h']
	
	def __init__(self, w, h ):
		self.w = w
		self.h = h

class DigitBlitter2538Mono:
	""" Blit 25 x 38px MonoChrome Digits on FrameBuffer. 
	    Design based on Pixel Madness Font """
	def __init__( self, target_fb, format ):
		""" format: target FrameBuffer format (depending on the OLED used) """
		self.target_fb = target_fb
		self.h=38        # Font size
		self.w=25        # Normal Width  (the digit)
		self.w_short = 5 # Shorter Width (eg: colon)
		self.spacing = 4 # Spacing between chars

		def create_fb( size ):
			if format==framebuf.MONO_VLSB:
				h = math.ceil(size.h/8)*8
				w = size.w
			elif format==framebuf.MONO_HLSB:
				h = size.h
				w = math.ceil(size.w/8)*8
			else:
				raise NotImplementedError( 'framebuffer format %s' % format )
			return framebuf.FrameBuffer( bytearray( math.ceil(w*h/8) ), size.w, size.h, format )
		# Segment A..G of a digit
		fb_a = create_fb( Size(19,5) )
		fb_b = create_fb( Size(5,17) )
                fb_c = create_fb( Size(5,17) )
                fb_d = create_fb( Size(19,5) )
                fb_e = create_fb( Size(5,17) )
                fb_f = create_fb( Size(5,17) )
                fb_g = create_fb( Size(17,6) )
		# Draw elements
		fb_a.poly(0,0, array.array('h',[0,0, 19,0, 14,5,  5,5, 0,0]), 1, 1)
		fb_b.poly(0,0, array.array('h',[5,0, 5,14, 3,16, 0,13, 0,5, 0,5]), 1, 1)
		fb_c.poly(0,0, array.array('h',[0,3,  3,0,  5,2, 5,16, 0,11, 0,3]), 1, 1)
		fb_d.poly(0,0, array.array('h',[0,5,  5,0, 14,0, 19,5, 0,5]), 1, 1)
		fb_e.poly(0,0, array.array('h',[0,2,  2,0,  5,3, 5,11, 0,16, 0,2]), 1, 1)
		fb_f.poly(0,0, array.array('h',[0,0,  5,5, 5,13, 2,16, 0,14, 0,0]), 1, 1)
		fb_g.poly(0,0, array.array('h',[0,3,  3,0, 12,0, 15,3, 12,6, 3,6, 0,3 ]), 1, 1)
		# colon definition
		fb_colon = create_fb( Size(5,20) )
		fb_colon.rect(0,0,5,5,1,1)
		fb_colon.rect(0,15,5,5,1,1)
		# Segments from a to G with their relatives x,y positions
		self.segments = [ (fb_a,3,0), (fb_b,20,1), (fb_c,20,20), (fb_d,3,33), (fb_e,0,20), (fb_f,0,1), (fb_g,5,15) ]
		self.colon = (fb_colon,0,9)
		# Digit definition 0..9 : each segment from A=0 to G=6
		self.ddef = { 0: [0,1,2,3,4,5], 1:[1,2], 2:[0,1,3,4,6], 3:[0,1,2,3,6], 4:[1,2,5,6], 5:[0,2,3,5,6], 6:[0,2,3,4,5,6],
				7:[0,1,2], 8:[0,1,2,3,4,5,6], 9:[0,1,2,3,5,6] }

	def blit_digit( self, x, y, digit ):
		""" Blit the digit at position x,y in the target fb """
		seg_indexes = self.ddef[digit]
		for seg_index in self.ddef[digit]:
			fb, x_off, y_off = self.segments[seg_index]
			self.target_fb.blit( fb, x+x_off, y+y_off, 0 )

	def blit_colon( self, x, y ):
		fb, x_off, y_off = self.colon
		self.target_fb.blit( fb, x+x_off, y+y_off, 0)

	def blit_time( self, x, y, h, m, s=None, colon=True ):
		hh = h // 10
		hl = h % 10
		mh = m // 10
		ml = m % 10
		if s!=None:
			raise NotImplementedError('Seconds not yet implemented')
		self.blit_digit( x, y, hh )
		x += self.w + self.spacing
		self.blit_digit( x, y, hl )
		x += self.w + self.spacing
		if colon:
			self.blit_colon( x, y )
		x += self.w_short + self.spacing
		self.blit_digit( x, y, mh )
		x += self.w + self.spacing
		self.blit_digit( x, y, ml )


