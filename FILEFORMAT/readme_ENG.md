[Ce fichier existe également en FRANCAIS](readme.md)

==========TRANSLATE========================================

# File format support for MicroPython
This section contains class and examples to read various file format.

This is based on READER principle which moves seek cursor in file and read the data as needed.

This is avoids to load the file into memory and overload it (an important feature when running on MicroControler).

In counterpart, this also imply for file access and more byto to byte transfer (so it is also slower).

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/FILEFORMAT")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/FILEFORMAT
```

# IMAGES (supported format)

## BMP format
BMP is the Windows Bitmap format covering a wide variety of encoding (Bits per color, indexed color or not, compression or not, etc).
This library would support the following BMP formats:
* RGB888 (24 bits per Pixel).

While using editing tool (eg: Gimp), the RGB888 format must be saved with the following settings:

![Format RGB888 dans gimp](docs/_static/RGB888_config.jpg)

The "do not write data into the color space section" must be tick.

The `BmpReader` class from `imglib/bmp.py` is designed to read this kind of file (data cannot be compressed!).

Example files:
* [color-palette.bmp](examples/color-palette.bmp): 24 bits bmp picture (not compressed).<br /> ![Exemple de bitmap 24Bit](examples/color-palette.bmp)
* [olimex.bmp](examples/olimex.bmp): 24 bits bmp picture (not compressed).<br /> ![Exemple de bitmap 24Bit](examples/olimex.bmp)

See the [testbmp.py](examples/testbmp.py) to see how to use the `BmpReader`, `ClipReader` and `open_image()` tools to read from bmp file.

``` python
from img import open_image

# open_image() returns a ClipReader objet
clip = open_image( 'olimex.bmp' )
clip.show() # Display as text on the console

# Select an area on the image
clip.clip( 2,2,20,16 ) # x,y, w, h
# Display pixels information
for y in range( clip.height ):
	print( "--- Clip Line %i ---------" % y )
	for x in range( clip.width ):
		print( "(%i,%i) : %s" % (x,y,clip.read_pix()) ) #x,y, color
clip.close()
```

Ressources:
* [bmp_file_format @ www.ece.ualberta.ca](http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm) from Nathan Liesch


## The PBM format (Portable Bit Map)
The PBM is used to encore 2 color images (1 bit color, white/black). It does exists a text based format version (verbose) and a binary format (more compact).

Create a PBM file is quite easy with tool like Gimp. Load the image into Gimp then select the `File | Exporter as...` menu entry. Name your exported file with `.pbm` extension. __No need for color filtering and treatment, Gimp does applu a filter that perfectly degrade the colors to white/black image__.

Just before saving the file, Gimp will request the user to select the final file format to be used.

Just select the RAW option (binary format) :

![Gimp Pbm export](docs/_static/pbm_export.jpg)


The `imglib/pbm.py` library contains the `PbmReader` class used to read such file. See the [examples/mpy.pbm](examples/mpy.pbm) example file (visible here below, converted to Jpeg to made it visible to you).

![Content of mpy.pbm file as jpeg](docs/_static/mpy_pbm.jpg)

The [testpbm.py](examples/testpbm.py) example script loads the `mpy.pbm` from the file system then displays its content to the REPL console.

``` python
from img import open_image

reader = open_image( 'mpy.pbm' )
reader.show() # Affiche la zone de clipping  --> toute l'image
```

![Full display on the console](docs/_static/mpy_pbm_show_0.jpg)

![Full display on the console](docs/_static/mpy_pbm_show_1.jpg)

This example also contains a clipping operation used to select the "snake head" in the picture... then display the selected area on the REPL console.

``` python
from img import open_image

reader = open_image( 'mpy.pbm' )
# reader.show() example here above

# Select the snake head only
reader.clip( 49,6, 29, 44 ) # x, y, w, h
reader.show()
```

![Full display on the console](docs/_static/mpy_pbm_show_2.jpg)

The [testpbmlcd.py](examples/testpbmlcd.py) example script does load/cpy the [mpy.pbm](examples/mpy.pbm) 128*64 image pixels into the LCD FrameBuffer.

See the [esp8266-upy/lcdspi-lcd12864](https://github.com/mchobby/esp8266-upy/tree/master/lcdspi-lcd12864/lib) github for more information about wiring.

``` python
from machine import SPI, Pin
from lcd12864 import SPI_LCD12864
from img import open_image
import time

# PYBStick: S19=mosi, S23=sck, S26=/ss
cs = Pin( 'S26', Pin.OUT, value=0 )
spi = SPI( 1 )
spi.init( polarity=0, phase=1 )

lcd = SPI_LCD12864( spi=spi, cs=cs )


def color_transform( rgb ):
	# Transform the clipreader (r,g,b) color to LCD FrameBuffer color (1 bit color)
	return 0 if rgb==(0,0,0) else 1

reader = open_image( 'mpy.pbm' )
# Select a clipping area in the picture (fit it to the size of LCD)
reader.clip(0,0,lcd.width,lcd.height)
# Copy the clipped aread to the LCD FrameBuffer. This copy starts at coordinates
# 0,0 of LCD target. The copied height & width are those of the clipping area.
reader.copy_to(lcd, 0,0, color_transform )
lcd.update()
```

![The result of the copy](docs/_static/mpy_pbm_lcd.jpg)


Ressources:
* http://netpbm.sourceforge.net/doc/pbm.html
* https://en.wikipedia.org/wiki/Netpbm#PBM_example

# img.py - the helper library
The `imglib/img.py` library contains tooling classes and functions.

## open_image()

The `open_image()` helper function does detect the image type based on the file extension. It creates the proper `Reader` class and wrap it into a `ClipReader` to benefit from clipping, pixel per pixel reading, copy to frame buffer operations.

* `.bmp` : `BmpReader` class
* `.pbm` : `PbmReader` class

## Other functions

* `grayscale( r,g,b )` : compute a gray scale value (0..232) from a RGB888 (r,g,b) color tuple
* `charpix( r,g,b )` : compute displayable char in (' ', '.' '-', '+', '*', 'X') from the RGB888 (r,g,b) color tuple. Color is degraded to gray scale before the char conversion.

## ClipReader class

The `ClipReader` class feature an image clipping operation over a reader class (so you can extract a sub-section of an image). The ClipReader class relies on the API offered by the Reader classes available.

The `ClipReader` class is quite usefull to extract a part of an image to be displayed onto a LCD/OLED/TFT ;-)

* `ClipReader.clip( self, x, y, width, height )` : allow to set the clipping area for reading the pixels on the image. This update the `height` & `width` properties.

![Image clipping](docs/_static/clipping.jpg)

* `ClipReader.read_pix( pos=None )` : reads the next pixel from the clipping area with automatic line return (allowing continuous pixel reading). This method return a RGB888 (r,g,b) tuple returned by the Reader. If `pos` contains a (x,y) tuple then the file cursor is moved at the x,y pixel in the clipping area before reading the pixel color.

* `ClipReader.copy_to( self, target_fb, x,y, color_fn )` : Push a copy of the clipping area into the `target_fb` FrameBuffer. The copy is inserted into the `target_fb` at the x,y position. The `color_fn( rgb_tuple )` function given as parameter is will transform the (r,g,b) tuple into the numerical value inserted into the target FrameBuffer.

* `ClipReader.show()` : used to inspect the clipping aread into the terminal (Text based format, useful to display into REPL console))!

![Image clip.show()](docs/_static/clip_show.jpg)
