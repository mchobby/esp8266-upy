import os

__version__ = "0.0.2"

COMMANDS = [ 'help', 'append', 'cat', 'cp', 'df', 'exit', 'ls', 'mv', 'rm', 'touch', 'uname' ]

class Exit( Exception ):
	pass

def exec_append( args ):
	if len(args)<2:
		print( "arg required!")
		return 1
	try:
		_file = open( args[0], "a+" )
	except:
		print( "Unable to open %s" % args[0] )
		return 1

	_file.write( args[1] ) # Append
	_file.write( '\n' )
	_file.close()
	return 0

def exec_cat( args ):
	if len(args)<1:
		print( "arg required!")
		return 1
	try:
		_file = open( args[0], "R" )
	except:
		print( "Unable to open %s" % args[0] )
		return 1
	_s = _file.readline()
	_count = 0
	while _s != None:
		print( _s.rstrip('\n') )
		_s = _file.readline()
		if len(_s)==0:
			_count += 1
		else:
			_count = 0
		if _count >= 3:
			break
	_file.close()
	return 0

def exec_cp( args ):
	if len(args)<2:
		print( "2 args required!")
		return 1

	try:
		_file = open( args[0], "r+b" )
	except:
		print( "Unable to open %s" % args[0] )
		return 1

	_file2 = open( args[1], "w+b" )
	_data = ' '
	_count = 0
	while len(_data) > 0:
		_data = _file.read( 50 )
		if len(_data)>0:
			_file2.write( _data )
		_count += len(_data)

	_file.close()
	_file2.close()
	print( '%i bytes copied!' % _count )
	return 0

def exec_df( args ):
	if len(args)<=0:
		_p = "/"
	else:
		_p = args[0]
	import os
	_s = os.statvfs( _p )
	f_frsize = _s[1]
	f_blocks = _s[2]
	f_bfree  = _s[3]
	print( _s[0] )
	print( 'FileSystem: %i bytes (%i KB, %i Blocks)' % (f_frsize*f_blocks,f_frsize*f_blocks//1024,f_blocks) )
	print( 'Free      : %i bytes (%i KB, %i Blocks)' % (f_frsize*f_bfree,f_frsize*f_bfree//1024,f_bfree) )
	print( 'Block size: %i bytes' % f_frsize )

	return 0

def exec_ls( args ): # don't care args
	for i in os.listdir():
		print( i )
	return 0

def exec_mv( args ):
	if len(args)<2:
		print( "args required!")
		return 1
	try:
		os.rename( args[0], args[1] )
	except:
		print( 'fail to move %s to %s' % (args[0], args[1]) )
		return 1
	return 0

def exec_rm( args ): # don't care args
	if len(args)<1:
		print( "arg required!")
		return 1
	try:
		os.remove( args[0] )
		print( '%s deleted!' % args[0])
	except:
		print( 'fail to remove %s' % args[0] )
		return 1
	return 0

def exec_touch( args ): # don't care args
	if len(args)<1:
		print( "arg required!")
		return 1
	_file = open( args[0], "w" )
	_file.close()
	return 0

def exec_uname( args ): # don't care the args
	import os
	print( 'sysname : %s' %os.uname().sysname )
	print( 'nodename: %s' %os.uname().nodename )
	print( 'release : %s' %os.uname().release )
	print( 'version : %s' %os.uname().version )
	print( 'machine : %s' %os.uname().machine )
	return 0

def exec_exit( args ):
	raise Exit()

def exec_help( args ):
	return exec_cat( ['mshell.txt'] )

# ---- Main code ----

def read_eval():
	cmd = input( '$ ' )
	l = cmd.split() # should be improved to mange string containsing spaces
	if (l == None) or (len(l)==0):
		return 0 # ignore this
	_cmd = l[0]
	_args = []
	for item in l[1:] :
		_args.append( item.strip('"') )

	if _cmd in COMMANDS:
		fct = eval( 'exec_%s' % _cmd ) # ref to the function
		return fct( _args )
	else:
		print( 'undefined command %s!' % _cmd )
		return 0 # not an ERROR

def run():
	print( "=== Welcome to mini shell %s ===" % __version__ )
	print( "Supports:", ", ".join(COMMANDS) )
	print( "Use mshell.run() to restart!")
	print( " " )
	while True:
		try:
			_err = read_eval()
			if _err != 0:
				print( 'ERROR %i' % _err )
		except Exit:
			print('Exiting Mini Shell')
			break

run()
