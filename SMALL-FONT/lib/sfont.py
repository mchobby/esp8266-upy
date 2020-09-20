""" SmallFont is a Font Drawer Class embedding and drawing a very compact font.

    Mini project Spin-off from the MCHobby's FreeType-Generator for MicroPython
	See for reference : https://github.com/mchobby/freetype-generator

See: https://github.com/mchobby/esp8266-upy/tree/master/SMALL-FONT

domeu, 20 Sept 2020, Initial Writing (shop.mchobby.be)
----------------------------------------------------------------------------
MCHobby invest time and ressource in developping project and libraries.
It is a long and tedious work developed with Open-Source mind and freely available.
IF you like our work THEN help us by buying your product at MCHobby (shop.mchobby.be).
----------------------------------------------------------------------------
Copyright (C) 2020  - Meurisse D. (shop.mchobby.be)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
__version__ = '0.0.1'

CHAR_6_8 = b'\x00\x00\x00\x00\x00\x00\x00\x00_\x00\x00\x00\x00\x07\x00\x07\x00\x00\x14\x7f\x14\x7f\x14\x00$*\x7f*\x12\x00#\x13\x08db\x006IV P\x00\x00\x08\x07\x03\x00\x00\x00\x1c"A\x00\x00\x00A"\x1c\x00\x00$\x18~\x18$\x00\x08\x08>\x08\x08\x00\x00\x80p0\x00\x00\x08\x08\x08\x08\x08\x00\x00\x00``\x00\x00 \x10\x08\x04\x02\x00>AIA>\x00\x00B\x7f@\x00\x00rIIIF\x00!AIM2\x00\x18\x14\x12\x7f\x10\x00\'EEE8\x00<JII1\x00A!\x11\t\x07\x006III6\x00FII)\x16\x00\x00\x00\x14\x00\x00\x00\x00@4\x00\x00\x00\x00\x08\x14"A\x00\x14\x14\x14\x14\x14\x00\x00A"\x14\x08\x00\x02\x01Y\t\x06\x00>A]YN\x00|\x12\x11\x12|\x00\x7fIII6\x00>AAA"\x00\x7fAAA>\x00\x7fIIIA\x00\x7f\t\t\t\x01\x00>AAQs\x00\x7f\x08\x08\x08\x7f\x00\x00A\x7fA\x00\x00 @A?\x01\x00\x7f\x08\x14"A\x00\x7f@@@@\x00\x7f\x02\x1c\x02\x7f\x00\x7f\x04\x08\x10\x7f\x00>AAA>\x00\x7f\t\t\t\x06\x00>AQ!^\x00\x7f\t\x19)F\x00&III2\x00\x03\x01\x7f\x01\x03\x00?@@@?\x00\x1f @ \x1f\x00?@8@?\x00c\x14\x08\x14c\x00\x03\x04x\x04\x03\x00aYIMC\x00\x00\x7fAAA\x00\x02\x04\x08\x10 \x00\x00AAA\x7f\x00\x04\x02\x01\x02\x04\x00@@@@F\x00\x00\x03\x07\x08\x00\x00 TTx@\x00\x7f(DD8\x008DDD(\x008DD(\x7f\x008TTT\x18\x00\x00\x08~\t\x02\x008\xa4\xa4\x9cx\x00\x7f\x08\x04\x04x\x00\x00D}@\x00\x00 @@=\x00\x00\x7f\x10(D\x00\x00\x00A\x7f@\x00\x00|\x04x\x04x\x00|\x08\x04\x04x\x008DDD8\x00\xfc\x18$$\x18\x00\x18$$\x18\xfc\x00|\x08\x04\x04\x08\x00HTTT$\x00\x04\x04?D$\x00<@@ |\x00\x1c @ \x1c\x00<@ @<\x00D(\x10(D\x00L\x90\x90\x90|\x00DdTLD\x00\x00\x086A\x00\x00\x00\x00w\x00\x00\x00\x00A6\x08\x00\x00\x02\x01\x02\x04\x02\x00\x00\x00\x00\x00\x00\x00'

def get_character( ch ):
	""" Returns (list_of_bytes,width,height) or (None,width,height) """
	iOrd = ord(ch)
	var1 = 0
	if iOrd < 0x20 :
		if 0x06 <= iOrd < 0x0e : # Entre 6 et 14
			return (None,6,8) # return 1
		else:
			return (None,6,8)

	# know code
	if iOrd < 0x80:
		return (CHAR_6_8[(iOrd-0x20)*6:(iOrd-0x20)*6+6], 6, 8)
	else:
		return (None,6,8)

class FontDrawer:
	def __init__(self, frame_buffer, font_color=1, bgcolor=0 ):
		self.fb = frame_buffer
		self._fontscale = 1
		self._fontcolor = font_color # Font color (integer representation)
		self._bgcolor   = bgcolor # Background color

	@property
	def color( self ):
		""" FrameBuffer color value for drawing font """
		return self._fontcolor

	@color.setter
	def color( self, value ):
		""" FrameBuffer color value used to draw font """
		self._fontcolor = value

	@property
	def bgcolor( self ):
		""" FrameBuffer color value for drawing background """
		return self._bgcolor

	@bgcolor.setter
	def bgcolor( self, value ):
		""" FrameBuffer color value used to drawing background.
		 	(TODO) None will use the pixel background color for the drawed pixel """
		self._bgcolor = value

	@property
	def scale( self ):
		return self._fontscale

	@scale.setter
	def scale( self, value ):
		assert 1 <= value <= 4
		self._fontscale = value

	def _get_bgcolor(self, x, y):
		""" Extract the Background color at position x,y """
		if self._bgcolor == None:
			raise NotImplementedError('TODO')
		else:
			return self._bgcolor

	def _fill_bicolor(self, data, x, y, width, height, scale=1 ):
		bgcolor = self._get_bgcolor(x, y)

		xpix=0
		for col in data:
			ypix = (height-1) * scale
			for _y in range( height-1, -1, -1 ):
				c = self._fontcolor if ((col & (1<<_y)) > 0) else bgcolor
				for i in range( scale-1, -1, -1):
					self.fb.hline(x+xpix,y+ypix+scale+i,scale,c)
				ypix -= scale
			xpix+=scale


	def print_char(self, char, x, y ):
		""" Print a single char on a screen (a single characters or an ASCII code) """
		if type(char) is str:
			assert len(char) == 1
		elif type(char) is int:
			assert char <= 255
			char = chr( char ) # Convert to char

		_ch, _w, _h = get_character( char )
		try:
			chrwidth = len(_ch) * self._fontscale
		except KeyError:
			_ch = None
			chrwidth = self._font.width * self._fontscale

		if _ch is None:
			self.fb.rect(x, y, _h*self._fontscale, chrwidth*self._fontscale, self._fontcolor)
		else:
			# Debug: print( data, x, y, chrwidth, self._font.height, self._fontscale )
			self._fill_bicolor(_ch, x, y, chrwidth, _h, scale=self._fontscale)

		# char_width_proportionnal, char_width_NON_proportionnal
		return chrwidth, _h * self._fontscale

	def print_str( self, text, x, y ):
		""" As defined in projet FreeType-Generator for FontDrawer.print_str() ! """
		# See https://github.com/mchobby/freetype-generator,
		# file micropython/lib/fdrawer.py, classe FontDrawer, method print_str()
		xpos = x
		for ch in text:
			widths = self.print_char( ch, xpos, y )
			xpos += widths[0] # add proportional_witdth of characters
			xpos += 2*self._fontscale # 2 pixels spacing between chars

	def text( self, text, x, y ):
		""" Draw the text from position x, y. x,y are the position of the top-left pixel of the text.
			Mimic the FrameBuffer.text()"""
		return self.print_str( text, x, y )
