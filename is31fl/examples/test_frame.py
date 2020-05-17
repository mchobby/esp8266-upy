# Draw a heart on the 8th frames. At a different position on each frame.
# Frame 0 is the less bright while the frame 7 is the most bright.
# Then display each frame, one at the time, to create a small animation
#
from machine import I2C
import is31fl3731 as is31f
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

heart = bytearray( ( 0b01100110,
					 0b10011001,
					 0b10001001,
					 0b01000010,
					 0b00100100,
					 0b00010100,
					 0b00001000,
					 0b00010000 ) )

# first load the frame; moves the to the right at each frame
display.sleep(True)  # turn display off while frames are updated
for frame in range(8):
	# Select a Frame
	display.frame(frame, show=False)
	display.fill(0)
	# Fill in the select Frame
	for y in range(display.height):
		row = heart[y]
		for x in range(8):
			bit = 1 << (7 - x) & row
			# display the pixel into selected frame with varying intensity
			if bit:
				display.pixel(x + frame, y, frame ** 2 + 1) # x,y, color=brightness(0..255)

# Exit sleep mode
display.sleep(False)

# now tell the display to show the frame one at time
while True:
	for frame in range(8):
		display.frame(frame, show=True)
		time.sleep(0.1)
