# Make a rainbow color cycle on the trackball
#
#  See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/trackball

from machine import I2C
from trackball import Trackball
import time

i2c = I2C(2) # Y9=scl, Y10=sda or Pyboard-Uno-R3 (I2C over pin 13)
trackball = Trackball(i2c)

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


while True:
    h = int(time.time()*3 ) % 360 / 360.0

    # Calculate RGB vals
    r, g, b = [int(c * 255) for c in hsv_to_rgb(h, 1.0, 1.0)]
    w = 0

    # Set LEDs
    trackball.set_rgbw(r, g, b, w)
