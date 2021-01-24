# See LICENSE.txt file
# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili934x
#
# TODO: set_font
import time
import ustruct
import framebuf # Printing/drawing characters
import math
from micropython import const

__version__ = '0.0.1'

_RDDSDR = const(0x0f) # Read Display Self-Diagnostic Result
_SLPOUT = const(0x11) # Sleep Out
_GAMSET = const(0x26) # Gamma Set
_DISPOFF = const(0x28) # Display Off
_DISPON = const(0x29) # Display On
_CASET = const(0x2a) # Column Address Set
_PASET = const(0x2b) # Page Address Set
_RAMWR = const(0x2c) # Memory Write
_RAMRD = const(0x2e) # Memory Read
_MADCTL = const(0x36) # Memory Access Control
_VSCRSADD = const(0x37) # Vertical Scrolling Start Address
_PIXSET = const(0x3a) # Pixel Format Set
_PWCTRLA = const(0xcb) # Power Control A
_PWCRTLB = const(0xcf) # Power Control B
_DTCTRLA = const(0xe8) # Driver Timing Control A
_DTCTRLB = const(0xea) # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7) # Pump Ratio Control
_PWCTRL1 = const(0xc0) # Power Control 1
_PWCTRL2 = const(0xc1) # Power Control 2
_VMCTRL1 = const(0xc5) # VCOM Control 1
_VMCTRL2 = const(0xc7) # VCOM Control 2
_FRMCTR1 = const(0xb1) # Frame Rate Control 1
_DISCTRL = const(0xb6) # Display Function Control
_ENA3G = const(0xf2) # Enable 3G
_PGAMCTRL = const(0xe0) # Positive Gamma Control
_NGAMCTRL = const(0xe1) # Negative Gamma Control
_SWRESET = const(0x01)

_CHUNK = const(1024) #maximum number of pixels per spi write

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


class ILI9341:

	def __init__(self, spi, cs, dc, rst, w, h, r):
		self.spi = spi
		self.cs = cs
		self.dc = dc
		self.rst = rst
		self._init_width = w
		self._init_height = h
		self.width = w
		self.height = h
		self.rotation = r
		self.cs.init(self.cs.OUT, value=1)
		self.dc.init(self.dc.OUT, value=0)
		if self.rst:
			self.rst.init(self.rst.OUT, value=0)
		self.reset()
		self.init()
		self._scroll = 0
		self._buf = bytearray(_CHUNK * 2)
		self._font = None # print() : font
		self._pbuf = None # print() : Buffer for Print statement
		self._pfb  = None # print() : FrameBuf for Print statement
		self._font_name = None # The fontname to use by the font_drawer
		self._cbuf = bytearray( 2 ) # buffer color
		self._colormap = bytearray(b'\x00\x00\xFF\xFF') #default white foregraound, black background
		self._x = 0
		self._y = 0
		self.scrolling = False

	def set_color(self,fg,bg):
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
		self._pbuf = bytearray( (self._font.font.height+self._font.font.descender)*self.width//8 )
		self._pfb = framebuf.FrameBuffer(self._pbuf,self.width,self._font.font.height+self._font.font.descender, framebuf.MONO_VLSB )
		self._font.fb = self._pfb # Font must be drawed to custom FrameBuffer
		self._font.color = 1


	def init(self):
		for command, data in (
			(_RDDSDR, b"\x03\x80\x02"),
			(_PWCRTLB, b"\x00\xc1\x30"),
			(_PWRONCTRL, b"\x64\x03\x12\x81"),
			(_DTCTRLA, b"\x85\x00\x78"),
			(_PWCTRLA, b"\x39\x2c\x00\x34\x02"),
			(_PRCTRL, b"\x20"),
			(_DTCTRLB, b"\x00\x00"),
			(_PWCTRL1, b"\x23"),
			(_PWCTRL2, b"\x10"),
			(_VMCTRL1, b"\x3e\x28"),
			(_VMCTRL2, b"\x86")):
			self._write(command, data)

		if self.rotation == 0:                  # 0 deg
			self._write(_MADCTL, b"\x48")
			self.width = self._init_height
			self.height = self._init_width
		elif self.rotation == 1:                # 90 deg
			self._write(_MADCTL, b"\x28")
			self.width = self._init_width
			self.height = self._init_height
		elif self.rotation == 2:                # 180 deg
			self._write(_MADCTL, b"\x88")
			self.width = self._init_height
			self.height = self._init_width
		elif self.rotation == 3:                # 270 deg
			self._write(_MADCTL, b"\xE8")
			self.width = self._init_width
			self.height = self._init_height
		elif self.rotation == 4:                # Mirrored + 0 deg
			self._write(_MADCTL, b"\xC8")
			self.width = self._init_height
			self.height = self._init_width
		elif self.rotation == 5:                # Mirrored + 90 deg
			self._write(_MADCTL, b"\x68")
			self.width = self._init_width
			self.height = self._init_height
		elif self.rotation == 6:                # Mirrored + 180 deg
			self._write(_MADCTL, b"\x08")
			self.width = self._init_height
			self.height = self._init_width
		elif self.rotation == 7:                # Mirrored + 270 deg
			self._write(_MADCTL, b"\xA8")
			self.width = self._init_width
			self.height = self._init_height
		else:
			self._write(_MADCTL, b"\x08")

		for command, data in (
			(_PIXSET, b"\x55"),
			(_FRMCTR1, b"\x00\x18"),
			(_DISCTRL, b"\x08\x82\x27"),
			(_ENA3G, b"\x00"),
			(_GAMSET, b"\x01"),
			(_PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
			(_NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
			self._write(command, data)
		self._write(_SLPOUT)
		time.sleep_ms(120)
		self._write(_DISPON)

	def reset(self):
		if self.rst:
			self.rst(0) # Hardware Reset Pin
			time.sleep_ms(50)
			self.rst(1)
			time.sleep_ms(50)
		else:
			self._write(_SWRESET)

	def _write(self, command, data=None):
		self.dc(0)
		self.cs(0)
		self.spi.write(bytearray([command]))
		self.cs(1)
		if data is not None:
			self._data(data)

	def _data(self, data):
		self.dc(1)
		self.cs(0)
		self.spi.write(data)
		self.cs(1)

	def _writeblock(self, x0, y0, x1, y1, data=None):
		self._write(_CASET, ustruct.pack(">HH", x0, x1))
		self._write(_PASET, ustruct.pack(">HH", y0, y1))
		self._write(_RAMWR, data)

	def _readblock(self, x0, y0, x1, y1, data=None):
		self._write(_CASET, ustruct.pack(">HH", x0, x1))
		self._write(_PASET, ustruct.pack(">HH", y0, y1))
		if data is None:
			return self._read(_RAMRD, (x1 - x0 + 1) * (y1 - y0 + 1) * 3)

	def _read(self, command, count):
		self.dc(0)
		self.cs(0)
		self.spi.write(bytearray([command]))
		data = self.spi.read(count)
		self.cs(1)
		return data

	def pixel(self, x, y, color=None): # FrameBuffer mimic
		if color is None:
			r, b, g = self._readblock(x, y, x, y)
			return color565(r, g, b)
		if not 0 <= x < self.width or not 0 <= y < self.height:
			return
		self._writeblock(x, y, x, y, ustruct.pack(">H", color))

	def hline( self, x,y,w, c, tick=1 ): # FrameBuffer mimic
		if (x+w) >= self.width: w = self.width-x
		if (w<=0) or (x>=self.width):
			return
		if tick > 10: tick = 10
		if (y+tick-1) > self.height: tick = self.height-y
		if tick<=0:
			return
		# fill the buffer with the color
		if (w*tick) > _CHUNK:
			raise MemoryError( "hline Buffer Overflow (%i px)" % _CHUNK )
		# transform color to _bytearray
	 	self._cbuf[0] = c>>8
		self._cbuf[1] = c & 255
		# Fill buffer with color
		v = memoryview(self._buf)
		for idx in range(0, w*tick*2, 2):
			v[idx:idx+2] = self._cbuf
		self._writeblock(x, y, x+w, y+(tick-1), data=v[0:w*tick*2] )


	def vline( self, x,y,h, c, tick=1 ): # Framebuffer Mimic
		if (y+h) >= self.height: h = self.height-y
		if (h<=0) or (y>=self.height):
			return
		if tick > 10: tick = 10
		if (x+tick-1) > self.width: tick = self.width-x
		if tick<=0:
			return
		if (h*tick) > _CHUNK:
			raise MemoryError( "vline Buffer Overflow (%i px)" % _CHUNK )
	 	self._cbuf[0] = c>>8
		self._cbuf[1] = c & 255
		v = memoryview(self._buf)
		for idx in range(0, h*tick*2, 2):
			v[idx:idx+2] = self._cbuf
		self._writeblock(x, y, x+(tick-1), y+h, data=v[0:h*tick*2] )

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

	def fill( self, c ): # FrameBuffer mimic
		self.fill_rect( 0,0,self.width,self.height,c)

	def rect( self, x,y, w,h, c, tick=1 ):
		self.hline( x, y, w, c, tick )
		self.hline( x, y+h, w, c, tick )
		self.vline( x, y, h, c, tick )
		self.vline( x+w, y, h, c, tick )

	def fill_rect(self, x, y, w, h, color=None):
		x = min(self.width - 1, max(0, x))
		y = min(self.height - 1, max(0, y))
		w = min(self.width - x, max(1, w))
		h = min(self.height - y, max(1, h))
		if color:
			color = ustruct.pack(">H", color)
		else:
			color = self._colormap[0:2] #background
		for i in range(_CHUNK):
			self._buf[2*i]=color[0]; self._buf[2*i+1]=color[1]
		chunks, rest = divmod(w * h, _CHUNK)
		self._writeblock(x, y, x + w - 1, y + h - 1, None)
		if chunks:
			for count in range(chunks):
				self._data(self._buf)
		if rest != 0:
			mv = memoryview(self._buf)
			self._data(mv[:rest*2])

	def erase(self):
		self.fill_rect(0, 0, self.width, self.height)

	def blit(self, bitbuff, x, y, w, h):
		x = min(self.width - 1, max(0, x))
		y = min(self.height - 1, max(0, y))
		w = min(self.width - x, max(1, w))
		h = min(self.height - y, max(1, h))
		chunks, rest = divmod(w * h, _CHUNK)
		self._writeblock(x, y, x + w - 1, y + h - 1, None)
		written = 0
		for iy in range(h):
			for ix in range(w):
				index = ix+iy*w - written
				if index >=_CHUNK:
					self._data(self._buf)
					written += _CHUNK
					index   -= _CHUNK
				c = bitbuff.pixel(ix,iy)
				self._buf[index*2] = self._colormap[c*2]
				self._buf[index*2+1] = self._colormap[c*2+1]
		rest = w*h - written
		if rest != 0:
			mv = memoryview(self._buf)
			self._data(mv[:rest*2])

	def scroll(self, dy):
		self._scroll = (self._scroll + dy) % self.height
		self._write(_VSCRSADD, ustruct.pack(">H", self._scroll))

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

		self._font.fb.fill_rect( 0,0, self.width, self._font.font.height, 0 ) # Fill it in black
		pos = 0
		for ch in str:
			char_w = self._font.print_char( ch,pos,0 )# draw it into the FB
			pos += char_w[0]+self._font.spacing # add proportional width
		self.blit(self._font.fb,x,y,pos,self._font.font.height )
		return x+pos #str_w

	def print(self, text): #does word wrap, leaves self._x unchanged
		cury = self._y; curx = self._x
		char_h = self._font.font.height
		char_w = self._font.font.width # Max Width
		lines = text.split('\n')
		for line in lines:
			words = line.split(' ')
			for word in words:
				if curx + self._font.font.get_width(word) >= self.width:
					curx = self._x; cury = self.next_line(cury,char_h)
					while self._font.font.get_width(word) > self.width:
						self.chars(word[:self.width//char_w],curx,cury)
						word = word[self.width//char_w:]
						cury = self.next_line(cury,char_h)
				if len(word)>0:
					curx = self.chars(word+' ', curx,cury)
			curx = self._x; cury = self.next_line(cury,char_h)
		self._y = cury
