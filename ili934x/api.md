# ILI934x API

This file contains the description of the API used on the ILI934x drivers.

This driver use RGB565 16bits colors encoded into an 16 bits integer with the `color565(r, g, b)` library function.

# Library functions and constants

## Color constants
The library already includes somes COLOR constant which are the follow:
`BLACK, NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE, LIGHTGREY, DARKGREY,
BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE, ORANGE, GREENYELLOW`

## color565(r, g, b)

Encode a 24 bits color where `r`, `g`, `b` are values between 0 & 255.

The function returns a RGB565 integer value (fits into a 16 bits integer).

# ILI9341 class - General feature

## __init__( spi, cs, dc, rst, w, h, r )
* spi: initialised machine.spi bus attached to the TFT
* cs: pin name of TFT _Chip Select_ line. Will be initialized by the driver.
* dc: pin name of TFT _Data Command_ line. Will be initialized by the driver.
* rst: (optional) pin name of TFT _Reset_ line. Can be None when not used. Will be initialized by the driver.
* w: TFT width in pixels
* h: TFT height in pixels
* r: rotation (see _rotation_ property here below).

Initialisation of the TFT screen and its property.
Also initialize the default colors for foreground (white) and background (black).

Here is the minimal code for starting the driver as shown in the [test_main.py](examples/test_main.py) example.

``` python
from ili934x import ILI9341
from machine import Pin, SPI

# PYBStick config (idem with PYBStick-Feather-Face)
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

# r in 0..3 is rotation, r in 4..7 = rotation+miroring
lcd = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=0)

lcd.erase()      # Clear the screen
lcd.set_pos(0,0) # Original cursor position for text display
lcd.print("Hello world")
```

## set_color( fg, bg )

Set the forground dans backgound color with color565 integers. The color565 integer are generated with the `color565(r, g, b)` function.

## blit( bitbuff, x, y, w, h )

Draw a bitbuff FrameBuffer MONO_VLSB at positions. Used by font drawing.

# ILI9341 class - Properties

## height, width
Height and width of the screen in pixel. These values are permutated accordingly to the screen _rotation_ .

## rotation
Display content rotation as defined @ class creation.

* rotation in 0..3: rotation.
* rotation in 4..7: rotation+miroring

1 & 3 = __landscape__ with width=320 height=240

0 & 2 = __portrait__ with width=240 height=320

## scrolling
Returns a boolean value stating of the scrolling state. This may append when displaying text with many lines.

This is resetted by `reset_scroll()` method.

# ILI9341 class - Drawing primitives

## erase()

Clear the screen content with the background color (black).

## fill( c )
__FrameBuffer MIMIC__

Fill the screen with a given color.


## pixel( x, y, color=None )

__FrameBuffer MIMIC__

Draw a pixel at x,y position with the given color565.

If color=`None` then it returns the color565 of the `x,y` pixel.

See the example [test_pixel.py](examples/test_pixel.py)

![test pixel results](examples/test_pixel.jpg)

## hline( x, y, w, c, tick=1 )

__FrameBuffer MIMIC__

Draw an horizontal (optimized) having `w` pixels large line from the `x`,`y` position with the given `c` (color565).

The `tick` extra parameter (tickness) with __default value 1__ can be used to draw ticker lines :-)

See the example [test_hlines.py](examples/test_hlines.py)

![Horizontal lines](examples/test_hlines.jpg)

## vline( x, y, h, c, tick=1 )

__FrameBuffer MIMIC__

Draw vertical line (optimized) having `h` pixels height. see `hline()` for description.

See the example [test_vlines.py](examples/test_vlines.py)  

![vline results](examples/test_vlines.jpg)

## rect( x,y, w,h, c )

__FrameBuffer MIMIC__

Draw a rectangle with top-left corner at `x,y` and having `w` pixels width & `h` pixels height.

![rect results](examples/test_rect.jpg)

## fill_rect( x,y, w,h, c )

__FrameBuffer MIMIC__

Same as `rect()` except that it fills the rectangle.

Draw and fill a rectangle with the 565color value.
* x: x starting position
* y: y starting position
* w: rectangle width
* h: rectange height
* color: 16bit color to fill with (otherwise it use the background color)

See example [test_fill_rect.py](examples/test_fill_rect.py)

![test_fill_rect result](examples/test_fill_rect.jpg)

# ILI9341 class - Text display

Prior to print any text, a `FontDrawer` instance must be assigned to the `font` property prior to call any text display function.

The text display routine inside the driver does manage the `\n` character to wrap lines.

See the examples [test_print.py](examples/test_print.py) as HowTo Guide.

Please note that `FontDrawer` can also be used to draw directly text on a FrameBuffer (or the driver) as showned in the [test_fdrawer.py](examples/test_fdrawer.py) .

## set_pos( x, y )

Set the cursor position @ x,y position. Also impact the text display routine.

## chars( str, x, y )

Draw one or several characters at arbitrary x,y position.

Does not modifies the x,y cursor position.

Returns: x+string_length

## print( text )

Draw text on screen with WORD wrap and scrolls the screen when going over the screen area.

Print text on a new line @ each call.

Required the `font` to be assigned.

note: Leaves x unchanged, so lines can be displayed within a column from `set_pos(x,y)` .

__Bug:__ screen scrolling is now working properly in rotation 3!

## write( text )

Draw text on a line with CHARACTER wrap at the end of the line. Also support line wrap with `\n`.

Note: Compatible with stream output.

__Bug:__ CHARACTER wrap at the end of the line does raise en TypeError in rotation 3!

## next_line( cury, char_h )

TO DOCUMENT

## scroll( dy )

Make the screen scrolling by `dy` pixels (can be negative).

Useful to create scrolling text.

## scroll_reset()

Reset the scroll feature.
