__version__ = '0.0.1'

def map(value, istart, istop, ostart, ostop):
	# map value between [istart-istop] input interval to its [ostart-ostop] output interval
	# float compatible. Use int() to remove decimal part
	return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
