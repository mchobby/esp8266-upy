[Ce fichier existe également en FRANCAIS ici](readme.md)

# HT1632C Driver with Independent LED Control under MicroPython

The HT1632 a high performance LED Driver designed to creates LED matrix expansion. It provides independent register control for every LED in the LEDs matrix. This chip can drive 24 Row with 16 Commons pins or 32 Row with 8 Commons pins.

It is the chip used on the [FireBeetle Covers‑24×8 LED Matrix](https://www.dfrobot.com/product-1596.html) (DFRobot DFR0487).

![DFR0487: DFRobot FireBeetle Covers‑24×8 LED Matrix](docs/_static/fb_text.jpg)

The fine grained addressing enables flexible graphics, icons, and scrolling text effects without complex external circuitry. The chip integrated hardware management reduces firmware overhead while using a serial data communication between the display board and host controller,

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/ht1632c")
>>> mip.install("github:mchobby/esp8266-upy/FBGFX")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/ht1632c
mpremote mip install github:mchobby/esp8266-upy/FBGFX
```

# Wiring

Wiring the DFR0487 board requires only 3 wires (Data, WR, CS) and power supply.

The board can be used with 3.3V or 5V power supply. Just keep in mind that Data & WR pins are pull-up to supply voltage!

![HT1632C / DFR0487 wired to Raspberry-Pi Pico](docs/_static/dfr0487-to-pico.jpg)

| Pico | DFR0487  |
| ------- | --- |
| GND | GND |
| 3V3 | VCC |
| GP16 | WR |
| GP17 | DATA |
| GP18 | D2 (ChipSelect CS1) |

__Warning:__ do not use BLUE or WHITE LEDs display with 3.3V power. Indeed, the blue LED forward voltage from 2.8 to 3.7V whereas white LED requires a Fv of at least 3.0V. Note that green LEDs have a Fv voltage from 1.9 to 3.1V, so depending on the LED manufacturer, this may work under 3V3. Finally, red, orange & yellow LEDs are the best options with a Fv from 1.8 to 2.2V.

# Testing

As the HT1632C driver inherits from FrameBuffer, any drawing method supported by the FrameBuffer will applies to the target HC1632C display.

The following [bright.py](examples/bright.py) example script displays rectangles then use the brighness feature to pulse-in/pulse-out the brightness.

``` python
from machine import Pin
from ht1632c import HT1632C
import time

# Raspberry-Pi Pico 
# pin will be reconfigured by the driver
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )

# top,left, width,height Color=1
display.rect( 1,1, display.width-2, display.height-2, 1 )
display.rect( 3,3, display.width-6, display.height-6, 1 )
# Send data to display
display.show()

while True:
	for i in range(11): # 0..10
		display.brightness=i/10
		time.sleep_ms(100)
	for i in range( 9, 0, -1 ): #9..0
		display.brightness=i/10 
		time.sleep_ms(100)
```

Thanks to the __FBText__ class made available with the [FBGFX library](https://github.com/mchobby/esp8266-upy/tree/master/FBGFX), small text can be drawed on the display as demonstrated with [hello.py](examples/hello.py)

``` python
from machine import Pin
from ht1632c import HT1632C
from fbtext  import FBText
from font8x4 import Font8X4

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )
text_drawer = FBText( display, display.width, display.height, Font8X4() )

display.fill( 0 )
# Draw some text on the display FrameBuffer
text_drawer.text( "Hello", 0, 0, 1 ) 
# Send data to display
display.show()
```

Even better as __FBText__ draws into the FrameBuffer, some clipping can be used to scroll text on the display. Here follows the [scroll.py](examples/scroll.py) .

``` python
from machine import Pin
from ht1632c import HT1632C
from fbtext  import FBText
from font5x4 import Font5X4

# Raspberry-Pi Pico
wr_pin = Pin( 16 )
data_pin = Pin( 17 )
cs_pin = Pin( 18 )

display = HT1632C( data_pin, wr_pin, cs_pin )
font = Font5X4()
text_drawer = FBText( display, display.width, display.height, font )

display.fill( 0 )
# Draw some text on the display FrameBuffer
s = "Hello world!"
w = font.text_width(s)
while True:
	for y_pos in range( 28, -w-1, -1 ):
		display.fill(0)
		text_drawer.text( s, y_pos, 2, 1 ) 
		display.show()
		time.sleep_ms(50)
```
