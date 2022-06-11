""" MiniShell ptest command. Minimal structure for a minishell plug-in """

def ptest( shell, args ):
	shell.println( '--- ptest MiniShell Plug-in demo ---')
	shell.println( 'args count: %s' % len(args) )
	for i in range( len(args) ):
		shell.println( 'args[%i] = %s' % (i, args[i]) )

	# All input should be made via the shell
	val = shell.readline( 'Your name: ')
	shell.println( 'You entered: %s' % val)

	# Must return a numeric value 0 = OK, >0 = Error
	return 0
