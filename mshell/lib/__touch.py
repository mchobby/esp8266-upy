""" MiniShell touch command. create a file """

def touch( shell, args ):
	if len(args)<1:
		shell.println( "arg required!")
		return 1
	_file = open( args[0], "w" )
	_file.close()
	return 0
