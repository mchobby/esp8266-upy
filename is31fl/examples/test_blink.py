# Make a blinking arrow
#
from machine import I2C
import is31fl3731 as is31f

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

# class Matrix: Adafruit 16x9 Charlieplexed
# class CharlieBonnet : Adafruit 16x8 Charlieplexed Bonnet

# array pattern in bits; top row-> bottom row, 8 bits in each row
# value 0x08, 0x0C, 0xFE, 0xFF, 0xFE, 0x0C, 0x08, 0x00, 0x00
an_arrow = bytearray( ( 0b00001000,
						0b00001100,
						0b11111110,
						0b11111111,
						0b11111110,
						0b00001100,
						0b00001000,
						0b00000000,
						0b00000000 ) )

# first load the frame with the arrows
#
display.sleep(True)  # turn display off while updating blink bits
display.fill(0)
for y in range(display.height): # For each line
	row = an_arrow[y]
	for x in range(8): # for each bit (each pixel) in the line
		bit = 1 << (7 - x) & row
		if bit:
			display.pixel(x + 4, y, 50, blink=True) # Draw from the 5th column

display.blink(1000)  # ranges from 270 to 2159; smaller the number to faster blink
display.sleep(False)  # turn display on
