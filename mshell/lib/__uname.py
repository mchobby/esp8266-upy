""" MiniShell uname command. Show system identification """

def uname( shell, args ):
	import os
	shell.println( 'sysname : %s' %os.uname().sysname )
	shell.println( 'nodename: %s' %os.uname().nodename )
	shell.println( 'release : %s' %os.uname().release )
	shell.println( 'version : %s' %os.uname().version )
	shell.println( 'machine : %s' %os.uname().machine )
	return 0
