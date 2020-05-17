# Show a scrolling text on the display.
# The text is a bit bigger than ChaliePlexing FeatgerWing (15x7 leds).
#
# Should use a bigger charlieplex grid
#
from machine import I2C
import framebuf
import is31fl3731 as is31f
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

# Create a framebuffer for our display
#   Buffer Size for CharliePlex 15x7 (ADA3134) - 1bit_color * 15 columns of 7 pixels = 1bit_color * 15 * 8 bits_per_column = 15 Bytes storage
#   Buffer Size for CharliePlex 16x9 (ADA2974) - 1bit_color * 16 columns of 9 pixels = 1bit_color * 16 * 16 bits_per_column = 32 Bytes storage
# Data is stored in multiple of 8 bits. So to store 9 pixel height, 9 bits, we will need 16 bits of storage.
buf = bytearray(15)
fb = framebuf.FrameBuffer( buf, display.width, display.height,
			framebuf.MVLSB ) # Monochrome 1 bit color, bit arranged vertically, first bit near of top
fb.fill(0)
fb.text( "123", 0, 1) # X,Y, Color

display.frame( 0 , show=False)
display.fill(0)

# Transfert FrameBuffer to display
for x in range(display.width):
	# using the FrameBuffer text result
	bite = buf[x]
	for y in range(display.height):
		bit = 1 << y & bite
		# if bit > 0 then set the pixel brightness
		if bit:
			display.pixel(x, y, 50) # x,y,color=brightness(0..255)

# now that the frame is filled, show it.
display.frame(0, show=True)
