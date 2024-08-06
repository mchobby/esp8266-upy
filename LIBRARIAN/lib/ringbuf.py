# Implementation of Ring Buffer
#
# Author: DMeurisse
#
# See project source at: https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN
#
# Based on "Data Structure and Algorithms" description document
#   https://sites.google.com/view/algobytheroyakash/about-ds-algorithms?authuser=0
#   https://sites.google.com/view/algobytheroyakash/data-structures/ring-buffer

from micropython import const

__version__ = '0.0.1'

class RingBuffer:
	# The parameter to the constructor is the size of the buffer.
	# put() puts a byte into the buffer, not overwriting previous content.
	# get() returns the first value.
	# @free remaining bytes in the RingBuffer
	# None is returned if either not data can be put or no data is to be retrieved.
	def __init__(self, size):
		self.data = bytearray(size)
		self.size = size
		self.index_put = 0
		self.index_get = 0

	@property
	def available_for_reading( self ):
		return self.index_put - self.index_get

	@property
	def free( self ):
		return self.size - self.available_for_reading

	@property
	def is_full( self ):
		return self.free == 0

	@property
	def is_empty( self ):
		return self.available_for_reading == 0

	def put(self, value):
		if not(self.is_full):
			# DEBUG: print( "data[%s] = %s" % (self.index_put % self.size, value) )
			self.data[self.index_put % self.size] = value
			self.index_put += 1
			return value
		else:
			return None

	def get(self):
		if not(self.is_empty):
			_r = self.data[self.index_get % self.size]
			# DEBUG: print("_r = self.data[%i] = %i" % (self.index_put % self.size, _r) )
			self.index_get += 1
			return _r
		else:
			return None  ## buffer empty

	def put_from( self, buf ):
		# return #bytes added to the ring
		if len(buf)>self.free:
			return 0 # we can't add
		else:
			for b in buf:
				self.put( b )
				# print( 'index_get',self.index_get )
				# print( 'index_put',self.index_put )
			return len(buf)

	def get_bytes( self, size ):
		# return a bytes containing the size next bytes from the ring
		if size > self.available_for_reading:
			return None
		else:
			_b = bytearray(size)
			for i in range( size ):
				v = self.get()
				# debug: print( v )
				_b[i] = v
			return _b
