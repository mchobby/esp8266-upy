'''
modlcd19 is a micropython module for the Olimex MOD-IO board. 

It allows the user to control one or more MOD-IO board.
MOD-LCD1x9 board : http://shop.mchobby.be/product.php?id_product=1414
MOD-LCD1x9 : https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/open-source-hardware  
User Guide : https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/LCD1X9.pdf 

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import ustruct
from machine import Pin
from time import sleep

# __lcd_mapping : segment mapping in COM,segment BIT for all the LCD char.
#
# See segments indexes for a given LCD char.
#   -------0------
# 
#  |   \7  |8  /9 |
#  |5   \  |  /   |1
# 
#   --6---  ---10--
# 
#  |    /  |  \11 |
#  |4  /13 |12 \  |2
# 
#   -------3------  .(14)
#   ------15------
# There are 9 LCD chars on LCD. They are numbered from 1 to 9, so lcd_mapping[1..9].
# Each lcd_mapping[] char has 2 sub-lists for the 16th segments: 
#   lcd_mapping[1..9][COM] : list of "COM" for the 16 segments 
#   lcd_mapping[1..9][BIT] : list of "Segment BIT" for the 16 segments.
COM = 0
BIT = 1
__lcd_mapping = { 
    1 : [
       [ 3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0], # com
       [  34 - 0,  32 - 0,  32 - 0,  34 - 0,  35 - 0,  35 - 0,  34 - 0,  35 - 0,  33 - 0,  33 - 0,  32 - 0,  32 - 0,  33 - 0,  34 - 0,  33 - 0,  35 - 0]  ], # bit  
    2 : [
       [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0], 
	   [34 - 4,  32 - 4,  32 - 4,  34 - 4,  35 - 4,  35 - 4,  34 - 4,  35 - 4,  33 - 4,  33 - 4,  32 - 4,  32 - 4,  33 - 4,  34 - 4,  33 - 4,  35 - 4] ],
    3 : [
	   [ 3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 8,  32 - 8,  32 - 8,  34 - 8,  35 - 8,  35 - 8,  34 - 8,  35 - 8,  33 - 8,  33 - 8,  32 - 8,  32 - 8,  33 - 8,  34 - 8,  33 - 8,  35 - 8] ],
    4 : [
	   [ 3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0 ],
	   [ 34 - 12, 32 - 12, 32 - 12, 34 - 12, 35 - 12, 35 - 12, 34 - 12, 35 - 12, 33 - 12, 33 - 12, 32 - 12, 32 - 12, 33 - 12, 34 - 12, 33 - 12, 35 - 12 ] ],
    5 : [
	   [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 16, 32 - 16, 32 - 16, 34 - 16, 35 - 16, 35 - 16, 34 - 16, 35 - 16, 33 - 16, 33 - 16, 32 - 16, 32 - 16, 33 - 16, 34 - 16, 33 - 16, 35 - 16] ],
    6 : [
	   [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 20, 32 - 20, 32 - 20, 34 - 20, 35 - 20, 35 - 20, 34 - 20, 35 - 20, 33 - 20, 33 - 20, 32 - 20, 32 - 20, 33 - 20, 34 - 20, 33 - 20, 35 - 20] ],    
    7 : [
	   [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 24, 32 - 24, 32 - 24, 34 - 24, 35 - 24, 35 - 24, 34 - 24, 35 - 24, 33 - 24, 33 - 24, 32 - 24, 32 - 24, 33 - 24, 34 - 24, 33 - 24, 35 - 24] ],    
    8 : [
	   [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 28, 32 - 28, 32 - 28, 34 - 28, 35 - 28, 35 - 28, 34 - 28, 35 - 28, 33 - 28, 33 - 28, 32 - 28, 32 - 28, 33 - 28, 34 - 28, 33 - 28, 35 - 28] ],    
    9 : [
	   [3,       3,       0,       0,       2,       1,       1,       3,       1,       3,       1,       2,       2,       2,       0,       0],
	   [34 - 32, 32 - 32, 32 - 32, 34 - 32, 35 - 32, 35 - 32, 34 - 32, 35 - 32, 33 - 32, 33 - 32, 32 - 32, 32 - 32, 33 - 32, 34 - 32, 33 - 32, 35 - 32] ]
  }

# Dictionnary with correspondance between alphabet character and bit pattern of __lcd_mapping
# Eg. Capital O would have bit 0 1 2 3 4 5 activated --> 0x3f
__lcd_alphabet = { 
  ' ': 0x0000, 
  '!': 0x1100, 
  '"': 0x0280, 
  '#': 0x0000, 
  '$': 0x0000, 
  '%': 0x0000, 
  '&': 0x0000, 
  '£': 0x0000, 
  '(': 0x0039, 
  ')': 0x000f,
  '}': 0x2480,
  '{': 0x0a40,
  '°': 0x0463, 
  '+': 0x1540, 
  ',': 0x0000, 
  '-': 0x0440, 
  '.': 0x1000, 
  '/': 0x2200, 

  '0': 0x003f, 
  '1': 0x0006, 
  '2': 0x045b, 
  '3': 0x044f, 
  '4': 0x0466, 
  '5': 0x046d, 
  '6': 0x047d, 
  '7': 0x0007, 
  '8': 0x047f, 
  '9': 0x046f, 

  ':': 0x0000, # Rien
  ';': 0x0000, # Rien
  '<': 0x0a00, 
  '=': 0x0000, 
  '>': 0x2080, 
  '?': 0x0000, 
  '@': 0xffff, 

  'A': 0x0477, 
  'B': 0x0a79, 
  'C': 0x0039, 
  'D': 0x20b0, 
  'E': 0x0079, 
  'F': 0x0071, 
  'G': 0x047d, 
  'H': 0x0476, 
  # 'i': 0x0006, /* I */
  'I': 0x0030, # I edit 
  'J': 0x000e, 
  'K': 0x0a70, 
  'L': 0x0038, 
  'M': 0x02b6, 
  'N': 0x08b6, 
  'O': 0x003f, 
  'P': 0x0473, 
  'Q': 0x083f, 
  'R': 0x0c73, 
  'S': 0x046d, 
  'T': 0x1101, 
  'U': 0x003e, 
  'V': 0x2230, 
  'W': 0x2836, 
  'X': 0x2a80, 
  'Y': 0x046e, 
  'Z': 0x2209, 

  '[': 0x0039, 
  # ' ': 0x0880, # backslash 
  ']': 0x000f, 
  '^': 0x0001, 
  '_': 0x0008, 
  '\'': 0x0100, 

  'a': 0x1058, 
  'b': 0x047c, 
  'c': 0x0058, 
  'd': 0x045e, 
  'e': 0x2058, 
  'f': 0x0471, 
  'g': 0x0c0c, 
  'h': 0x0474, 
  'i': 0x0004, 
  'j': 0x000e, 
  'k': 0x0c70, 
  'l': 0x0038, 
  'm': 0x1454, 
  'n': 0x0454, 
  'o': 0x045c, 
  'p': 0x0473, 
  'q': 0x0467, 
  'r': 0x0450, 
  's': 0x0c08, 
  't': 0x0078, 
  'u': 0x001c, 
  'v': 0x2010, 
  'w': 0x2814, 
  'x': 0x2a80, 
  'y': 0x080c, 
  'z': 0x2048 
 }

class MODLCD1x9():
    """
    Class to control the MOD-LCD1x9 board

    ....description of methods.....
    """

    def __init__( self, i2c_bus, addr=0x38 ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr = addr # MOD-LCD1x9 board address
        self.lcdBitmap = [0x00] * 20 # 40segments * 4 = 160px, 160 / 8 = 20bytes (cfr: Olimex 32U4 driver)
        self.__enable_point = [None] * 9 # Enable/Disable/don't care points individually on screen
        self.__enable_selection = [False] * 9 # True/False - enable/disable

        if not self._initialize():
            raise Exception( 'init failure')

    def _initialize( self ):
        """ initializes pins and registers of the LCD1x9.
            Also lights up all segments """
        nack = self.i2c.writeto( self.addr, bytes(
            [ 0b11001000, # mode register
              0b11110000, # blink register
              0b11100000, # device select register
              0b00000000  # Pointer register
            ] + [0xFF]*20   # Light up all segments (over 20 bytes)
            ) )
        # also initialize local buffer (light up all segment)
        for i in range( 20 ):
            self.lcdBitmap[i] = 0xFF
        return nack == 24        

    def _enable_segment( self, comIndex, bitIndex ):
        """ enables a segment in the display buffer. Does not actually light up the segment until Update(..)

            :params comIndex: backplate index
            :params bitIndex: segment index
        """
        if bitIndex >= 40:
            return
        comIndex = comIndex & 0x03
        if (bitIndex & 0x01):
            comIndex = comIndex | 0x04

        bitIndex = bitIndex >> 1

        self.lcdBitmap[bitIndex] = self.lcdBitmap[bitIndex] | (0x80 >> comIndex)

    def _disable_segment( self, comIndex, bitIndex ):
        """ see _enable_segment() """
        if bitIndex >= 40:
            return
        comIndex = comIndex & 0x03
        if (bitIndex & 0x01):
            comIndex = comIndex | 0x04

        bitIndex = bitIndex >> 1

        self.lcdBitmap[bitIndex] = self.lcdBitmap[bitIndex] &  (0xFF - (0x80 >> comIndex)) # 0xFF - y = bitwise not = ~(y)

    def _write( self, s9 ):
        """ Write a string to the LCD buffer. Do not write more than than 9 characters """
        assert len(s9)<=9, '9 chars max!' 

        s9 = s9+(' '*(9-len(s9))) # upsize to 9 char len
        for index, s in enumerate(s9):
            # ensure a know character
            if not( s in __lcd_alphabet ):
                s = ' '
            bitfield = __lcd_alphabet[s] # 16bit 

            for i in range( 16 ): # 16bit of bitfield
                bit = __lcd_mapping[ index+1 ][BIT][i] # i+1 ==> 0-indexed to 1-indexed
                com = __lcd_mapping[ index+1 ][COM][i]

                # If the bit is activated in the bitfield
                if bitfield & (1<<i):
                    self._enable_segment( com, bit )
                else:
                    self._disable_segment( com, bit )

    def _apply_extra( self ):
    	""" apply the extra configuration in the lcdBitmap buffer. 
    	    This concerns the POINY setting and SELECTION setting. """
    	for iPos in range( 9 ):
            # POINT = bit #14 
            bit = __lcd_mapping[ iPos+1 ][BIT][14] # i+1 ==> 0-indexed to 1-indexed
            com = __lcd_mapping[ iPos+1 ][COM][14]

            # If we should not take care about the bit
            if self.__enable_point[iPos] != None: # enable_point is 0-indexed
                # If the bit should be activated	
                if self.__enable_point[iPos]: # enable_point is 0-indexed
                    self._enable_segment( com, bit )
                else:
                    self._disable_segment( com, bit )   

            # SELECTION = bit #15 
            bit = __lcd_mapping[ iPos+1 ][BIT][15] # i+1 ==> 0-indexed to 1-indexed
            com = __lcd_mapping[ iPos+1 ][COM][15]

            # If the bit should be activated	
            if self.__enable_selection[iPos]: # enable_point is 0-indexed
                self._enable_segment( com, bit )
            else:
                self._disable_segment( com, bit )  

    def update( self ):
        """ Update send the display_buffer to the LCD. Usually, you do not need to call this yourself """
        self._apply_extra() # Apply point+selection config in the lcdBitmap

        nack = self.i2c.writeto( self.addr, bytes(
            [ 0b11100000, # device select register
              0b00000000  # pointer register
            ] + self.lcdBitmap ) )
        # print( self.lcdBitmap )
        if nack != 22:
            raise Exception( 'update error')

    def write( self, value, format=None, scrool_time=0.350 ):
        """ Write exactly 9 chars on the LCD + Update LCD """
        if format:
            s = format % value
        else:
            s = value

        if type( s ) != str:
            s = '%s' % value
        
        # take care about point (ex: digital value)
        if format and ('.' in format):
            if len( s )>10:  # we will replace the . so we can accept one char more
                self._write( 'FError' ) # Formating error
                self.update()
                return
            # Left pad with space (on 10 position, we will remove the dot)
            s = ' '*(10-len(s))+s
            # Identify '.' position
            idxPoint = s.index('.')
            # write the content without the point
            self._write( s.replace('.','') )
            # set the point to the proper position
            for i in range(9):
                self.point( i+1, enable=True if (i+1)==idxPoint else False )
            self.update()
            return

        # Simple display
        if len(s)<=9:
            self._write( s )
            self.update()
        else:
        	# Scrooling display
        	for i in range( len(s)+1 ):
        		self._write( s[i:i+9] )
        		self.update()
        		sleep( 0.750 if i==0 else scrool_time ) # Wait 1/2 sec for first display

    def point( self, position, enable=True, force_update=False ):
        """ Light the point on the LCD. 

        :param enable: True/False/None for display/hide/don't care """
        assert 1<= position <=9
        assert enable in (True,False,None)
        self.__enable_point[ position-1 ] = enable
        if force_update:
            self.update()
        
    def selection( self, position, enable=True, force_update=False ):
        """ Light the selection UNDER BARRE on the LCD. Call it after _write & before _update. """
        assert 1<= position <=9
        assert enable in (True,False)
        self.__enable_selection[ position-1 ] = enable
        if force_update:
            self.update() 	
