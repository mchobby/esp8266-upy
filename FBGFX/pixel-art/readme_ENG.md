# 1bit pixel art icons

This folder contains icons ressources that can used in your own project.

Those ressources will be converted to python file then could be drawed with
 {{fname|icontls.py}} library.

## The ressources 

The icon ressources were collected on itch.io and stored in their original form into sub-folder. The sub-folder also contains text file with description, source url, license, etc.

Examples:

* mystery-icons
* one-bit-dog-puppy
* one-bit pixel-icons
* one-bit-prison
* one-bit-space-arcade
* one-bit-tileset
* ...

Icons are usually made available into image file like the following one:

![__Icons_Weather.png__ from __one-bit-pixel-icons__ subdirectory](one-bit-pixel-icons/Icons_Weather.png)

__Remark:__ All selected icons should be free for use.

## PBM icon file

PBM stand for Portable Bit Map and is used to encode a two color image (1 bit per pixel). Converted PBM file are stored into the the __sub-folder.bpm__ directory

MicroPython can read PBM file by using this [FILEFORMAT library](https://github.com/mchobby/esp8266-upy/tree/master/FILEFORMAT) . That librrary can open the image and transfert its content to a display FrameBuffer. The great thing about the FILEFORMAT library is the __ClipReader__ class allowing an __area selection__ within the image before copying its content to the target FrameBuffer. Exactly what we need to copy an icon.

## Python icon files

The original ressource are __converted__ into their Python representation by using
some scripts.

The resulting python file is stored into the __sub-folder.lib__ directory.

![Automatic naming of icons](convert-to-fbgfx-icon.jpg)

The icons are automatically named depending on their position in the original 
ressource image.

__Recommendation:__ As the generated python script may be quite large (eg: 63Ko for software icons), it may be appropriate to copy/paste the definition of interest into your project. This would avoids to overload the memory with file parsing and icon storage that will not be use.

__By example:__ the image [one-bit-pixel-icons/Icons_Weather.png](one-bit-pixel-icons/Icons_Weather.png) will be converted to icons stored into [one-bit-pixel-icons.lib/iweather.py](one-bit-pixel-icons.lib/iweather.py)

## Converter
__The binary pbm files__ are created with the Gimp software.

__The icons are converted__ with pyhton script like {{fname|convert-to-fbgfx-icon.py}} that slice the original image and create the target python file.

The conversion process is managed by the [generate.sh](generate.sh) shell script. 