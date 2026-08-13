#!/usr/bin/env python3
""" Convert a descriptive font .dat file 
       into 
    fontxxx.py definition file used by the fbtext FBGFX library.

The python script will be stored within the <out_filename> file.

Example:
  convert-to-fbgfx-font.py font14x14.dat ../lib/fibt14x14.py

Usage:
  convert-to-fbgfx-font.py <dat_filename> <out_filename>
  convert-to-fbgfx-font.py <dat_filename> <out_filename> [--show] [--debug] [--strict]
  convert-to-fbgfx-font.py (-h | --help)
  
Options:
  --strict  halt compilation when a definition miss in the charset
  --show    Show the extracted chars in the output.
  --debug   Show debugging messages
  
"""
from docopt import docopt

# Minimum list of the chars to defines (in their expected order)
MINIMAL_CHARSET = ['SPACE']+ list( [chr(_b) for _b in b'!"#$%&\'()*+,-./0123456789:;<'] ) + ['EQUAL'] + list( [chr(_b) for _b in b'>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'] )


FILE_HEADER = """# Define the @@h@@ x @@w@@ Font for FrameBuffer Text Writer (fbtext)
#
# Compiled with convert-to-fbgfx-font.py from MC Hobby
# 
# * See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX
# * Author: Meurisse Dominique
#
# Remarks:
#   Definition based on DFRobot FireBeetle 20x8 DFR0487 Arduino library
#   Available at https://wiki.dfrobot.com/dfr0487/

from fontdef import FontDef

class Font@@h@@X@@w@@( FontDef ):
	def __init__( self ):
		super().__init__()
		self.h = @@h@@
		self.w = @@w@@
		self.gutter_space = @@gutter_space@@ # Space between chars
		self.data = @@data@@"""

FILE_DATAEND = "\t\tself.data_end = @@data@@"



class CharData( list ):
	def __init__( self, char_name ):
		self.char_name = char_name
		super().__init__()

class CharCollection( dict ):
	""" Collection of chars data decoded from .dat file """
	def add_char( self, char_name ):
		_data = CharData( char_name )
		self[char_name] = _data
		return _data

class FontCompiler:
	def __init__( self, dat_filename, out_filename, bshow=False, bdebug=True, bstrict=True ):
		self.dat_filename = dat_filename
		self.out_filename = out_filename
		self.bshow = bshow
		self.bdebug = bdebug
		self.bstrict= bstrict
		self.params = {}
		self.chars = CharCollection()

	def read_data( self ):
		with open( self.dat_filename, "r") as f:
			current_char = None
			for s in f:
				s=s.replace('\r','').replace('\n','')
				if len(s)==0:
					continue
				if s[0] in (';', '#'):
					continue
				# PARAM section OR CHAR section
				if (current_char == None) and not(s.startswith("char=")):
					# Check if the line contains a parameter
					if '=' in s:
						_l = s.split('=')
						_pname = _l[0].strip()
						_pvalue = _l[1].strip()
						if _pvalue.isdigit():
							_pvalue = int(_pvalue)
						self.params[_pname]=_pvalue
				elif s.startswith("char="):					
					_char_name = s.split('=')[1].strip()
					current_char = self.chars.add_char( _char_name ) # CharData					
				else:
					# We are in a Char definition data
					# Line can only contains . & *
					s = s.strip()					
					for _c in s:
						if not( _c in ('.','*') ):
							raise Exception( 'Invalid char %s for char=%s in line %s' % (_c, current_char.char_name, s) )
					current_char.append(s)

	def check( self ):
		""" Check all the parameters and conditions.
		    Raise exception in case of error. strict parameter will raise an error if any chars is missing in the minimal definition. """
		# check properties
		if not('h' in self.params):
			raise Exception( 'missing h parameter')
		if not('w' in self.params):
			raise Exception( 'missing w parameter')
		if not( type(self.params['h']) is int ):
			raise Exception( 'h parameter must be integer')
		if not( type(self.params['w']) is int ):
			raise Exception( 'w parameter must be integer')

		if not('gutter_space' in self.params):
			raise Exception( 'missing gutter_space parameter')
		if not( type(self.params['gutter_space']) is int ):
			raise Exception( 'w parameter must be integer')


		h = self.params['h']
		w = self.params['w']
		# All char must have the proper Height		
		for char_name, char_def in self.chars.items():
			if len(char_def)!=h:
				raise Exception('Improper length %i for char %s. Expected %i' % (len(char_def), char_name, h ))
			# All char lines must have the same line
			_len = None
			for idx, line in enumerate(char_def):
				if _len==None:
					_len = len(line)
					continue
				elif len(line)!=_len:
					raise Exception('Invalid data len %i @ line %i for char %s' % (len(line),idx+1,char_def.char_name))
				elif len(line)>w:
					raise Exception('Data len %i exceed width @ line %i for char %s' % (len(line),idx+1,char_def.char_name))
		# Check for the expected chars
		warning = 0
		for _char_name in MINIMAL_CHARSET:
			if not _char_name in self.chars:
				print( '[warning] No declaration for char %s' % _char_name )
				warning += 1
		if self.bstrict and (warning>0):
			raise Exception( 'Missing %i definition in charset' % warning )

	def write( self ):
		h = self.params['h']
		w = self.params['w']
		gutter_space = self.params['gutter_space']
		# list of char_width in pixels
		chars_width = []

		def subs( s ):
			# Substitute the @@xx@@ with their respectives values
			s = s.replace( '@@h@@', str(h) )
			s = s.replace( '@@w@@', str(w) )
			s = s.replace( '@@gutter_space@@', str(gutter_space) )
			s = s.replace( '@@data@@', '[' )
			return s


		with open( self.out_filename, 'w' ) as fout:
			for line in FILE_HEADER.split('/n'):
				bDataLine = '@@data@@' in line
				fout.write( subs(line) )
				fout.write( '\r\n' )

			# Encode the Chars in the proper order
			for idx, _char in enumerate(MINIMAL_CHARSET):
				if self.bdebug:
					print( 'compiling char %s at char_index %i' % (_char,idx))
				# Remember width for each char
				chars_width.append( self.write_char( fout, _char, line_prefix='\t\t\t', line_suffix='\n') )

			fout.write( '\t\t]\r\n')

			# Data End section
			for line in FILE_DATAEND.split('/n'):
				bDataLine = '@@data@@' in line
				fout.write( subs(line) )
				fout.write( '\r\n' )
			# Write the data
			fout.write( '\t\t\t')
			iEndPos=0
			for idx,_width in enumerate(chars_width):
				iEndPos+=_width
				fout.write( str(iEndPos) )
				if idx<len(chars_width)-1:
					fout.write(',')

			fout.write( '\t\t]\r\n')



	def write_char( self, fout, _char, line_prefix, line_suffix ):
		""" Returns the char_width in BYTES """
		# Bytes per column
		h = self.params['h']
		w = self.params['w']		
		byte_per_column = (h//8)+(1 if (h%8)>0 else 0)

		if not _char in self.chars:
			print( 'skip for char %s' % _char )
			return 0

		_char_def = self.chars[_char]
		char_width = len(_char_def[0])

		# Let's encode it
		if not(line_prefix is None):
			fout.write( line_prefix )
		for _col in range(char_width):
			s = ''
			for _line in range(h):
				s += _char_def[_line][_col]
			
			# Column is encoded
			s = s.replace('.','0').replace('*','1')
			s = s+('0'*(byte_per_column*8-len(s)) ) # Upsize to proper byte size

			# slice by 8 bytes value
			#if self.bdebug:
			#	print( '_char', _char, 'columns=', _col, s )
			for idx in range(byte_per_column):
				_slice = s[idx*8:idx*8+8]
				#if self.bdebug:
				#	print( '   ', idx, _slice )
				fout.write( str(eval('0b%s'%_slice)) )
				fout.write( ',' )
		if not(line_suffix is None):
			fout.write( line_suffix )

		return char_width*byte_per_column

	def show( self ):
		# Just print the collected data
		for char_name, char_data in self.chars.items():
			print( '='*40 )
			print( 'char = %s' % char_name )
			for line in char_data:
				print(' ', line )

	def run( self ):
		self.read_data()
		self.check()
		self.write()



if __name__=="__main__":
    arguments = docopt(__doc__)
    if arguments['--debug']:
        print("Arguments :", arguments )
    
    
    if len('<dat_filename>')>0:
    	compiler = FontCompiler( dat_filename=arguments['<dat_filename>'],
                      out_filename=arguments['<out_filename>'],
                      bshow=arguments['--show'],
                      bdebug=arguments['--debug'],
                      bstrict=arguments['--strict'] )

    	compiler.run()
    	if arguments['--show']:
    		compiler.show()
        
    print( 'Done!' )