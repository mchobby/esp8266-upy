# Show a wave effect on the display.
#
#
from machine import I2C
import framebuf
import is31fl3731 as is31f
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

sweep = [ 1, 2, 3, 4, 6, 8,10,15,20,30,40,60,
		 60,40,30,20,15,10 ,8, 6, 4, 3, 2, 1 ]

frame = 0
while True:
	for incr in range(24):
		# to reduce update flicker, use two frames make a frame active, don't show it yet
		display.frame(frame, show=False)
		# fill the display with the next frame
		for x in range(display.width):
			for y in range(display.height):
				display.pixel(x, y, sweep[(x + y + incr) % 24])
		# show next frame
		display.frame(frame, show=True)
		# Swith between frame 0 et frame 1
		frame = 0 if frame==1 else 1
		time.sleep( 0.05 )
