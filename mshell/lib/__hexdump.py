""" MiniShell HexDump command """
def hexdump( shell, args ):
	if len( args )<1 :
		shell.println( 'Missing filename' )
		return 1
	fname = args[0]

	if shell.file_size( fname )<0:
		shell.println( 'file does not exists!')
		return -1

	shell.paging = True
	shell.println("hexdump for %s" % fname )
	shell.println("")
	shell.println("%6s | %-48s | %s" % ("Offset", "Data(h)", "String") )
	shell.println("-"*80)
	iOffset = 0
	try:
		with open( fname, "rb" ) as f:
			while True:
				sData = ''
				sText = ''
				buf = f.read( 16 )
				if len( buf )== 0:
					break
				sData = " ".join( ["%02X" % int(b) for b in buf] )
				sText = "".join( [chr(b) if 32<=b<127 else '.' for b in buf] )
				shell.println( "%06X | %-48s | %s" % (iOffset, sData, sText) )
				iOffset += 16
	finally:
		shell.paging = False
	return 0
