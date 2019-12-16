"""
keypad.py - read entry from 4x4 matrix keypad.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/esp8266-upy/tree/master/keypad-4x4

"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
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

__version__ = "0.0.1"

from machine import Pin
import time

class Keypad(object):
	""" Class used to read Keypad Matrix """

	def __init__(self, lines, cols, debounce_ms=300 ):
		""" lines : array of lines pins configured as OUPUT (from 1 to N)
			cols  : array of columns pins configured as INPUT (from 1 to N) """
		self.lines = [ Pin(pin_name, Pin.OUT, value=True) for pin_name in lines ]
		self.line_count = len( lines )
		self.cols  = [ Pin(pin_name, Pin.IN, Pin.PULL_UP) for pin_name in cols ]
		self.col_count = len( cols )

		# read debouncing
		self.debounce_ms  = debounce_ms
		self.last_release = time.ticks_ms() # last release time
		self.last_index   = -1              # last pressed key

	def scan( self ):
		""" Scan all lines and read entries that are low. Returns a list of key-index """
		r = []
		for i in range(self.line_count):
			self.lines[i].value( 0 )
			for j in range(self.col_count):
				if self.cols[j].value()<=0:
					r.append( i*self.col_count + j )
			self.lines[i].value( 1 )
		return r

	def read( self, timeout=None ):
		""" Wait for a key to be pressed + release and returns its index. May returns None in case of time-out (in seconds)"""
		ctime = time.time() # timeout in second
		pressed = []
		while( (timeout==None) or ((time.time()-ctime)<timeout) ):
			scan = self.scan()
			# Do not add duplicates
			pressed.extend( [x for x in scan if x not in pressed] )
			# attempt to detect released key
			release = [ x for x in pressed if x not in scan ]
			#print( scan, pressed, release )
			if len(release)>0:
				# first released key is release[0]
				# Check for multiple activation of the same key
				if ((time.ticks_ms()-self.last_release)<self.debounce_ms) and (self.last_index==release[0]):
					continue
				else:
					self.last_release = time.ticks_ms() # Now
					self.last_index   = release[0]
					return self.last_index
		# In case of time-out
		return None


class Keypad4x4( Keypad ):
	""" Class used for the 4x4 Menbrane Keypad available at

		https://shop.mchobby.be/fr/tactile-flex-pot-softpad/83-clavier-16-touches-souple-3232100000834.html """

	def __init__( self, lines=["X5","X6","X7","X8"], cols=["Y9","Y10","Y11","Y12"], map="123A456B789C*0#D" ):
		self.map = map
		super().__init__( lines, cols )

	def read_key( self, timeout=None ):
		""" Wait for a key to be pressed + release and returns its label/name. May returns None in case of time-out """
		idx = self.read( timeout=timeout )
		if idx!=None:
			return( self.map[idx] )
		else:
			return None
