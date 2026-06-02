from math import sqrt 

__version__ = '0.2.0'

class Statistic():
	""" Calculation of min, max, mean, variance, std_dev, unbiased std_dev of 
	    values append() into the dataset. The class doesn't keeps history of values! 

	    rely on Kahan summation @ https://en.wikipedia.org/wiki/Kahan_summation_algorithm
	"""
	def __init__( self ):
		self.clear()

	def clear( self ):
		self._count = 0
		self._sum_high = 0.0
		self._sum_low = 0.0
		self._min = 0.0
		self._max = 0.0
		# sum of squares
    		self._ssq_high = 0.0
		self._ssq_low  = 0.0

	def append( self, value ):
		""" Append a new value in the dataset """
		if self._count == 0:
			self._min = value
			self._max = value
		else:
			if value < self._min:
				self._min = value
			elif value > self._max:
				self. _max = value
		
		# Kahan summation @ https://en.wikipedia.org/wiki/Kahan_summation_algorithm
		_store = self._sum_high 
		self._sum_high += value
		self._sum_low  += value - (self._sum_high - _store)
		self._count += 1

		if self._count > 1:
			value *= value # square the value
			_store = self._ssq_high
			self._ssq_high += value
			self._ssq_low += value - (self._ssq_high - _store)

	@property
	def sum( self ):
		return self._sum_high + self._sum_low

	@property
	def min( self ):
		return self._min

	@property
	def max( self ):
		return self._max

	@property
	def mean( self ):
		""" Average of pushed values """
		if self._count == 0:
			return None
		return (self._sum_high + self._sum_low) / self._count

	@property
	def count( self ):
		return self._count

	@property
	def variance( self ):
		if self._count == 0:
			return None
		_store = self._sum_high + self._sum_low
		_store *= _store
		_store = (self._ssq_high + self._ssq_low) - (_store / self._count)
		return _store / self._count

	@property
	def std_dev( self ):
		""" Population standard deviation (biased standard deviation)"""
		#  s = sqrt [ S ( Xi - µ )2 / N ]
		if self._count == 0:
			 return None
		_store = self._sum_high + self._sum_low
		_store *= _store
		_store = (self._ssq_high + self._ssq_low) - (_store / self._count)
		return sqrt( _store / self._count)

	@property
	def unbiased_std_dev( self ):
		""" Unbiased use n-1 on denominator to avoids underestimation the population variation """
		if self._count < 2:
			return None
		_store = self._sum_high + self._sum_low
		_store *= _store
		_store = (self._ssq_high + self._ssq_low) - (_store / self._count)
		return sqrt( _store / (self._count - 1))


class BufferedStatistic( Statistic ):
	""" Also keeps a copy of the appended value into the buffer list """
	def __init__( self ):
		self.buffer = []
		super().__init__()

	def clear( self ):
		self.buffer.clear()
		super().clear()

	def append( self, value ):
		self.buffer.append( value )
		super().append( value )
		
class Damper():
    """ Damper will calculate the mean of the N last values pushed
        in the Damper """
    def __init__( self, length ):
        self.lst = list( [None]*length )
        self.imaxpos = length-1 # Max cursor position
        self.ipos = -1   # Current cursor position
        self.ilength = 0 # Current length of dataset (0 to length)
        
    def clear( self ):
        self.lst  = list( [None]*(self.imaxpos+1) )
        self.ipos = -1
        self.ilength = 0
        
    def append( self, value ):
        self.ipos += 1 # Next storage position
        if self.ilength < self.imaxpos+1: # Current length of dataset
            self.ilength += 1
        if self.ipos > self.imaxpos:
            self.ipos = 0
        self.lst[ self.ipos ] = value
        
    @property
    def count( self ):
        return self.ilength
        
    @property
    def mean( self ):
        s = sum( [v for v in self.lst if v!=None] )
        return s/self.ilength


