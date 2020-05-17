# Draw a box on the edge of the display.
#
from machine import I2C
import is31fl3731 as is31f

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)

# initialize display using Feather CharlieWing LED 15 x 7
display = is31f.CharlieWing(i2c)

# class Matrix: Adafruit 16x9 Charlieplexed
# class CharlieBonnet : Adafruit 16x8 Charlieplexed Bonnet

# draw a box on the display
# first draw the top and bottom edges
for x in range(display.width):
    display.pixel(x, 0, 50)
    display.pixel(x, display.height - 1, 50)
# now draw the left and right edges
for y in range(display.height):
    display.pixel(0, y, 50)
    display.pixel(display.width - 1, y, 50)
