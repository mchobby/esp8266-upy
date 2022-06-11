""" MiniShell HexDump command """
def hexdump( shell, args ):
	if len( args )<1 :
		shell.println( 'Missing filename' )
		return 1
	fname = args[0]

	shell.println("  hexdump for %s" % fname )
	shell.println( args )

	return 0
