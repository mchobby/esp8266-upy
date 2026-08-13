# FrameBuffer Text Writter - draw small size text on FrameBuffer
#
# Based on DFRobot FireBeetle 20x8 DFR0487 Arduino library
# available at https://wiki.dfrobot.com/dfr0487/
# 
# * See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
# * Author: Meurisse Dominique
#
import framebuf

___version__ = "0.2.0"
__repo__ = "https://github.com/mchobbyMCHobby/esp8266-upy/FBGFX.git"

class FBText:
	""" FrameBuffer Text drawer """
	def __init__( self, target_fb, w_fb, h_fb, source_font ):
		""" target_fb : Frame Buffer where the draw the text
			w_fb      : Width of the Frame Buffer (usually screen width)
			h_fb      : Height of the Frame Buffer (usually screen height) 
			source_font : instance of FontDef() containing the font data  """
		self.target_fb = target_fb
		self.w_fb = w_fb # Width of the FrameBuffer
		self.h_fb = h_fb 
		self.font = source_font

	def text( self, s, x, y, c ):
		""" Draw text s at position (x,y) in the FrameBuffer with color c """
		bg = 0 if c else 1
		curr_x = x
		i = 0
		currchar = 0
		if((y+self.font.h) < 0) or (y >= self.h_fb):
			return
	
		while True:
			# EndOfStr ?
			if i>=len(s):
				return
			
			currchar = self.font.char_index(s[i])
			if currchar==None: # Unknown ?
				i+=1
				continue

			if curr_x >= self.w_fb:
				break
			
			chr_width = self.font.char_width(currchar) # In Pixels
			if(curr_x + chr_width + self.font.gutter_space) >= 0:

				_offset = self.font.char_offset(currchar)
				_char_width = self.font.char_width(currchar)

				iCol = 0 # Col in the drawed char 
				iRow = 0 # Row in the drawed char
				while True:
					# draw Pixel (char is drawed Column per Column)
					self.target_fb.pixel( curr_x+iCol, y+iRow, c if (self.font.data[_offset] & (1<<(7-(iRow%8))))>0 else bg  )
					# Next Pixel to draw (colum per column)
					iRow += 1
					# Next column ?
					if iRow==self.font.h:
						iCol += 1
						iRow = 0
						_offset += 1
						# The end ?
						if iCol>=_char_width:
							break 
					if iRow==8:
						_offset+=1
					elif iRow==16:
						_offset+=1
					elif iRow==24:
						raise Exception( "%s limited to 24 pixel height max!" % self.__class__.__name__)
					
			
			curr_x += (chr_width + self.font.gutter_space)			
			i += 1

