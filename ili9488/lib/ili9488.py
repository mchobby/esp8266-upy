# See LICENSE.txt file
# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
#
# MIMIC the ILI934x API @ https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# Remarks:
#    Driver defines color as 16 bits (RGB565, rrrrrggg gggbbbbb)
#    Hardware controler receives color as 18 bits (rrrrr000 gggggg00 bbbbb000)
from micropython import const
import ustruct
import framebuf
import math
import time

__version__ = '0.0.2'

READ_DISPLAY       = const(0x0f)
SLEEP_OUT          = const(0x11)
GAMMA_SET          = const(0x26)
DISPLAY_ON         = const(0x29)
COLUMN_ADDRESS_SET = const(0x2a)
PAGE_ADDRESS_SET   = const(0x2b)
RAM_WRITE          = const(0x2c)
RAM_READ           = const(0x2e)
MEMORY_ACCESS_CONTROL = const(0x36)
VER_SCROLL_ADDRESS    = const(0x37) # Vertical Scrolling Start Address
PIXEL_FORMAT_SET      = const(0x3a)
POWER_CONTROL_A       = const(0xcb)
POWER_CONTROL_B       = const(0xcf)
DRIVER_TIMING_CONTROL_A = const(0xe8)
DRIVER_TIMING_CONTROL_B = const(0xea)
POWER_ON_CONTROL      = const(0xed)
PUMP_RATIO_CONTROL    = const(0xf7)  # Pump Ratio Control
POWER_CONTROL_1       = const(0xc0)  # Power Control 1
POWER_CONTROL_2       = const(0xc1)  # Power Control 2
VCOM_CONTROL_1        = const(0xc5)  # VCOM Control 1
VCOM_CONTROL_2        = const(0xc7)
FRAME_RATE_CONTROL_1     = const(0xB1)# Frame Rate Control 1
FRAME_RATE_CONTROL_2     = const(0xb2)
DISPLAY_INVERSION        = const(0xB4) # Display RGB column Inversion control
DISPLAY_FUNCTION_CONTROL = const(0xb6) # Display Function Control
ENTRY_MODE_SET           = const(0xB7) # Entry Mode Set
HS_LANE_CTRL             = const(0xBE) # HS Lanes Control
ENABLE_3G                = const(0xf2)
POS_GAMMA_CONTROL        = const(0xe0)
NEG_GAMMA_CONTROL        = const(0xe1)
SET_IMAGE_FCT            = const(0xE9) # Set Image Function

MEMORY_BUFFER = const(256) # SPI Write Buffer (best performances for 256 bytes/color buffer)

# Basic colors
BLACK       = const(0x0000)
NAVY        = const(0x0010)
DARKGREEN   = const(0x0400)
DARKCYAN    = const(0x0410)
MAROON      = const(0x8000)
PURPLE      = const(0x8010)
OLIVE       = const(0x8400)
LIGHTGREY   = const(0xc618)
DARKGREY    = const(0x8410)
BLUE        = const(0x001f)
GREEN       = const(0x07e0)
CYAN        = const(0x07ff)
RED         = const(0xf800)
MAGENTA     = const(0xf81f)
YELLOW      = const(0xffe0)
WHITE       = const(0xffff)
ORANGE      = const(0xfd20)
GREENYELLOW = const(0xafe5)

def color565(r, g, b):
	return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

class ILI9488:
	def __init__(self, spi, cs, dc, rst, w=320, h=480, r=0):
		self.spi = spi;
		self.cs = cs;
		self.dc = dc;
		self.rst = rst
		self._init_width = w
		self._init_height = h
		self.width = w
		self.height = h
		self.rotation = r
		self.cs.init(self.cs.OUT, value=1)
		self.dc.init(self.dc.OUT, value=0)
		self.rst.init(self.rst.OUT, value=0)
		self.reset()
		self.init()
		self._buf = bytearray(MEMORY_BUFFER * 3) # color encoded on 18 bits
		self._colormap = bytearray(b'\x00\x00\xFF\xFF') # RGB565 : white foreground [0..1], black background [2..3]
		self._fg_c18bit = bytearray(3) # Encoding buffer for 18bits color
		self._bg_c18bit = bytearray(3) # Encoding buffer for 18bits color
		self._x = 0
		self._y = 0

		self._scroll = 0
		self._font = None # print() : font
		self._pbuf = None # print() : Buffer for Print statement
		self._pfb  = None # print() : FrameBuf for Print statement
		self.scrolling = False

	def init( self ):
		self.cs.value( 0 ) # CS

		for command, data in (
				(PUMP_RATIO_CONTROL, b"\xA9\x51\x2C\x82" ),
				(POWER_CONTROL_1, b"\x11\x09" ),
				(POWER_CONTROL_2, b"\x41" ),
				(VCOM_CONTROL_1, b"\x00\x0A\x80" ),
				(FRAME_RATE_CONTROL_1, b"\xB0\x11" ),
				(DISPLAY_INVERSION, b"\x02" ),
				(DISPLAY_FUNCTION_CONTROL, b"\x02\x22" ),
				(ENTRY_MODE_SET, b"\xC6" ),
				(HS_LANE_CTRL, b"\x00\x04" ),
				(SET_IMAGE_FCT, b"\x00" ) ):
			self._write(command, data)

		if self.rotation == 0:                  # 0 deg - portrait
			self._write(MEMORY_ACCESS_CONTROL, b"\x08")
			self.width,self.height = self._init_width,self._init_height
		elif self.rotation == 1:                # 90 deg - Landscape
			self._write(MEMORY_ACCESS_CONTROL, b"\x68")
			self.width,self.height = self._init_height,self._init_width
		elif self.rotation == 2:                # 180 deg - portrait
			self._write(MEMORY_ACCESS_CONTROL, b"\xC8")
			self.width,self.height = self._init_width, self._init_height
		elif self.rotation == 3:                # 270 deg - landscape
			self._write(MEMORY_ACCESS_CONTROL, b"\xA8")
			self.width,self.height = self._init_height, self._init_width
		elif self.rotation == 4:                # 0 deg - portrait + mirroring
			self._write(MEMORY_ACCESS_CONTROL, b"\x48")
			self.width,self.height = self._init_width,self._init_height
		elif self.rotation == 5:                # 90 deg - Landscape + mirroring
			self._write(MEMORY_ACCESS_CONTROL, b"\xE8")
			self.width,self.height = self._init_height,self._init_width
		elif self.rotation == 6:                # 180 deg - portrait + mirroring
			self._write(MEMORY_ACCESS_CONTROL, b"\x88")
			self.width,self.height = self._init_width, self._init_height
		elif self.rotation == 7:                # 270 deg - landscape + mirroring
			self._write(MEMORY_ACCESS_CONTROL, b"\x28")
			self.width,self.height = self._init_height, self._init_width
		else:
			raise Exception('rotation not in 0..7')

		# 18 bits/pixel & Use the ili934x Gamma values
		for command, data in ( (PIXEL_FORMAT_SET, b"\x66" ), # 0x66 : 18 bits, 0x55 : 16 bits
					(GAMMA_SET, b"\x01" ),
					#ILI924x (POS_GAMMA_CONTROL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00" ),
					#ILI924x (NEG_GAMMA_CONTROL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f" )
					(POS_GAMMA_CONTROL, b"\x00\x07\x10\x09\x17\x0B\x41\x89\x4B\x0A\x0C\x0E\x18\x1B\x0F" ),
					(NEG_GAMMA_CONTROL, b"\x00\x17\x1A\x04\x0E\x06\x2F\x45\x43\x02\x0A\x09\x32\x36\x0F" )
					):
			self._write(command, data)

		self._write( SLEEP_OUT )
		time.sleep_ms(120)
		self._write( DISPLAY_ON )

		self.cs.value( 1 )


	def reset( self ):
		self.rst.value( 1 )
		time.sleep_ms(5)
		self.rst.value( 0 )
		time.sleep_ms(15)
		self.rst.value( 1 )
		time.sleep_ms(15)

	def _write(self, command, data=None):
		self.dc(0)
		#self.cs(0)
		self.spi.write(bytearray([command]))
		#self.cs(1)
		if data is not None:
			self._data(data)

	def _read(self, command, count):
		self.dc(0)
		self.spi.write(bytearray([command]))
		data = self.spi.read(count)
		return data

	def _data(self, data):
		self.dc(1)
		self.spi.write(data)

	#def _writeblock(self, x0, y0, x1, y1, data=None):
	#	self.cs.value(0)
	#	self._write(COLUMN_ADDRESS_SET, ustruct.pack(">HH", x0, x1))
	#	self._write(PAGE_ADDRESS_SET, ustruct.pack(">HH", y0, y1))
	#	self._write(RAM_WRITE, data)
	#	if data!=None: # Must be closed by the callee (sending multiple chunchs of data)
	#		self.cs.value(1)

	def _writeblock(self, x0, y0, x1, y1, data=None):
		# Optimized WriteBlock
		self.cs.value(0)
		self.dc(0)
		self.spi.write(COLUMN_ADDRESS_SET.to_bytes(1,'big'))
		self.dc(1)
		self.spi.write(ustruct.pack(">HH", x0, x1))

		self.dc(0)
		self.spi.write(PAGE_ADDRESS_SET.to_bytes(1,'big'))
		self.dc(1)
		self.spi.write(ustruct.pack(">HH", y0, y1))

		self.dc(0)
		self.spi.write(RAM_WRITE.to_bytes(1,'big'))
		if data is not None:
			self.dc(1)
			self.spi.write(data)
			self.cs.value(1)


	def _readblock(self, x0, y0, x1, y1, data=None):
		self.cs.value(0)
		self._write(COLUMN_ADDRESS_SET, ustruct.pack(">HH", x0, x1))
		self._write(PAGE_ADDRESS_SET, ustruct.pack(">HH", y0, y1))
		if data is None:
			_d = self._read(RAM_READ, (x1 - x0 + 1) * (y1 - y0 + 1) * 3)
			self.cs.value(1)
			return _d
		self.cs.value(1)

	def _set_18bit_color( self, color, foreground=True ):
		# init the _c18bit color from a 16 bit color parameter (or 2 byte color)
		if type(color) is int:
			c16bit = ustruct.pack(">HH", color )
		else:
			c16bit = color # already an array

		if foreground:
			self._fg_c18bit[0] = c16bit[0] & 0xF8
			self._fg_c18bit[1] = (( (c16bit[0] & 0b111)<<5 ) | (c16bit[1]>>3) ) & 0xFC
			self._fg_c18bit[2] = (c16bit[1]<<3) & 0xFF
		else:
			self._bg_c18bit[0] = c16bit[0] & 0xF8
			self._bg_c18bit[1] = (( (c16bit[0] & 0b111)<<5 ) | (c16bit[1]>>3) ) & 0xFC
			self._bg_c18bit[2] = (c16bit[1]<<3) & 0xFF


	def erase(self):
		self.fill_rect(0, 0, self.width, self.height)

	def fill( self, c ): # FrameBuffer mimic
		self.fill_rect( 0,0,self.width,self.height,c)

	def fill_rect(self, x, y, w, h, color=None):
		x = min(self.width - 1, max(0, x))
		y = min(self.height - 1, max(0, y))
		w = min(self.width - x, max(1, w))
		h = min(self.height - y, max(1, h))
		if color:
			color = ustruct.pack(">H", color)
		else:
			color = self._colormap[0:2] #background
		self._set_18bit_color( color )
		#self._fg_c18bit[0] = color[0] & 0xF8
		#self._fg_c18bit[1] = (( (color[0] & 0b111)<<5 ) | (color[1]>>3) ) & 0xFC
		#self._fg_c18bit[2] = (color[1]<<3) & 0xFF
		for i in range(MEMORY_BUFFER):
			self._buf[3*i]   = self._fg_c18bit[0]
			self._buf[3*i+1] = self._fg_c18bit[1]
			self._buf[3*i+2] = self._fg_c18bit[2]
		chunks, rest = divmod(w * h, MEMORY_BUFFER)
		self._writeblock(x, y, x + w - 1, y + h - 1, None)
		if chunks:
			for count in range(chunks):
				self._data(self._buf)
		if rest != 0:
			mv = memoryview(self._buf)
			self._data(mv[:rest*3])
		self.cs.value(1)

	def blit_mono( self, fbuf, x, y, w, h, colors ):
		# blit the fbuf monochrome buffer of x,y,w, h size to the FrameBuffer
		# colors contains a type of (fg_color, bg_color)
		# Useful to speed up print OR icon display of the TFT
		x = min(self.width - 1, max(0, x))
		y = min(self.height - 1, max(0, y))
		w = min(self.width - x, max(1, w))
		h = min(self.height - y, max(1, h))

		self._set_18bit_color( colors[0] )
		self._set_18bit_color( colors[1], foreground=False )

		self._writeblock(x, y, x + w - 1, y + h - 1, None)

		chunck_pos = 0
		pixel_pos = 0
		max_pixel = w*h

		while pixel_pos < max_pixel:
			y_pos, x_pos = divmod( pixel_pos, w )
			if fbuf.pixel(x_pos, y_pos)!=0:
				self._buf[3*chunck_pos]   = self._fg_c18bit[0]
				self._buf[3*chunck_pos+1] = self._fg_c18bit[1]
				self._buf[3*chunck_pos+2] = self._fg_c18bit[2]
			else:
				self._buf[3*chunck_pos]   = self._bg_c18bit[0]
				self._buf[3*chunck_pos+1] = self._bg_c18bit[1]
				self._buf[3*chunck_pos+2] = self._bg_c18bit[2]
				#print( i )
			chunck_pos += 1
			pixel_pos  += 1

			if chunck_pos == MEMORY_BUFFER:
				self._data(self._buf)
				chunck_pos = 0

		if chunck_pos > 0:
			mv = memoryview(self._buf)
			self._data(mv[:chunck_pos*3])

		self.cs.value(1)

	def set_color(self,fg,bg): # 16 bits color
		self._colormap[0] = bg>>8
		self._colormap[1] = bg & 255
		self._colormap[2] = fg>>8
		self._colormap[3] = fg & 255

	@property
	def color( self ):
		return (self._colormap[2] << 8) + self._colormap[3]

	@color.setter
	def color( self, value ):
		self._colormap[2] = value>>8
		self._colormap[3] = value & 255

	@property
	def bgcolor( self ):
		return (self._colormap[0] << 8) + self._colormap[1]

	@bgcolor.setter
	def bgcolor( self, value ):
		self._colormap[0] = value>>8
		self._colormap[1] = value & 255

	def set_pos(self,x,y):
		self._x = x
		self._y = y

	def pixel(self, x, y, color=None): # FrameBuffer mimic
		if color is None:
			r, b, g = self._readblock(x, y, x, y) # TODO: to check
			return color565(r>>3, g>>2, b>>3)
		if not 0 <= x < self.width or not 0 <= y < self.height:
			return
		self._set_18bit_color( color )
		self._writeblock(x, y, x, y, self._fg_c18bit )

	def hline( self, x,y,w, c, tick=1 ): # FrameBuffer mimic
		if (x+w) >= self.width: w = self.width-x
		if (w<=0) or (x>=self.width):
			return
		if tick > 10: tick = 10
		if (y+tick-1) > self.height: tick = self.height-y
		if tick<=0:
			return
		# fill the buffer with the color
		self.fill_rect( x,y, w, tick, c )

	def vline( self, x,y,h, c, tick=1 ): # Framebuffer Mimic
		if (y+h) >= self.height: h = self.height-y
		if (h<=0) or (y>=self.height):
			return
		if tick > 10: tick = 10
		if (x+tick-1) > self.width: tick = self.width-x
		if tick<=0:
			return
		self.fill_rect( x,y, tick, h, c )

	def line(self, x, y, x1, y1, color):
		if x==x1:
			self.vline( x, y if y<=y1 else y1, abs(y1-y), color )
		elif y==y1:
			self.hline( x if x<=x1 else x1, y, abs(x-x1), color )
		else:
			# keep positive range for x
			if x1 < x:
				x,x1 = x1,x
				y,y1 = y1,y
			r = (y1-y)/(x1-x)
			# select ratio > 1 for fast drawing (and thin line)
			if abs(r) >= 1:
				for i in range( x1-x+1 ):
					if (i==0): # first always a point
						self.pixel( x+i, math.trunc(y+(r*i)), color )
					else:
						# r may be negative when drawing to wrong way > Fix it when drawing
						self.vline( x+i, math.trunc(y+(r*i)-r)+(0 if r>0 else math.trunc(r)), abs(math.trunc(r)), color )
			else:
				# keep positive range for y
				if y1 < y:
					x,x1 = x1,x
					y,y1 = y1,y
				# invert the ratio (should be close of r = 1/r)
				r = (x1-x)/(y1-y)
				for i in range( y1-y+1 ):
					if( i== 0): # starting point is always a point
						self.pixel( math.trunc(x+(r*i)), y+i, color )
					else:
						# r may be negative when drawing the wrong way > fix it to draw positive
						self.hline( math.trunc(x+(r*i)-r)+(0 if r>0 else math.trunc(r)), y+i, abs(math.trunc(r)), color )

	@property
	def font( self ):
		return self._font

	@property
	def font_name( self ):
		return self._font_name

	@font_name.setter
	def font_name( self, value ):
		self._font_name = value
		# print_buffer, print_FrameBuffer, FontDrawer
		import fdrawer
		self._font = fdrawer.FontDrawer( frame_buffer=None, font_name=self._font_name )
		# Buffer height must be a multiple of height bits
		px_height = self._font.font.height+self._font.font.descender
		byte_height = px_height//8
		if (px_height%8) != 0:
			byte_height += 1
		self._pbuf = bytearray( byte_height*self.width )
		self._pfb = framebuf.FrameBuffer(self._pbuf,self.width,self._font.font.height+self._font.font.descender, framebuf.MONO_VLSB )
		self._font.fb = self._pfb # Font must be drawed to a custom FrameBuffer
		self._font.color = 1

	def scroll(self, dy):
		self._scroll = (self._scroll + dy) % self.height
		self._write(VER_SCROLL_ADDRESS, ustruct.pack(">H", self._scroll))

	def reset_scroll(self):
		self.scrolling = False
		self._scroll = 0
		self.scroll(0)

	def next_line(self, cury, char_h):
		global scrolling
		if not self.scrolling:
			res = cury + char_h
			self.scrolling = (res >= self.height)
		if self.scrolling:
			self.scroll(char_h)
			res = (self.height - char_h + self._scroll)%self.height
			self.fill_rect(0, res, self.width, self._font.height())
		return res

	def write(self, text): #does character wrap, compatible with stream output
		# TO BE CHECKED
		curx = self._x; cury = self._y
		char_h = self._font.height()
		width = 0
		written = 0
		for pos, ch in enumerate(text):
			if ch == '\n':
				if pos>0:
					self.chars(text[written:pos],curx,cury)
				curx = 0; written = pos+1; width = 0
				cury = self.next_line(cury,char_h)
			else:
				char_w = self._font.get_width(ch)
				if curx + width + char_w >= self.width:
					self.chars(text[written:pos], curx,cury)
					curx = 0 ; written = pos; width = char_h
					cury = self.next_line(cury,char_h)
				else:
					width += char_w
		if written<len(text):
			curx = self.chars(text[written:], curx,cury)
		self._x = curx; self._y = cury

	def chars(self, str, x, y):
		assert self._font != None, 'font_name not assigned yet!'
		self._font.fb.fill_rect( 0,0, self.width, self._font.font.height, 0 ) # Fill it with background color
		pos = 0
		for ch in str:
			# print( '   ch', ch )
			char_w = self._font.print_char( ch,pos,0 )# draw it into the FB
			pos += char_w[0]+self._font.spacing # add proportional width
		self.blit_mono( self.font.fb, x, y, w=pos, h=self.font.font.height, colors=(WHITE,BLACK) )
		return x+pos #str_w

	def print(self, text): #does word wrap, leaves self._x unchanged
		cury = self._y; curx = self._x
		char_h = self._font.font.height
		char_w = self._font.font.width # Max Width
		lines = text.split('\n')
		for line in lines:
			#print( "print() line:", line )
			words = line.split(' ')
			for word in words:
				#print( 'print() drawing word:', word )
				if curx + self._font.font.get_width(word) >= self.width:
					#print( "print() splitting required")
					curx = self._x; cury = self.next_line(cury,char_h)
					#print( 'print() curx', curx, 'cury', cury)
					while self._font.font.get_width(word) > self.width:
						# print("print() -> chars() calling")
						self.chars(word[:self.width//char_w],curx,cury)
						# print("print() -> chars() done")
						word = word[self.width//char_w:]
						# print('   > next_line(cury,char_h)', curx, char_h)
						cury = self.next_line(cury,char_h)
					#print( "print() splitting done for word", word )
				if len(word)>0:
					#print( "print() non split required")
					#print( 'print() curx', curx, 'cury', cury)
					#print("print() -> chars() calling_2")
					curx = self.chars(word+' ', curx,cury)
					#print("print() curx %i" % curx)
					#print("print() -> chars() done_2")
			#print( "next_line()")
			curx = self._x; cury = self.next_line(cury,char_h)
			#print( "next_line() done")
		self._y = cury
