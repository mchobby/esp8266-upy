__version__ = '0.0.2'

def map(value, istart, istop, ostart, ostop):
	# map value between [istart-istop] input interval to its [ostart-ostop] output interval
	# float compatible. Use int() to remove decimal part
	return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def ranking( value, ranges, transposed=None ):
	if transposed and ( len(ranges)!=len(transposed) ):
		raise ValueError( "ranges and transposed must have same length!")

	if value < ranges[0]:
		return None
	for index in range( len(ranges)-1 ):
		if ranges[index] <= value < ranges[index+1]:
			return ranges[index] if transposed==None else transposed[index]
	index = len(ranges)-1
	if value >= ranges[index]:
		return ranges[index] if transposed==None else transposed[index]
	raise ValueError( 'ranking() cannot resolve value %r!' % value )
	