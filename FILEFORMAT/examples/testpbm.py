# Test the PBM reading and clipping by displaying the content to the consile
#
# bpm & img libraries: https://github.com/mchobby/esp8266-upy/tree/master/FILEFORMAT/imglib
# mpy.pbm : image bitmap of older MicroPython logo
#
from img import open_image

reader = open_image( 'mpy.pbm' )
reader.show() # Show the clipping area --> so the full image

reader.clip( 49,6, 29, 44 ) # x, y, w, h
reader.show()
