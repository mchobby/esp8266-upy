# Show a scrolling text on the display.
# The text is a bit bigger than ChaliePlexing FeatgerWing (15x7 leds)
#
from machine import I2C
import framebuf
import is31fl3731 as is31f
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

text_to_show = "MicroPython"

# Create a framebuffer for our display
buf = bytearray(32)  # 1 bytes height x 16 wide = 32 bytes (9 bits is 2 bytes)
fb = framebuf.FrameBuffer( buf, display.width, display.height,
			framebuf.MVLSB ) # Monochrome 1 bit color, bit arranged vertically, first bit near of top


frame = 0  # start with frame 0
while True:
	for i in range(len(text_to_show) * 9):
		fb.fill(0)
		fb.text(text_to_show, -i + display.width, 1)

		# to improve the display flicker we can use two frame
		# fill the next frame with scrolling text, then
		# show it.
		display.frame(frame, show=False)
		# turn all LEDs off
		display.fill(0)
		for x in range(display.width):
			# using the FrameBuffer text result
			bite = buf[x]
			for y in range(display.height):
				bit = 1 << y & bite
				# if bit > 0 then set the pixel brightness
				if bit:
					display.pixel(x, y, 50)

		# now that the frame is filled, show it.
		display.frame(frame, show=True)
		frame = 0 if frame else 1
		time.sleep( 0.050 ) # 50 ms
