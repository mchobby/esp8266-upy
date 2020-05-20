# Change the color of the trackball LED depending on the trackball movement
#  - Move up/down, right/left to modify color and saturation
#  - Press the button to light on/off
#
#  See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/trackball

from machine import I2C
from trackball import Trackball
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)
trackball = Trackball(i2c)

x = 0
y = 50.0

toggled = False

def hsv_to_rgb(h, s, v):
	if s == 0.0:
		return v, v, v
	i = int(h*6.0) # XXX assume int() truncates!
	f = (h*6.0) - i
	p = v*(1.0 - s)
	q = v*(1.0 - s*f)
	t = v*(1.0 - s*(1.0-f))
	i = i%6
	if i == 0:
		return v, t, p
	if i == 1:
		return q, v, p
	if i == 2:
		return p, v, t
	if i == 3:
		return p, q, v
	if i == 4:
		return t, p, v
	if i == 5:
		return v, p, q
	# Cannot get here

try:
	while True:
		up, down, left, right, switch, state = trackball.read()

		# Update x and y vals based on movement
		y += up
		y -= down
		x += right / 10.0
		x -= left / 10.0

		# Clamp to min of 0 and max of 100
		x %= 100
		y = max(0, min(y, 100))

		# Calculate hue and brightness
		h = x / 100.0
		v = y / 100.0

		# Prevents button from retriggering
		debounce = 0.5

		# Change toggled state if switch is pressed
		if state and not toggled:
			toggled = True
			time.sleep(debounce)
		elif state and toggled:
			toggled = False
			time.sleep(debounce)

		# Set brightness to zero if switch toggled
		if toggled:
			v = 0

		# Calculate RGB vals
		w = 0
		r, g, b = [int(c * 255) for c in hsv_to_rgb(h, 1.0, v)]

		# Set LEDs
		trackball.set_rgbw(r, g, b, w)

		time.sleep(0.01)
finally:
	# Ligth off the trackball
	trackball.set_rgbw(0, 0, 0, 0)
