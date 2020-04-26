# Reduced micropython-dotstar library -> dotstar.py

This library is based on the work of [micropython-dotstar](https://github.com/mattytrentini/micropython-dotstar) to control DotStar LEDs (APA102). This original GitHub contains the examples for the library.

The code has been prune (remove of comments) and some code __to allow the parsing on lower RAM MicroPython board__ (like Pyboard Lite or PYBStick). The file header (with CopyRight, author, etc) is now stored in `dotstar.header` file.

The dynamic ribbon brightness change has been removed because it allocates a second full buffer (even for 10ms it is too much for lighter board).

Global brightness can still be defined via the `brightness` property (from 0.1 to 1.0).

Each LED can still receive its own brightness as a 4th color parameter like show in the code below

```
MicroPython v1.12-256-geae495a-dirty on 2020-03-18; PYBSTICK26_LITE with STM32F411CE
Type "help()" for more information.
>>>
>>> from machine import SPI, Pin
>>> spi = SPI( sck=Pin("S23"), mosi=Pin("S19"), miso=Pin("S21") )
>>> from dotstar import DotStar
>>> leds = DotStar( spi, 3 )
>>> # Fill in RED
>>> leds.fill( (255,0,0) )
>>> # 3 degree of brightness for Blue (0,0,255)
>>> leds[0] = (0,0,255,0.1) 
>>> leds[1] = (0,0,255,0.5) 
>>> leds[2] = (0,0,255,1) 
```
