[Ce fichier existe également en FRANCAIS](readme.md)

# Using NeoPixel / WS2812 with MicroPython

__Many micropython firmware do already support NeoPixel out-of-the-box__.<br />Take the necessary time to double check your firmware documentation before installing this library (ws2812 was designed for Pyboard).

The RGB WS2812 LEDs, also named NeoPixels by Adafruit, are smart LEDs able to provide lot of colorful light. They fit a large variety of products (Stip Led, ring, panel, etc.

![NeoPixels examples](docs/_static/neopixels.jpg)

To drive NeoPixels, only one MCU pin is required to drive a series of Neopixels (Arduino, ESP8266, Pyboard). Chaque pixel est adressable individuellement et propose un panel de couleur 24 bit sur chaque LED.

__Warning: use recent NeoPixels!__

The library included into MicroPython firmware does rely on last generation of NeoPixel (data stream at 800 KHz).

The library __does supports the following WS2812__:
* older NeoPixel hardware generation (data stream at 400 KHz)
* RGBW NeoPixel LEDs.

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/neopixel")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/neopixel
```

# Wiring
## ESP8266 under 3.3V

![ESP8266 Wiring to 3.3V](docs/_static/neopixel_bb.jpg)

| ESP8266 Pin | NeoPixel Pin | Remark
|----------------|------------------|------------------------------------------------------------------------------------------------------------|
| GND            | GND              |                                                                                                            |
| 3V             | 5V               | Neopixel does also works at 3.3V. They are less brighter. Data must also be at  3.3V |
| 2              | DIN              | The Data IN signal (do not confuse with Data OUT)                                    |

## ESP8266 under 5V

You can power the NeoPixels with 5V to have more brighter LEDs and more light are color more stable.

You will need a [Level Shifter 74AHCT125](http://df.mchobby.be/datasheet/74AHC125.pdf) (pdf) to up-lift the data signal from 3V to 5V.

![ESP8266 Wiring to 5V](docs/_static/neopixel-2_bb.jpg)

### ESP8266 - Compatible Pins

We do have tested tje NeoPixel library on the following ESP8266 pins:

| Pin | Compatibility |
|---|---|
| __14__ | NeoPixel compatible. |
| __12__ | _non testé._ |
| __13__ | NeoPixel compatible. |
| __15__ | NeoPixel compatible. |
| __0__  | __DO NOT USE__. Pin for the boot. |
| __16__ | __NOT WORKING__ with NeoPixel |
| __2__  | NeoPixel compatible. |
| __5__  | NeoPixel compatible. I2C Bus (SCL) |
| __4__  | NeoPixel compatible. I2C Bus (SDA) |

## Pyboard Under 5V

The origninal MicroPython Pyboard do not have embedded NeoPixel drivers but you will find many ressource on Internet like [micropython-ws2812](https://github.com/JanBednarik/micropython-ws2812) from JanBednarik.

__Do not forget to check if your recent firmware version did not include it already__.

The JanBednarik is included within this repository. Its interface have been slightly modified to be compatible with the ESP8266's NoePixel library.

![ESP8266 Wiring to 5V](docs/_static/pyboard-to-neopixel.jpg)

## Pyboard

The library do use the MOSI pin of a SPI bus to sent the data to NeoPixel LEDs.

You will need a SPI hardware bus able to send datas at 3.200.000 bauds

| Pin | Compatibility |
|---|---|
| __X8__ | MOSI bus SPI(1) |
| __Y8__ | MOSI bus SPI(2) |

# Test

## Basic example
```
# Using the Neopixel library on Feather ESP8266 with MicroPython
#
# Shop: https://shop.mchobby.be/55-leds-neopixels-et-dotstar
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from time import sleep

# -- LOAD LIBRARY ----------------------------------
# ESP8266 NEOPIXEL - utiliser bibliothèque native
from machine import Pin
from neopixel import NeoPixel

# Pyboard NEOPIXEL - utiliser bibliothèque WS2812
# from ws2812 import NeoPixel

# -- INSTANCIATE NEOPIXEL --------------------------
# ESP8266 NeoPixel( broche_signal, nbre_de_led )
np = NeoPixel( Pin(2), 8 )

# Pyboard NeoPixel( spi_bus=1, led_count=1, intensity=1 ) -> X8
# np = NeoPixel( spi_bus=1, led_count=8 )

# Set the color of the first pixel with a (r,g,b) tuple where each value
# is between 0 and 255
np[0] = (255,0,0) # rouge

# color for the other pixels
np[1] = (0, 255, 0) # vert
np[2] = (0, 0, 128) # bleu (1/2 brillance)

# See the HTML Color Picker
# https://www.w3schools.com/colors/colors_picker.asp
np[3] = (255, 102, 0) # Orange
np[4] = (255, 0, 102) # Pink
np[5] = (153, 51, 255) # Violet
np[6] = (102, 153, 255) # dilued blue
np[7] = (153, 255, 153) # dilued green

# Send data to the NeoPixels
np.write()

sleep(2)

# fill() sent the caolor to all the pixels
# with only one tuple color
colors = [ (255,0,0), (0, 255, 0), (0, 0, 128),
    (255, 102, 0) , (255, 0, 102), (153, 51, 128),
    (102, 153, 128), (153, 255, 128) ]

for color in colors:
    np.fill( color )
    np.write()
    sleep(2)

# Shutdown the Pixels
np.fill( (0,0,0) )
np.write()
```

## Light effects
This repository dies contains the `fxdemo.py` example. It contains many example function used to creates light effect with NeoPixels.

Here below, the script body does present the various light effect function.

```
# theater_chase sample
theater_chase( np, (127,0,0) ) # red
theater_chase( np, (127,127,127) ) # white
theater_chase( np, (0,0,127) ) # blue
clear( np )
sleep( 1 )

# Wipe in color
np.fill( (190, 0, 0) ) # fill in red
np.write()
wipe( np, (0,180,0), pause=0.150 ) # wipe in green
wipe( np, (0,0,255), pause=0.150 ) # wipe in blue
wipe( np, (0,0,0),   pause=0.150 ) # wipe in black
sleep( 1 )

# Moving_rainbow
for i in range( 4 ):
	moving_rainbow( np )
clear( np )
sleep( 1 )

# Fade In And Out
fade_inout( np, (255,   0,   0) ) # Red
fade_inout( np, (0  , 255,   0) ) # Green
fade_inout( np, (0  ,   0, 255) ) # Blue
clear( np )
sleep( 1 )

# moving_wheel
moving_wheel( np )
clear( np )
sleep( 1 )

# cycle_wheel
for i in range(2):
	cycle_wheel( np )
clear( np )
sleep( 1 )

# Candle Effect
candle( np )
clear( np )
sleep( 1 )

# Larson Scanner (K2000)
#   execute 3 iterations
posdir = None
for i in range( 3 ):
	posdir = larson_scanner( np, posdir )
clear( np )
sleep( 1 )
```

# Source and ressources
* [NeoPixel under ESP8266 (official reference)](http://docs.micropython.org/en/v1.8.2/esp8266/esp8266/tutorial/neopixel.html)
* (Originale WS2512 library from JanBednarik](https://github.com/JanBednarik/micropython-ws2812)
* [NeoPixel Wiki with avec ESP8266](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython)

# Shopping list
* Shop: [Gamme NeoPixel](https://shop.mchobby.be/55-leds-neopixels-et-dotstar)
* Shop: [NeoPixel Stick](https://shop.mchobby.be/leds-neopixels-et-dotstar/407-stick-neopixel-8-leds-rgb--3232100004078-adafruit.html) as used in this sample.
