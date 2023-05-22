[Ce fichier existe aussi en FRANCAIS](readme.md)

# Is this the first round screen working under MicroPython ?
DFRobot distribue a [2.2” TFT LCD display (SPI interface) under the reference DFR0529](https://www.dfrobot.com/product-1794.html).

![2.2" DFRobot Round display](docs/_static/text_display.jpg)

What's exciting with this screen is its shape!

The display uses a __ST7687S display controler__ with a SPI interface, coupled to a 8 bits shift register (HC595). This combination is known as "ST7687S with Latch" and it need more signals changes than a simple SPI driver.

The round display is cutout into a squared TFT display of 128px * 128 px (so only 79% of the pixels are visible).

![2.2" DFRobot Round display showing a bitmap](docs/_static/bmp_display.jpg)

You can have more details about this screen on the [TFT-2.2pc-ROND product sheet](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/1856-tft-couleur-22-rond-spi-breakout-3232100018563-dfrobot.html).

__Advantages:__
* Direct access to the screen memory without using any MicroPython FrameBuffer... __so spare RAM__ on the MCU.
* Acces to the Pixel
* Round screen cutout into a square TFT area (of 128px * 128px)
* 180° angle of view (cfr. see TFT specification)
* The driver handle geometrical shape drawing as well as text drawing
* Backlight control.

__Disadvantages:__
* Data rate slow down because of the Latch handling (HC595).<br />Fill the screen needs up to 5 seconds.
* Graphical animation and bitmap transfert restricted by the data rate.

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/st7687s")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/st7687s
```

## Portage limit
The portage to MicroPython did handle almost all of the initial functions.

The following functions from [DFRobot_Display.cpp](https://raw.githubusercontent.com/DFRobot/DFRobot_Display/master/DFRobot_Display.cpp) have not been ported to the MicroPython implementation.
* fillCircleHelper()
* circleHelper()
* fillRoundRect()
* drawRoundRect()

## View it in a Vidéo
This [vidéo YouTube](https://youtu.be/ceWs7rgPLbw) demonstrate the `test_simple.py` script.

# Wiring

## MicroPython Pyboard

![ST7687S to MicroPython Pyboard](docs/_static/st7687s-to-pyboard.jpg)

# Test

## The libraries
Several libraries are required to make this screen running. They are available under the `lib/` folder.

The libraries must be copied to the MicroPython board before using the examples.

* `st7687s.py` : contains the hardware control class and basic function for drawing pixels into the screen memory buffer.  
* `display.py` : contains Helper classes used to draw shape and text on the screen via the `st7687s` driver (ported from DFRobot's display.cpp).
* `character.py` : contains the 6x8 pixels font definition.

## Axis origin
On a classical square/rectangular display, the axis origin is usually at the top-lef corner of the screen (this is the case for `st7687s.py`).

however, this is not clearly the best choice for a round screen!

The `Display` drawing class move the axis origin at the center of the screen. This makes the code writing quite more natural, more comprehensive and simplier.

![Axis](docs/_static/axis.jpg)

## test_simple.py example
The [test_simple.py](example/test_simple.py) script, visible here below, shows the basic features of the library.

The first action of the script is to light off and on the backlight several times.
This is obtained by writing a simple command byte to the screen controler. This is the best example to double check the wiring and code.

See this [YouTube video](https://youtu.be/ceWs7rgPLbw).

```
from machine import Pin, SPI
from st7687s import ST7687S_Latch
from display import *
from time import sleep

# Color handling -> from COLORS/colortls.py
def rgb24_to_rgb16( r,g,b ):
	""" Convert RGB888 to RGB565 """
	return (  ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) )

# Pin definition
# Pyboard:
SPI_BUS = 2
CS  = "X1"
RS  = "X3" # Command mode
WR  = "X4"
LCK = "Y5"

spi = SPI( SPI_BUS, polarity=0, phase=0) # mode 0: CPOL=0, CPHA=0
cs = Pin(CS, Pin.OUT ) # Slave activation
rs = Pin(RS, Pin.OUT ) # Command mode
wr = Pin(WR, Pin.OUT )
lck= Pin(LCK,Pin.OUT )

lcd = ST7687S_Latch( spi, cs,  rs, wr, lck)
# Helper class that draws directly to the display's BufferMemory
disp = Display( lcd, 128, 128 )

#--- Switch off/on the backlight ---
for i in range(5):
	lcd.turn_on(False)
	sleep(0.4)
	lcd.turn_on(True)
	sleep(0.4)

# Clear the screen
disp.clear( rgb24_to_rgb16(255,0,0) ) # Fill it in RED

print( "Part 1" )
disp.clear( 0x0000 ) # Black
disp.circle( (0, 0), 20, DISPLAY_GREEN) # circle at (0, 0) and  radius = 20
disp.rect ( (-20,-30) , 40, 60, DISPLAY_CYAN ) # rectangle (-20, -30), width = 40, height = 60
disp.line ( (-64,-64) , (64,64), DISPLAY_RED);  # line from (-64, -64) to (64, 64)
# Draw a series of line
for y in range(-64,64,3):
	disp.line( (-64,64), (64,y), DISPLAY_PINK )
disp.hline( (-64, 0), 128, DISPLAY_WHITE)   # horizontal line at (-64, 0), length = 128
disp.vline( (0, -64), 128, DISPLAY_WHITE)   # vertical line at (0, -128), length = 128

print( "Part 2" )
disp.clear( DISPLAY_LIGHTGREY )
disp.triangle( (-20,-50), (0,0), (50,20), DISPLAY_ORANGE ) # triangle with 3 points at coordonates (-20, -50), (0, 0), (50, 20)
disp.circle( (0, 0) , 20, DISPLAY_GREEN) # drawing a circle (0, 0) and radius = 20
disp.fill_circle( (0,0) , 20, DISPLAY_GREEN)
disp.fill_rect( (-20,-20), 40, 40, DISPLAY_CYAN) # (-20, -30), width = 40, height = 40
disp.fill_triangle( (-20,-50), (-20,0), (50,20), DISPLAY_ORANGE )
```

## Other examples
The folder [examples](examples/) contains other examples:
* [test_text.py](examples/test_text.py) : text drawing on the screen
* [test_clear.py](examples/test_clear.py) : Comparing the `fill_screen()` and `clear()` method to completely fills the screen.
* [test_bmp.py](examples/test_bmp.py) : transfert the content of the mpy.bmp image to the screen.
* [char68tobin.py](examples/char68tobin.py) : script used to generate the binary content for the [character.py](lib/character.py) library

# Shopping list
* [The 2.2” TFT LCD display (SPI interface) under the DFR0529 reference](https://www.dfrobot.com/product-1794.html) est disponible chez MCHobby.
* [The 2.2” TFT LCD display (SPI interface) under the DFR0529 reference](https://www.dfrobot.com/product-1794.html) chez DFRobot.
* [MicroPython PYBStick](https://shop.mchobby.be/fr/micropython/1844-pybstick-standard-26-micropython-et-arduino-3232100018440-garatronic.html)
* [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)
