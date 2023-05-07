def draw_icon( fb, icon, x, y, color ):
	""" Display one of the icon in the fb FrameBuffer @ x,y position with the C color.
		Icons are stored into the icons.py file. Only draws pixels (don't clear pixels) """
	size = icon[0]
	for row in range( size ):
		for col in range( size ):
			if (icon[row+1] & (1<<(7-col))) > 0:
				fb.pixel(col+x,row+y,color)

def icon_as_list( icon ):
	""" Extract the icon data as a list of [True,False,True] values. """
	_r = list()
	size = icon[0]
	for row in range( size ):
		_line = list()
		for col in range( size ):
			_line.append( (icon[row+1] & (1<<(7-col))) > 0 )
		_r.append( _line )
	return _r

def icon_as_text( icon ):
	""" Return a list of string containing the representation of the icon """
	_r = list()
	size = icon[0]
	for row in range( size ):
		_s = ''
		for col in range( size ):
			_s += '*' if (icon[row+1] & (1<<(7-col))) > 0 else ' '
		_r.append( _s )
	return _r
