[Ce fichier existe également en FRANCAIS](readme.md)

# A lighter font for MicroPython FrameBuffer

![SMALL-FONT examples](docs/_static/small-font.jpg)

MicroPython does offer a `FrameBuffer` class to write display drivers (OLED, TFT, etc).

The `FrameBuffer` class is used to draw lines, rectangle, circle and text.

However, the default MicroPython font is a bit "fat", which is not very aesthetic to draw text on small screen.

It exists two other options for Font drawing:
* __SMALL-FONT__ : __this project__ allows to write text with less thicker font (coming from [st7687s display driver](https://github.com/mchobby/esp8266-upy/tree/master/st7687s) ).
* __FreeType-Generator__ : [an alternative project](https://github.com/mchobby/freetype-generator) creating a binary file for Fonts under MicroPython. File used with the FontDrawer class to draw text into the FrameBuffer.

# Using

The SMALL-FONT project is mainly made of the `FontDrawer` class stored in [lib/sfont.py](lib/sfont.py) (_Small Font_).

The `FontDrawer` class constructor does takes the `FrameBuffer` parameter, so it is compatible with all graphical drivers based FrameBuffer. You can still use all the posibilities offered by the original driver.

As example, we do use a [OLED display based on the official SSD1306 driver from MicroPython.org as described here](https://github.com/mchobby/esp8266-upy/tree/master/oled-ssd1306).

The [test_oled_i2c.py](examples/test_oled_i2c.py) example, visible here below, show how to use SMALL-FONT on various display using a `FrameBuffer` .

1. You need to created a `FontDrawer` instance by providing the FrameBuffer as parameter.
2. Then, calling the method __text() of FontDrawer__ will draw the desired text into the display's FrameBuffer.  

``` python
from machine import Pin, I2C
import time
import ssd1306
from sfont import FontDrawer

i2c = I2C( sda=Pin(23), scl=Pin(22) ) # ESP32
# i2c = I2C( sda=Pin(4), scl=Pin(5) ) # ESP8266

lcd = ssd1306.SSD1306_I2C( 128, 32, i2c )
fd = FontDrawer( lcd, font_color=1, bgcolor=0 )

# Drawing with MicroPython font
lcd.text( "MicroPython! <3", 0, 0 )

# Standard FrameBuffer Drawing (horizontal line)
lcd.hline( 0, 16, 128, 1 ) #x,y, width, color

# Print with small font (use the font drawer)
fd.text( "MicroPython! <3", 0, 20 )

lcd.show()  # display / Afficher!
```
Which produce the following results:

![small font example](docs/_static/small-font.jpg)
