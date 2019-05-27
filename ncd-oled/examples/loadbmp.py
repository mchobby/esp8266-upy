"""
Test the NCD OLED Display (I2C) board from National Control Device.

Load an bpm (Bitmap Portable) image and display it on the OLED display over I2C bus.

NCD-I2COLED : http://shop.mchobby.be/
NCD-I2COLED : https://store.ncd.io/product/oled-128x64-graphic-display-i2c-mini-module/

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from machine import I2C, Pin
import ssd1306
import framebuf
import time

# Create the I2C bus accordingly to your plateform.

# --- ESP8266 ---
# Feather ESP8266 & Wemos D1: sda=4, scl=5.
# i2c = I2C( sda=Pin(4), scl=Pin(5) )
# ESP8266-EVB
# i2c = I2C( sda=Pin(6), scl=Pin(5) )
# lcd = ssd1306.SSD1306_I2C( 128, 64, i2c , addr=0x78)

# --- PYBOARD ---
# WARNING: On pyboard, the ssd1306 driver is written for machine.I2C (not pyb.I2C)
#          and I2C bus must be instanciate against specific Pin configuration
#          see Topic https://forum.micropython.org/viewtopic.php?f=6&t=4663
# Pyboard: SDA on Y9, SCL on Y10. See NCD wiring on https://github.com/mchobby/pyboard-driver/tree/master/NCD
#
pscl = Pin('Y9', Pin.OUT_PP)
psda = Pin('Y10', Pin.OUT_PP)
i2c = I2C(scl=pscl, sda=psda)
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c )

lcd.fill(1) # Rempli l'écran en blanc
lcd.show()  # Afficher!

while True:
	# Code inspired from twobitarcade.net
	#   https://www.twobitarcade.net/article/displaying-images-oled-displays/
	with open('ncd-mch.pbm', 'rb' ) as f:
		f.readline() # Magic number    P4 for pbm (Portable Bitmap)
		f.readline() # Creator comment
		f.readline() # Dimensions
		data = bytearray(f.read())

	fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
	lcd.invert(1)
	lcd.blit(fbuf, 0, 0)
	lcd.show()

	time.sleep(3)

	with open('upy-logo.pbm', 'rb' ) as f:
		f.readline() # Magic number    P4 for pbm (Portable Bitmap)
		f.readline() # Creator comment
		f.readline() # Dimensions
		data = bytearray(f.read())

	fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
	lcd.invert(1)
	lcd.blit(fbuf, 0, 0)
	lcd.show()

	time.sleep(3)
