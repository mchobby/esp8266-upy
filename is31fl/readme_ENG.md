[Ce fichier existe également en FRANCAIS](readme.md)

# Control a CharliePlexing LED matrix with the IS31FL3731

The IS31FL3731 chip used the charlieplexing method to control a large quantity of LEDs. Each LED can be controlled individually with 256 level of brightness (thanks to PWM support).

This component can work under 3V and is driven via the I2C bus. As it also have some memory you can store up to 8 frames, great to create some animations on the display.

A [15x7 CharliePlexing FeatherWing extension for Feather](https://shop.mchobby.be/product.php?id_product=1563) is used to demonstrate the usage of the driver.

![ChaliePlexing 15x7 Feather Wing from Adafruit](docs/_static/featherwing-charlieplexing-adafruit.jpg)

# Wiring

## with MicroPython Pyboard
![CharliePlexing Matrix on Pyboard](docs/_static/pyboard-to-charlieplexing.jpg)

## with MicroPython PYBStick
![CharliePlexing matrix on PYBStick-26](docs/_static/pybstick-to-charlieplexing.jpg)

# Test
The `CharlieWing` MicroPython driver (is31fl3731.py) must be present on the MicroPython board.

It exist  several matrix display control class:
* `Matrix` : 16 x 9 pixels (base class).
* `CharlieWing` : 15 x 7 pixels matrix
* `CharlieBonnet` : 16 x 8 pixels matrix

Here is the content of the `[test_simple.py](examples/test_simple.py)` script wich draw a mine all around the display:

![Result of test_simple](docs/_static/test_simple.jpg)

```
from machine import I2C
import is31fl3731 as is31f

# Create I2C bus
# Y9=scl, Y10=sda (same for Pyboard-Uno-R3 with I2C over tge pin 13)
i2c = I2C(2)

# Init the CharliePlexing FeatherWing 15 x 7 LEDs
display = is31f.CharlieWing(i2c)

# Draw a box on display
# First the top and low lines
for x in range(display.width):
    display.pixel(x, 0, 50)
    display.pixel(x, display.height - 1, 50)
# then tge right and left borders
for y in range(display.height):
    display.pixel(0, y, 50)
    display.pixel(display.width - 1, y, 50)
```  

This second example show how to use a `FrameBuffer` instance with the display

The code is available on `[test_text.py](examples/test_text.py)` .

![Result of test_text](docs/_static/test_text.jpg)

```
from machine import I2C
import framebuf
import is31fl3731 as is31f
import time

i2c = I2C(2) # Y9=scl, Y10=sda (idem for Pyboard-Uno-R3, the I2C bus over tge pin 13)

# Initialize a CharliePlexing 15 x 7 LEDs FeatherWing
display = is31f.CharlieWing(i2c)

# Create the FrameBuffer
# 15x7 LEDs (ADA3134) - 1bit_color * 15 columns of 7 pixels = 1bit_color * 15 * 8 bits_per_column = 15 bytes to store data
buf = bytearray(15)
fb = framebuf.FrameBuffer( buf, display.width, display.height,
			framebuf.MVLSB ) # Monochrom 1 bit color, vertical arranged bits, 1st bit on the top
fb.fill(0)
fb.text( "123", 0, 1) # X,Y, color

display.frame( 0 , show=False)
display.fill(0)

# Transfert the FrameBuffer to the display
for x in range(display.width):
	# use the drawing result from FrameBuffer operation
	bite = buf[x]
	for y in range(display.height):
		bit = 1 << y & bite
		# if bit > 0 then set brightness
		if bit:
			display.pixel(x, y, 50) # x,y,couleur=luminosité(0..255)

# Now the frame is filled -> Display it
display.frame(0, show=True)
```

Here is a list of the various examples:
* [`test_simple.py`](examples/test_simple.py) : Draw a border all around the display.
* [`test_frame.py`](examples/test_frame.py) : Display a moving heart on the display. Use the frames to make a animation.
* [`test_blink.py`](examples/test_blink.py) : draw a blinking arrow.
* [`test_text.py`](examples/test_text.py) : Use the FrameBuffer to draw a text on the display.
* [`test_textscroll.py`](examples/test_textscroll.py) : Scrolling text (also use FramBuffer).
* [`test_wave.py`](examples/test_wave.py) : Display a moving wave on the display.

Some other images coming from examples:
![test blink](docs/_static/test_blink.jpg)  ![test wave](docs/_static/test_wave.jpg)

# Shopping List
* [15x7 CharliePlexing for Feather board](https://shop.mchobby.be/product.php?id_product=1563)
* [MicroPython PYBStick](https://shop.mchobby.be/fr/micropython/1844-pybstick-standard-26-micropython-et-arduino-3232100018440-garatronic.html)
* [MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)
