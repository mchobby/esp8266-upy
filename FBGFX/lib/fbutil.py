# FrameBuffer utility class with additional drawing functions

__version__ = '0.0.1'

import math

class FBUtil:
	def __init__(self, fb ):
		self.fb = fb

	def _peri_x(self, x, degrees, radius):
		sin = math.sin(math.radians(degrees))
		x = int(x+(radius*sin))
		return x

	def _peri_y(self, y, degrees, radius):
		cos = math.cos(math.radians(degrees))
		y = int(y-(radius*cos))
		return y

	def circle( self, x, y, radius, color, border=1, degrees=360, startangle=0):
		border = 5 if border > 5 else border
		# adding startangle to degrees
		if startangle > 0:
			degrees += startangle
		if border > 1:
			x = x - border//2
			y = y - border//2
			radius = radius-border//2
		for i in range(startangle, degrees):
			X = self._peri_x(x, i, radius)
			Y = self._peri_y(y, i, radius)
			if   i == 90:  X = X-1
			elif i == 180: Y = Y-1
			if border==1:
				self.fb.pixel( X,Y, color )
			else:
				self.fb.rect(X, Y, border, border, color )

	def fill_circle(self, x, y, radius, color):
		tempY = 0
		for i in range(180):
			xNeg = self._peri_x(x, 360-i, radius-1)
			xPos = self._peri_x(x, i, radius)
			if i > 89:
				Y = self._peri_y(y, i, radius-1)
			else:
				Y = self._peri_y(y, i, radius+1)
			if i == 90: xPos = xPos-1
			if tempY != Y and tempY > 0:
				length = xPos+1
				self.fb.hline(xNeg, Y, length-xNeg, color, tick=4)
			tempY = Y

	def oval( self, x, y, xradius, yradius, color, border=1, degrees=360, startangle=0):
		border = 5 if border > 5 else border
		# adding startangle to degrees
		if startangle > 0:
			degrees += startangle
		if border > 1:
			x = x - border//2
			y = y - border//2
			xradius = xradius-border//2
			yradius = yradius-border//2
		for i in range(startangle, degrees):
			X = self._peri_x(x, i, xradius)
			Y = self._peri_y(y, i, yradius)
			if   i == 90:  X = X-1
			elif i == 180: Y = Y-1
			if border==1:
				self.fb.pixel( X,Y, color )
			else:
				self.fb.rect(X, Y, border, border, color )

	def fill_oval( self, x, y, xradius, yradius, color ):
		tempY = 0
		for i in range(180):
			xNeg = self._peri_x(x, 360-i, xradius)
			xPos = self._peri_x(x, i, xradius)
			Y    = self._peri_y(y, i, yradius)

			if i > 89: Y = Y-1
			if tempY != Y and tempY > 0:
				length = xPos+1
				self.fb.hline(xNeg, Y, length-xNeg, color, tick=4)
			tempY = Y

	def rrect( self, x,y, width, height, radius, color ):
		assert (2*radius) < height
		assert (2*radius) < width
		self.circle( x+radius, y+radius, radius, color, border=1, degrees=90, startangle=270)
		self.fb.hline( x+radius, y, width-(2*radius), color )
		self.circle( x+width-radius, y+radius, radius, color, border=1, degrees=90, startangle=0)
		self.fb.vline( x+width-1, y+radius, height-(2*radius), color )
		self.circle( x+width-radius, y+height-radius, radius, color, border=1, degrees=90, startangle=90)
		self.fb.hline( x+radius+1, y+height, width-(2*radius), color )
		self.circle( x+radius, y+height-radius, radius, color, border=1, degrees=90, startangle=180)
		self.fb.vline( x, y+radius+1, height-(2*radius)-1, color )

	def fill_rrect( self, x,y, width, height, radius, color ):
		assert (2*radius) < height
		assert (2*radius) < width
		self.fb.fill_rect( x+1, y+radius, width, height-(2*radius)+1, color )
		self.fb.fill_rect( x+radius, y, width-(2*radius)+1, radius, color )
		self.fb.fill_rect( x+radius, y+height-radius+1, width-(2*radius), radius+1, color )
		self.fill_circle( x+radius, y+radius, radius, color)
		self.fill_circle( x+width-radius, y+radius, radius, color)
		self.fill_circle( x+width-radius, y+height-radius, radius, color)
		self.fill_circle( x+radius, y+height-radius, radius, color)
