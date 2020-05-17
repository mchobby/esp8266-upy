# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
is31fl3731.py : MicroPython driver for the IS31FL3731 charlieplex IC.


* Author(s):
   16 apr 2020: Meurisse D. (shop.mchobby.be) - backport to MicroPython
   08 apr 2020: Tony DiCola, Melissa LeBlanc-Williams : original CircuitPython library posted on
                 https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731/blob/master/adafruit_is31fl3731.py

"""

# imports
import math
import time
from micropython import const

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/is31fl"

_MODE_REGISTER = const(0x00)
_FRAME_REGISTER = const(0x01)
_AUTOPLAY1_REGISTER = const(0x02)
_AUTOPLAY2_REGISTER = const(0x03)
_BLINK_REGISTER = const(0x05)
_AUDIOSYNC_REGISTER = const(0x06)
_BREATH1_REGISTER = const(0x08)
_BREATH2_REGISTER = const(0x09)
_SHUTDOWN_REGISTER = const(0x0A)
_GAIN_REGISTER = const(0x0B)
_ADC_REGISTER = const(0x0C)

_CONFIG_BANK = const(0x0B)
_BANK_ADDRESS = const(0xFD)

_PICTURE_MODE = const(0x00)
_AUTOPLAY_MODE = const(0x08)
_AUDIOPLAY_MODE = const(0x18)

_ENABLE_OFFSET = const(0x00)
_BLINK_OFFSET = const(0x12)
_COLOR_OFFSET = const(0x24)


class Matrix:
	""" The Matrix class support the main function for driving the 16x9 matrix Display

		:param i2c: the connected i2c bus machine.I2C
		:param address: the device address; defaults to 0x74 """

	width = 16
	height = 9

	def __init__(self, i2c, address=0x74):
		self.i2c = i2c
		self.address = address
		self._frame = None
		self.reset()
		self._init()

	def _i2c_read_reg(self, reg, result):
		# Read a buffer of data from the specified 8-bit I2C register address.
		# The provided result parameter will be filled to capacity with bytes of data read from the register.
		#self.i2c.writeto_then_readfrom(self.address, bytes([reg]), result)
		data = bytes([ reg ])
		self.i2c.writeto( self.address, data )
		data = bytearray( 1 )
		self.i2c.readfrom_into( self.address, result ) # read one byte
		return result #self._BUFFER[0]


	def _i2c_write_reg(self, reg, data):
		# Write a buffer of data (byte array) to the specified I2C register address.
		buf = bytearray(1)
		buf[0] = reg
		buf.extend(data)
		self.i2c.writeto(self.address, buf)


	def _bank(self, bank=None):
		""" Select the bank (or return the current bank) """
		if bank is None:
			result = bytearray(1)
			return self._i2c_read_reg(_BANK_ADDRESS, result)[0]
		self._i2c_write_reg(_BANK_ADDRESS, bytearray([bank]))
		return None

	def _register(self, bank, register, value=None):
		""" Write a value into a register (after bank selection). If value is omited then the function read it and return it """
		self._bank(bank)
		if value is None:
			result = bytearray(1)
			return self._i2c_read_reg(register, result)[0]
		self._i2c_write_reg(register, bytearray([value]))
		return None

	def _mode(self, mode=None):
		""" Display mode: Picture, animation, audio mode. See Datasheet """
		return self._register(_CONFIG_BANK, _MODE_REGISTER, mode)

	def _init(self):
		""" Clear all the frame """
		self._mode(_PICTURE_MODE)
		self.frame(0)
		for frame in range(8):
			self.fill(0, False, frame=frame)
			for col in range(18):
				self._register(frame, _ENABLE_OFFSET + col, 0xFF)
		self.audio_sync(False)

	def reset(self):
		"""Kill the display for 10MS"""
		self.sleep(True)
		time.sleep(0.01)  # 10 MS pause to reset.
		self.sleep(False)

	def sleep(self, value):
		""" Set the Software Shutdown Register bit
			:param value: True to set software shutdown bit; False unset """
		return self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, not value)

	def autoplay(self, delay=0, loops=0, frames=0):
		""" Start autoplay
			:param delay: in ms
			:param loops: number of loops - 0->7
			:param frames: number of frames: 0->7 """
		if delay == 0:
			self._mode(_PICTURE_MODE)
			return
		delay //= 11
		if not 0 <= loops <= 7:
			raise ValueError("Loops out of range")
		if not 0 <= frames <= 7:
			raise ValueError("Frames out of range")
		if not 1 <= delay <= 64:
			raise ValueError("Delay out of range")
		self._register(_CONFIG_BANK, _AUTOPLAY1_REGISTER, loops << 4 | frames)
		self._register(_CONFIG_BANK, _AUTOPLAY2_REGISTER, delay % 64)
		self._mode(_AUTOPLAY_MODE | self._frame)

	def fade(self, fade_in=None, fade_out=None, pause=0):
		""" Start and stop the fade feature.  If both fade_in and fade_out are None (the
			default), the breath feature is used for fading.  if fade_in is None, then
			fade_in = fade_out.  If fade_out is None, then fade_out = fade_in
			:param fade_in: positive number; 0->100
			:param fade-out: positive number; 0->100
			:param pause: breath register 2 pause value """
		if fade_in is None and fade_out is None:
			self._register(_CONFIG_BANK, _BREATH2_REGISTER, 0)
		elif fade_in is None:
			fade_in = fade_out
		elif fade_out is None:
			fade_out = fade_in
		fade_in = int(math.log(fade_in / 26, 2))
		fade_out = int(math.log(fade_out / 26, 2))
		pause = int(math.log(pause / 26, 2))
		if not 0 <= fade_in <= 7:
			raise ValueError("Fade in out of range")
		if not 0 <= fade_out <= 7:
			raise ValueError("Fade out out of range")
		if not 0 <= pause <= 7:
			raise ValueError("Pause out of range")
		self._register(_CONFIG_BANK, _BREATH1_REGISTER, fade_out << 4 | fade_in)
		self._register(_CONFIG_BANK, _BREATH2_REGISTER, 1 << 4 | pause)

	def frame(self, frame=None, show=True):
		""" Set the current frame
			:param frame: frame number; 0-7 or None. If None function returns current frame
			:param show: True to show the frame; False to not show. """
		if frame is None:
			return self._frame
		if not 0 <= frame <= 8:
			raise ValueError("Frame out of range")
		self._frame = frame
		if show:
			self._register(_CONFIG_BANK, _FRAME_REGISTER, frame)
		return None

	def audio_sync(self, value=None):
		"""Set the audio sync feature register """
		return self._register(_CONFIG_BANK, _AUDIOSYNC_REGISTER, value)

	def audio_play(self, sample_rate, audio_gain=0, agc_enable=False, agc_fast=False):
		""" Controls the audio play feature """
		if sample_rate == 0:
			self._mode(_PICTURE_MODE)
			return
		sample_rate //= 46
		if not 1 <= sample_rate <= 256:
			raise ValueError("Sample rate out of range")
		self._register(_CONFIG_BANK, _ADC_REGISTER, sample_rate % 256)
		audio_gain //= 3
		if not 0 <= audio_gain <= 7:
			raise ValueError("Audio gain out of range")
		self._register( _CONFIG_BANK, _GAIN_REGISTER,
						bool(agc_enable) << 3 | bool(agc_fast) << 4 | audio_gain, )
		self._mode(_AUDIOPLAY_MODE)

	def blink(self, rate=None):
		""" Updates the blink register """
		if rate is None:
			return (self._register(_CONFIG_BANK, _BLINK_REGISTER) & 0x07) * 270
		elif rate == 0:
			self._register(_CONFIG_BANK, _BLINK_REGISTER, 0x00)
			return None
		rate //= 270
		self._register(_CONFIG_BANK, _BLINK_REGISTER, rate & 0x07 | 0x08)
		return None

	def fill(self, color=None, blink=None, frame=None):
		""" Fill the display with a brightness level
			:param color: brightness 0->255
			:param blink: True if blinking is required
			:param frame: which frame to fill 0->7 (or current frame) """
		if frame is None:
			frame = self._frame
		self._bank(frame)
		if color is not None:
			if not 0 <= color <= 255:
				raise ValueError("Color out of range")
			data = bytearray([color] * 25)  # Extra byte at front for address.
			for row in range(6):
				data[0] = _COLOR_OFFSET + row * 24
				self.i2c.writeto(self.address, data)
		if blink is not None:
			data = bool(blink) * 0xFF
			for col in range(18):
				self._register(frame, _BLINK_OFFSET + col, data)

	@staticmethod
	def pixel_addr(x, y):
		""" Calulate the offset into the device array for x,y pixel """
		return x + y * 16

	def pixel(self, x, y, color=None, blink=None, frame=None):
		""" Blink or brightness for x-, y-pixel
			:param x: horizontal pixel position
			:param y: vertical pixel position
			:param color: brightness value 0->255
			:param blink: True to blink
			:param frame: the frame to set the pixel """
		if not 0 <= x <= self.width:
			return None
		if not 0 <= y <= self.height:
			return None
		pixel = self.pixel_addr(x, y)
		if color is None and blink is None:
			return self._register(self._frame, pixel)
		if frame is None:
			frame = self._frame
		if color is not None:
			assert 0 <= color <= 255, "Color out of range"
			self._register(frame, _COLOR_OFFSET + pixel, color)
		if blink is not None:
			addr, bit = divmod(pixel, 8)
			bits = self._register(frame, _BLINK_OFFSET + addr)
			if blink:
				bits |= 1 << bit
			else:
				bits &= ~(1 << bit)
			self._register(frame, _BLINK_OFFSET + addr, bits)
		return None


	def image(self, img, blink=None, frame=None):
		""" Set buffer to value of Python Imaging Library image.  The image should
			be in 8-bit mode (L) and a size equal to the display size.

			:param img: Python Imaging Library image
			:param blink: True to blink
			:param frame: the frame to set the image """
		if img.mode != "L":
			raise ValueError("Image must be in mode L.")
		imwidth, imheight = img.size
		if imwidth != self.width or imheight != self.height:
			raise ValueError( "Image must be same dimensions as display ({0}x{1}).".format( self.width, self.height ) )
		# Grab all the pixels from the image, faster than getpixel.
		pixels = img.load()

		# Iterate through the pixels
		for x in range(self.width):  # yes this double loop is slow,
			for y in range(self.height):  #  but these displays are small!
				self.pixel(x, y, pixels[(x, y)], blink=blink, frame=frame)


class CharlieWing(Matrix):
	""" Supports the Charlieplexed feather wing """
	width = 15
	height = 7

	@staticmethod
	def pixel_addr(x, y):
		""" Calulate the offset into the device array for x,y pixel """
		if x > 7:
			x = 15 - x
			y += 8
		else:
			y = 7 - y
		return x * 16 + y

class CharlieBonnet(Matrix):
	""" Supports the Charlieplexed bonnet """

	width = 16
	height = 8

	@staticmethod
	def pixel_addr(x, y):
		"""Calulate the offset into the device array for x,y pixel"""
		if x >= 8:
			return (x - 6) * 16 - (y + 1)
		return (x + 1) * 16 + (7 - y)
