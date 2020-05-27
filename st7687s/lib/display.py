# The MIT License (MIT)
#
# Copyright (c) 2020 Meurisse D. from MC Hobby (shop.mchobby.be)
#

"""
display.py : Helper class used to draw object directly into the Buffer Memory of the LCD.

* Author(s):
   21 apr 2020: Meurisse D. (shop.mchobby.be) - portage from Arduino code
   17 aug 2018: DFRobot Arduino's version - https://github.com/DFRobot/DFRobot_Display/blob/master/DFRobot_Display.h

"""
__version__ = '0.0.1'

from math import sqrt
from character import get_character

DISPLAY_BLACK       = 0x0000  #   0,   0,   0
DISPLAY_NAVY        = 0x000F  #   0,   0, 128
DISPLAY_DARKGREEN   = 0x03E0  #   0, 128,   0
DISPLAY_DARKCYAN    = 0x03EF  #   0, 128, 128
DISPLAY_MAROON      = 0x7800  # 128,   0,   0
DISPLAY_PURPLE      = 0x780F  # 128,   0, 128
DISPLAY_OLIVE       = 0x7BE0  # 128, 128,   0
DISPLAY_LIGHTGREY   = 0xC618  # 192, 192, 192
DISPLAY_DARKGREY    = 0x7BEF  # 128, 128, 128
DISPLAY_BLUE        = 0x001F  #   0,   0, 255
DISPLAY_GREEN       = 0x07E0  #   0, 255,   0
DISPLAY_CYAN        = 0x07FF  #   0, 255, 255
DISPLAY_RED         = 0xF800  # 255,   0,   0
DISPLAY_MAGENTA     = 0xF81F  # 255,   0, 255
DISPLAY_YELLOW      = 0xFFE0  # 255, 255,   0
DISPLAY_WHITE       = 0xFFFF  # 255, 255, 255
DISPLAY_ORANGE      = 0xFD20  # 255, 165,   0
DISPLAY_GREENYELLOW = 0xAFE5  # 173, 255,  47
DISPLAY_PINK        = 0xF81F

DIRECTION_VERTICAL   = 1
DIRECTION_HORIZONTAL = 2

def calc_line_direction( point0, point1 ):
	if abs(abs(point0[0]) - abs(point1[0])) > abs(abs(point0[1]) - abs(point1[1])):
		return DIRECTION_VERTICAL
	return DIRECTION_HORIZONTAL

class Display:
	def __init__( self, st7687s_driver, width, height ):
		self.lcd = st7687s_driver # Driver to the round lcd
		self._raw_width = width # screen width
		self._raw_height = height
		self.xprint = 0 # CURSOR position for printing in relative coordonate
		self.yprint = 0
		self._text_bg = DISPLAY_BLACK
		self._text_fg = DISPLAY_WHITE
		self._text_size = 1
		self.set_origin( width//2, height//2 ) # Set the new origin in the moddle of the screen

	@property
	def text_bg( self ):
		return self._text_bg

	@text_bg.setter
	def text_bg( self, value ):
		self._text_bg = value

	@property
	def text_fg( self ):
		return self._text_fg

	@text_fg.setter
	def text_fg( self, value ):
		self._text_fg = value

	@property
	def text_size( self ):
		return self._text_size

	@text_size.setter
	def text_size( self, value ):
		self._text_size = value

	@property
	def raw_width(self):
		return self._raw_width
	@property
	def raw_height(self):
		return self._raw_height

	def set_origin( self, x, y ):
		""" Mofify the axis origin for drawin """
		self.x_offset = x
		self.y_offset = y
		self.width  = (self._raw_width-x)
		self.height = (self._raw_height-y)

	def limit_pixel( self, point ):
		""" Limit pixel drawing. point (x,y) relative to origin. None value are ignored """
		if point[0] and not( 0 <= self.y_offset+point[0] < self._raw_width ):
			return True # Limit Pixel Drawing
		if point[1] and not( 0 <= self.y_offset+point[1] < self._raw_width ):
			return True # Limit Pixel Drawing
		return False

	def pixel( self, point, color ):
		""" point (x,y) relative to the origin (top-left) """
		if self.limit_pixel( point ):
			return
		self.lcd.setCursorAddr(self.x_offset+point[0], self.y_offset+point[1], self.x_offset+point[0], self.y_offset+point[1] )
		self.lcd.writeToRam()
		colorBuf = bytes( [(color >> 8) & 0xFF, color & 0xFF] )
		self.lcd.writeDatBytes(colorBuf)

	def pixel_width( self, point, eDirection, width, color ):
		if width == 1 :
			self.pixel( point, color )
		elif width > 1:
			if eDirection == DIRECTION_HORIZONTAL:
				self.hline( (point[0]-(width/2), point[1]), width, color )
			else:
				self.vline( (point[0], point[1]-(width/2)), width, color )

	def clear( self, color=0x0000 ):
		""" Optimized version of fill_screen """
		# do not fill the 21% of area inivisble to the user!
		# Save 1.12 sec from the 6.84 sec needed for fill_screen
		# Gain: 16.25% in time :-)
		for y in range( 2, 65, 2 ):
			lwidth = int( 2*sqrt(4096-pow(64-(y+2),2)) )
			if lwidth % 2:
				lwidth += 1 # multiple of 2 required!
			# Fill line from top
			xstart = (128-lwidth)//2
			# Top part
			self.lcd.setCursorAddr( xstart, y-2, xstart+lwidth, y ) # Drawing 2 lines
			self.lcd.writeToRam()
			self.lcd.writeRepeatPixel(color,lwidth, 2) # Pixels for 2 lines
			# Bottom part
			self.lcd.setCursorAddr( xstart, 130-y-2, xstart+lwidth, 130-y ) # Drawing 2 lines
			self.lcd.writeToRam()
			self.lcd.writeRepeatPixel(color,lwidth, 2) # Pixels for 2 lines

	def fill_screen( self, color ):
		""" Fill screen with a color (see clear for optimized version) """
		# Original from DFRobot
		self.lcd.setCursorAddr(0, 0, self._raw_width-1, self._raw_height-1)
		self.lcd.writeToRam()
		self.lcd.writeRepeatPixel(color, self._raw_width, self._raw_height)

	def vline( self, point, height, color ):
		if self.limit_pixel( (point[0],None) ): # Only test X position
			return
		direction = -1 if height<0 else 1
		var1 = point[1] + height
		# for(; y != var1; y += direction) {
		y = point[1]
		while y!=var1:
			self.pixel( (point[0], y), color)
			y += direction


	def hline( self, point, width, color ):
		if self.limit_pixel( (None,point[1]) ): # Only test Y position
			return
		direction = -1 if width<0 else 1
		var1 = point[0] + width
		#for(; x != var1; x += direction) {
		x = point[0]
		while( x != var1 ):
			self.pixel( (x,point[1]) , color)
			x += direction

	def line( self, point0, point1, color ):
		dx = abs(point1[0] - point0[0])
		dy = abs(point1[1] - point0[1])
		steep = 0

		eDirection = calc_line_direction( point0, point1)
		if dx < dy:
			steep = 1
			point0 = (point0[1],point0[0])
			point1 = (point1[1],point1[0])
			dx, dy = dy, dx

		dirX = 1 if (point1[0] - point0[0]) > 0 else -1
		dirY = 1 if (point1[1] - point0[1]) > 0 else -1
		endX = point0[0]
		endY = point0[1]
		var1 = dy * 2
		var2 = (dy - dx) * 2
		var3 = dy * 2 -dx

		if steep:
			while endX != point1[0]:
				if var3 < 0 :
					var3 += var1
				else:
					endY += dirY
					var3 += var2

				# drawPixel(endY, endX, color);
				self.pixel_width( (endY,endX), eDirection, 1, color)
				endX += dirX
		else:
			while endX != point1[0]:
				if var3 < 0:
					var3 += var1
				else:
					endY += dirY
					var3 += var2

				# drawPixel(endX, endY, color);
				self.pixel_width( (endX, endY), eDirection, 1, color)
				endX += dirX

	def circle( self, point , r, color ):
		r = abs(r)
		varX = 0
		varY = r
		endY = 0
		var1 = 3 - 2 * r

		while varX <= varY:
			self.pixel( (point[0] + varX, point[1] + varY), color)
			self.pixel( (point[0] - varX, point[1] + varY), color)
			self.pixel( (point[0] + varX, point[1] - varY), color)
			self.pixel( (point[0] - varX, point[1] - varY), color)
			self.pixel( (point[0] + varY, point[1] + varX), color)
			self.pixel( (point[0] - varY, point[1] + varX), color)
			self.pixel( (point[0] + varY, point[1] - varX), color)
			self.pixel( (point[0] - varY, point[1] - varX), color)
			if var1 < 0:
				var1 = var1 + 4 * varX + 6
			else:
				var1 = var1 + 4 * (varX - varY) + 10
				varY -= 1
			varX += 1

	def fill_circle( self, point, r, color ):
		r = abs(r)
		varX = 0
		varY = r
		endY = 0
		var1 = 3 - 2 * r

		while varX <= varY:
			self.vline( (point[0]+varX, point[1]-varY), 2 * varY + 1, color)
			self.vline( (point[0]+varY, point[1]-varX), 2 * varX + 1, color)
			self.vline( (point[0]-varX, point[1]-varY), 2 * varY + 1, color)
			self.vline( (point[0]-varY, point[1]-varX), 2 * varX + 1, color)
			if var1 < 0:
				var1 = var1 + 4 * varX + 6
			else:
				var1 = var1 + 4 * (varX - varY) + 10
				varY -= 1
			varX += 1

	def triangle( self, point0, point1, point2, color):
		self.line( point0, point1, color )
		self.line( point1, point2, color )
		self.line( point2, point0, color )

	def fill_triangle( self, point0, point1, point2, color):
		self.line( point0, point1, color)
		self.line( point1, point2, color)
		self.line( point2, point0, color)
		# reuse variable names as in the original C code
		x, y = point0
		x1, y1 = point1
		x2, y2 = point2

		if (x == x1) and (x == x2):
			ymax = max(y,y1,y2)
			ymin = min(y,y1,y2)
			self.hline( (x, ymin), ymax - ymin, color)
			return
		if (y == y1) and (y == y2):
			xmax = max(y,y1,y2)
			xmin = min(y,y1,y2)
			self.hlLine( (xmin, y), xmax - xmin, color)
			return


		direction = 1
		if (y==y1) or (y1==y2) or (y==y2):
			if (y==y1):
				x, x2 = x2,x
				y, y2 = y1,y
			elif y==y2 :
				x,x1 = x1,x
				y,y1 = y1,y
			if y > y1:
				direction = -1

			if x1 > x2:
				x1, x2 = x2, x
				y1, y2 = y2, y1
		else:
			if y > y1:
				x, x1 = x1, x
				y, y1 = y1, y
			if y > y2:
				x, x2 = x2, x
				y, y2 = y2, y
			if y1 > y2:
				x1, x2 = x2, x1
				y1, y2 = y2, y1

		dx1 = x1 - x
		dx2 = x2 - x
		dx3 = x2 - x1
		dy1 = y1 - y
		dy2 = y2 - y
		dy3 = y2 - y1
		if direction == 1:
			for i in range( dy1 ):
				self.hline( ( int(x + dx1 * i / dy1), y+i ), int((x + dx2 * i / dy2) - (x + dx1 * i / dy1) + 1), color)
			for i in range( dy3 ):
				self.hline( (int(x1 + dx3 * i / dy3), y1 + i), int((x + dx2 * (i + dy1) / dy2) - (x1 + dx3 * i / dy3) + 1), color)
		else:
			y = y1 + dy1
			dy1 = - dy1
			for i in range( dy1 ):
				self.hline( (int(x + dx1 * i / dy1), y1 + dy1 - i), int((x + dx2 * i / dy1) - (x + dx1 * i / dy1) + 1), color)

	def rect( self, point, width, height, color ):
		dirX = -1 if width > 0 else 1
		dirY = -1 if height > 0  else 1
		self.hline( point, width, color)
		self.hline( (point[0],point[1]+height+dirY) , width, color)
		self.vline( point, height, color )
		self.vline( (point[0]+width+dirX, point[1]) , height, color)

	def fill_rect( self, point, width, height, color ):
		directionX = 1
		x = point[0]
		var1 = x + width
		if width < 0:
			directionX = -1
		while x!=var1:
			self.vline( (x,point[1]), height, color )
			x += directionX


	def set_cursor( self, point ):
		""" The point coordonate are relative to the screen origin. """
		if  0 <= abs(point[0]) <= self.width :
			self.xprint = point[0]
		if  0 <= abs(point[1]) <= self.height :
			self.yprint = point[1]

	def get_cursor( self ):
		return (self.xprint,self.yprint)

	def print( self, s ):
		for ch in s:
			width,height = self.draw_char( self.xprint, self.yprint, ch )
			# Move cursor
			self.xprint += width

	def draw_char( self, x, y , ch ):
		""" Low level function to draw text @ absolute coordinate """
		charBuf = None
		i = 0
		j = 0
		k = 0
		var1 = 0
		textWidth = 0
		textHeight = 0

		#print( x,y,ch )
		charBuf, charWidth, charHeight = get_character( ch )
		self.fill_rect( (x,y),charWidth,charHeight, self._text_bg  )

		# No character Drawing
		if not charBuf:
			return charWidth, charHeight

		# Draw the character
		#	Codification for A = 0x7C,0x12,0x11,0x12,0x7C,0x00
		#	0x7C  .11111..
		#	0x12  ...1..1.
		#	0x11  ...1...1
		#	0x12  ...1..1.
		#	0x7C  .11111..
		#	0x00  ........
		for x_pos in range(len(charBuf)):
			bits = charBuf[x_pos]
			for y_pos in range(8):
				a_bit = (bits & (1<<y_pos))>0
				# pixel position & pixel size
				xstart = x+(x_pos*self.text_size)
				ystart = y+(y_pos*self.text_size)
				if a_bit:
					if self.text_size==1:
						self.pixel( (xstart,ystart), self.text_fg )
					else:
						self.fill_rect( (xstart,ystart), self.text_size, self.text_size, self.text_fg )

		# return the drawing size
		return charWidth*self.text_size, charHeight*self.text_size
