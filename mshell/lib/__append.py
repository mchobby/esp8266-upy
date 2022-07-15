""" MiniShell append command. Add text to the end of a file """

def append( shell, args ):
	if len(args)<2:
		shell.println( "arg required!")
		return 1
	try:
		_file = open( args[0], "a+" )
	except:
		shell.println( "Unable to open %s" % args[0] )
		return 1

	_file.write( args[1] ) # Append
	_file.write( '\n' )
	_file.close()
	return 0
