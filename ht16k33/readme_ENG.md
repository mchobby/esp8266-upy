## HT16K33 Led Matrix I2C controler library for MicroPython

The __ht16k33__ can be used in various products from various manufacturer.
![ht16k33 usages](docs/_static/ht16k33.jpg)

This library covers the HT16K33 and its implementation for several breakout manufacturers. 

Despite the minimal implementation, hardware support can be added for other breakout.

## Credit

This library is originated from [hybotix/micropython-ht16k33](https://github.com/hybotix/micropython-ht16k33) then properly documented and adapted to fits requirements of the esp8266-upy repository.

__Original readme:__

Micropython Library for the HT16K33-based LED Matrices, ported from Adafruit's Adafruit_CircuitPython_HT16K33 library.

It supports Adafruit's 16x8 and 8x8 matrices, as well as 7-segment numeric and 14-segment alphanumeric displays.

The code for the matrix displays are here and should just work. However, I can not test these because I do not have any of these displays.

NOTE: At this time, only the 14-segment alphanumeric and 7-segment numeric displays have been tested. Others may work but have not been tested. Be warned!

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/ht16k33")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/ht16k33
```

# Wiring
Adafruit product can be wired with Qwiic/Stemma câble or by wiring the SDA/SCL lines to the microcontroler I2C bus.

## Wiring to Pico
![4x7 Segment to Pico](docs/_static/seg4x7-to-pico.jpg)

# Test
The __ht16k33__ can be used in various products (and various manufacturer).

## Adafruit 4x7 segment display

![4x7 Segment from Adafruit Industries](docs/_static/seg4x7-adafruit.jpg)

The following content shows the main library features:

* `fill(0)` : Do clear the screen by filling it with the color 0.
* `print()` : Can show an integer, decimal value or time (string with colon).
* `print_hex()` : Show an Hexadecimal value.
* `marquee()` : display a string (make it scrolling on the screen).

```
from machine import I2C, Pin
from ht16k33.adafruit.segments import Seg7x4 # Seg14x4

i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )
display = Seg7x4(i2c, address=0x70)

display.fill(0)
# Integer
display.print( 3141, auto_round=True )
# Float
display.print( 29.2545, decimal=2 )
# Hexadecimal
display.print_hex( 0xBEAD )
# Time
display.print( '10:22' )
# 
display.marquee("Maison 192.168.100.102", 0.2, loop=False)
```

See the [examples/adafruit/segments_simpletest.py](examples/adafruit/segments_simpletest.py) for living example.