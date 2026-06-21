# FrameBuffer Text Writer dependancy
#
# Based on DFRobot FireBeetle 20x8 DFR0487 Arduino library
# available at https://wiki.dfrobot.com/dfr0487/
# 
# * See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
# * Author: Meurisse Dominique
#

__version__ = '0.1.0'

class FontDef:
	# Base class for the various founds
	__slots__ = ('h','w', 'data', 'data_end', 'gutter_space')


	def char_index( self, ch ):
		""" retreibe char_index for a given char OTHERWISE None """		
		ch = ord(ch)
		_r = ch - 32
		if 65 <= _r <= 90: # Is LowerCase
			_r -= 32 

		if (_r<0) or (_r>=64): # Unknown ?
			return None
		return _r

	def char_width( self, char_index ):
		bytesPerColumn = (self.h >> 3) + (1 if (self.h & 0b111)>0 else 0) 

		if char_index==0:
			return self.data_end[0]
		
		return (self.data_end[char_index] - self.data_end[char_index-1])//bytesPerColumn


	def char_offset( self, char_index ):
		""" Offset of data for the char_index """
		if char_index == 0:
			return 0
	
		return self.data_end[char_index - 1]

	def text_width( self, s ):
		_r = 0
		for c in s:
			char_idx = self.char_index( c )
			if char_idx==None:
				continue
			_r += self.char_width( char_idx )+self.gutter_space
		return _r