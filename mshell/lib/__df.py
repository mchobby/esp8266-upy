""" MiniShell df command. Disk free / disk usage """

def df( shell, args ):
	if len(args)<=0:
		_p = "/"
	else:
		_p = args[0]
	import os
	_s = os.statvfs( _p )
	f_frsize = _s[1]
	f_blocks = _s[2]
	f_bfree  = _s[3]
	shell.println( 'FileSystem: %i bytes (%i KB, %i Blocks)' % (f_frsize*f_blocks,f_frsize*f_blocks//1024,f_blocks) )
	shell.println( 'Free      : %i bytes (%i KB, %i Blocks)' % (f_frsize*f_bfree,f_frsize*f_bfree//1024,f_bfree) )
	shell.println( 'Block size: %i bytes' % f_frsize )
	return 0
