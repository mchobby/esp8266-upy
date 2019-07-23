[Ce fichier existe également en FRANCAIS](readme.md)

# File Format support for MicroPython
This section contains classes and examples to read various file format.

# IMAGE based format

## bmp format
BMP format is the Windows Bitmap file which have a variety of encoding algorithm.
This library support BMP  encoded with RGB888 (24 bits per Pixel).
The `BmpReader` from `imglib/bmp.py` can read  file content (as long its not compressed!).

* [color-palette.bmp](examples/color-palette.bmp): 24Bit uncompressed RGB bitmap sample.<br /> ![Sample 24Bit RGB bitmap](examples/color-palette.bmp)
* [olimex.bmp](examples/olimex.bmp): 24Bit uncompressed RGB bitmap sample.<br /> ![Sample 24Bit RGB bitmap](examples/olimex.bmp)

See the `examples/testbmp.py` to see how to extract pixel from such file.

Ressource: [bmp_file_format @ www.ece.ualberta.ca](http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm) from Nathan Liesch

## pbm format
1-bit black and white image; formatted in text format; basic raster image format in which each pixel is represented by a byte that contains a 1 or 0; 1 represents black and 0 represents white pixels.

Ressource: http://netpbm.sourceforge.net/doc/pbm.html

# IMAGE based helper (img)
The `imglib/img.py` library contains helper classes and functions.

The `ClipReader` class is made to offers image clipping (extract an image sub-section) service on the top of `xxxReader` classes. So, very useful to display a small part of a wide image onto a TFT ;-)

![Image clipping](docs/_static/clipping.jpg)

Notice that `ClipReader.show()` allows to inspect the content of the clipping in the terminal (display which characters, very usefull for debugging)!

![Image clip.show()](docs/_static/clip_show.jpg)

The `open_image()` is an helpher that identify the type of image based on file extension, create the appropriate reader (eg: `BmpReader` for .bmp file) and encapsulate it into a `ClipReader` to benefits from image clipping possibility.
