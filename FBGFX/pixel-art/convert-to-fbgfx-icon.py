#!/usr/bin/env python3
""" Convert a 1bit Image PNG file to FBGFX to icon_xxx.py

Will extract 1bit icons (having <icon_width> x <icon_width> pixels from the <in_filename> .

The created MICROPYTHON CONSTANTS are named with <basename>[row_index][column_index] (eg: WEATHER12).

The python script will be stored within the <out_filename> file.

Example:
  convert-to-fbgfx-icon.py one-bit-pixel-icons/Icons_Weather.png 16 WEATHER iweather.py

Usage:
  convert-to-fbgfx-icon.py <in_filename> <icon_width> <basename> <out_filename> [--show] [--debug]
  convert-to-fbgfx-icon.py (-h | --help)
  
Options:
  --show    Show the extracted images in the output.
  --debug   Show debugging messages
  
"""
from docopt import docopt
from PIL import Image

class OneBitImageSplitter():
    def __init__( self, in_filename, icon_width, icon_basename ):
        self.in_filename = in_filename
        self.icon_basename = icon_basename
        self.img = Image.open( in_filename )
        self.pixels = list(self.img.getdata())
        self.w, self.h = self.img.size
        self.icon_w = icon_width
        
    @property
    def line_count( self ):
        return self.h//self.icon_w
    
    @property
    def col_count( self ):
        return self.w//self.icon_w
        
    def pixel_at( self, x, y ):
        #list_ = [self.pixels[i * self.w:(i + 1) * self.w] for i in range(0,self.h)]
        return self.pixels[y*self.w+x]
        
    def extract_icon( self, line, col ):
        # Return Icon Pixels (data color)
        #
        # [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], ... ]
        assert 0<=line<=(self.h//self.icon_w), "Invalid line range"
        assert 0<=col<=(self.w//self.icon_w), "Invalid col range"
        
        abs_top_left = (col*self.icon_w, line*self.icon_w)
        data = []
        for row in range( self.icon_w ):
            _line = []
            data.append( _line )
            for col in range( self.icon_w ):
                abs_x_y = (abs_top_left[0]+col, abs_top_left[1]+row)
                _line.append( self.pixel_at( abs_x_y[0], abs_x_y[1] ))
        return data
    
    def color_to_bit( self, color ):
        # Transform the Pixel color to 1 or 0 (equivalent of True and False)
        # 0 = Transparent => 0,  1 = black => 1,  2 = White => 0
        if isinstance( color, int ):
            return 1 if color==1 else 0
        if isinstance( color, tuple ) and (len(color)==4):
            # (r,g,b,opacity)
            if color[3]==0 or ( (color[3]>250) and ((color[0]+color[1]+color[2])>(50*3)) ):
                return 0 # White or transparent
            else:
                return 1
        raise Exception( "color format %r not supported" % color )
    
    def preview_data( self, data ):
        # display the color Data as 1bit color
        # 0 = Transparent => 0b0,  1 = black => 0b1,  2 = White => 0b0
        for row in data:
            _ = []
            for color in row:
                _.append( 'X' if self.color_to_bit(color) else '.' )
            print( ''.join(_) )
    
    def is_empty_data( self, data ):
        # Check if the data contains at least one black pixel
        for row in data:
            for color in row:
                if self.color_to_bit( color ):
                    return False
        return True
            
    def icon_to_bits( self, data ):
        # Transform the color Data to 1bit color
        # 0 = Transparent => 0b0
        # 1 = black => 0b1
        # 2 = White => 0b0
        # Returns: [16, '0b0000000000000000', '0b0000111111100000', ... ]
        _bits = [ self.icon_w ] 
        for row in data:
            _ = []
            for color in row:
                _.append( '1' if self.color_to_bit(color) else '0' )
            _bits.append( '0b%s' % ''.join( _ ) )            
        return _bits
    
    def icon_name( self, line, col ):
        """ Compose a constant name line WEATHER12 (shift index from 0..N-1 to 1..N"""
        return "%s%s%s" % (self.icon_basename,line+1,col+1)


def export_icons( in_filename, icon_width, icon_basename, out_filename, bshow=False, bdebug=True ):
    splitter = OneBitImageSplitter( in_filename, icon_width=icon_width, icon_basename=icon_basename )
    print( 'Source     :', in_filename )
    print( 'Image Size :', (splitter.w,splitter.h) )
    print( 'Icon size  :', (icon_width,icon_width) )
    with open( out_filename, "w" ) as f:
        f.write( "# %sx%s icons generated from %s\n" % (icon_width,icon_width,in_filename) )
        f.write( "#\n" )
        f.write( "# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/FBGFX\n" )
        f.write( "#\n" )
        f.write( "# Author: Meurisse Dominique\n" )
        f.write( "#\n" )
        f.write( "__version__ = '0.0.1'\n" )
        f.write( "\n" )
        f.write( "# First byte is the size of the icon\n" )
        f.write( "\n" )
        f.write( "\n" )
        
        icount = 0
        icon_names = []
        for line in range( splitter.line_count ):
            for col in range( splitter.col_count ):
                icon_name = splitter.icon_name( line=line, col=col )
                data = splitter.extract_icon( line=line, col=col )
                if bdebug:
                    print( "--- %s ---------------------" % icon_name )
                    print( data )
                if splitter.is_empty_data( data ):
                    continue
                icon_names.append( icon_name )
                icount += 1
                # Show information about extracted icon
                if bshow:
                    print( "=== %s %s" % (icon_name,"="*40) )
                    splitter.preview_data( data )
                else:
                    print( "    %s" % icon_name )
                    
                bits = splitter.icon_to_bits( data )
                # bits = [16, '0b0000000000000000', ...
                f.write( '%s = [' % (icon_name,) )
                bits[0] = '%s' % bits[0] # Simplify for next line
                f.write( ', '.join( [_.replace("'","") for _ in bits] ) )
                f.write( ' ]\n' )
        f.write( 'all_icons = [' )
        f.write( ','.join(icon_names) )
        f.write( ']\n' )
        f.write( "\n" )
    
    print( "%s icons exported" % icount )
    print( "%s written" % out_filename )

if __name__=="__main__":
    arguments = docopt(__doc__)
    if arguments['--debug']:
        print("Arguments :", arguments )
    
    
    if len('<in_filename>')>0:
        export_icons( in_filename=arguments['<in_filename>'],
                      icon_width=int(arguments['<icon_width>']),
                      icon_basename=arguments['<basename>'],
                      out_filename=arguments['<out_filename>'],
                      bshow=arguments['--show'],
                      bdebug=arguments['--debug'] )
        
    print( 'Done!' )
