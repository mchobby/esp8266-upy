import os
import gc
import sys

__version__ = "0.0.5"

COMMANDS = [ 'help', 'cat', 'cp', 'exit', 'edit', 'free', 'ls', 'more', 'mv', 'rm', 'run' ]

class EAbort( Exception ):
	pass
class Exit( EAbort ):
	pass

# ---- Shell Commands ----
def run_more( shell, args ):
	return run_cat( shell, args, paging=True )

def run_cat( shell, args, paging=False ):
	if len(args)<1:
		shell.println( "arg required!")
		return 1
	try:
		_file = open( args[0], "R" )
	except:
		shell.println( "Unable to open %s" % args[0] )
		return 1
	shell.paging = paging
	try:
		_s = _file.readline()
		_count = 0
		while _s != None:
			shell.println( _s.rstrip('\n') )
			_s = _file.readline()
			if len(_s)==0:
				_count += 1
			else:
				_count = 0
			if _count >= 3:
				break
	finally:
		_file.close()
		shell.paging = False
	return 0

def run_cp( shell, args ):
	if len(args)<2:
		shell.println( "2 args required!")
		return 1

	try:
		_file = open( args[0], "r+b" )
	except:
		shell.println( "Unable to open %s" % args[0] )
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
	shell.println( '%i bytes copied!' % _count )
	return 0

def run_edit( shell, args ):
	if len(args)<1:
		shell.println( "filename required!")
		return 1
	import pye # requires  https://github.com/robert-hh/Micropython-Editor/blob/master/pye.py
	with open( args[0] ) as f:
		content = f.read().splitlines()
	pye.pye( content )

def run_free( shell, args ):
	gc.collect()
	shell.println( "Free Mem: %i bytes" % gc.mem_free() )
	return 0


def run_ls( shell, args ): # don't care args
	shell.paging = True
	try:
		for name in os.listdir( '/' if len(args)==0 else args[0] ):
			shell.println( ' %s' % name )
	finally:
		shell.paging = False
	return 0

def run_mv( shell, args ):
	if len(args)<2:
		shell.println( "args required!")
		return 1
	try:
		os.rename( args[0], args[1] )
	except:
		shell.println( 'fail to move %s to %s' % (args[0], args[1]) )
		return 1
	return 0

def run_rm( shell, args ): # don't care args
	if len(args)<1:
		shell.println( "arg required!")
		return 1
	try:
		os.remove( args[0] )
		shell.println( '%s deleted!' % args[0])
	except:
		shell.println( 'fail to remove %s' % args[0] )
		return 1
	return 0

def run_run( shell, args ):
	if len(args)<1:
		shell.println( "arg required!")
		return 1
	mod_name = args[0].split("/")[-1].replace('.py','')
	if mod_name in sys.modules:
		del sys.modules[mod_name]
		gc.collect()
	try:
		__import__( mod_name )
	except Exception as err:
		shell.println( 'Failed to run %s' % args[0] )
		shell.println( err )
	return 0

def run_exit( shell, args ):
	raise Exit()

def run_help( shell, args ):
	if shell.file_size( '/lib/mshell.txt' )>0:
		return run_more( shell, ['/lib/mshell.txt'] )
	else:
		return run_more( shell, ['mshell.txt'] )

# ----MiniShell Core ----
class MiniShell:
	def __init__(self):
		self.cols = 80
		self.rows = 24
		self._paging = False
		self._ipaged = 0 # nbr of lines in the current page

	@property
	def paging( self ):
		return self._pagning

	@paging.setter
	def paging( self, activate ):
		if activate:
			self._ipaged = 0 # nbr lines paged
		self._paging = activate

	def println( self, s ):
		print( s )
		if self._paging:
			self._ipaged += 1
			if self._ipaged >= self.rows-2:
				self._ipaged = 0
				print( 'Press Key to continue, q to quit...' )
				key=sys.stdin.read(1)
				if key in ('Q', 'q' ):
					raise EAbort()

	def readline( self, prompt ):
		return input( prompt )

	def load_and_eval( self, _cmd, args ):
		# Check if the command is implemented into an external module
		# ex: __hexdump.hexdump()
		mod_name = '__%s' % _cmd
		if self.file_size( '/lib/%s.py' % mod_name )<=0 :
			return 100 # Error 100 when module is not available in /lib
		_mod = __import__( mod_name )
		try:
			fct = eval( '%s.%s' % (mod_name,_cmd), { mod_name : _mod }) # ref to the function __hexdump.hexdump()
			if fct == None:
				self.println( '%s() not available in module %s' % (_cmd, mod_name))
				return 110
			r = fct( self, args )
		except Exception as ex:
			self.println( 'Exception in plugins.' )
			self.println( ex )
		finally:
			del( sys.modules[mod_name] )
		return r

	def read_eval(self): # Evaluate a string command
		cmd = input( '$ ' )
		# Replace heading . with run command
		if (len(cmd)>0) and (cmd[0]=='.'):
			cmd = 'run %s'%cmd[1:]

		l = cmd.split() # should be improved to mange string containsing spaces
		if (l == None) or (len(l)==0):
			return 0 # ignore this
		_cmd = l[0]
		_args = []
		for item in l[1:] :
			_args.append( item.strip('"') )

		if _cmd in COMMANDS: # Inner command
			fct = eval( 'run_%s' % _cmd ) # ref to the function
			return fct( self, _args )
		else:
			ret_code = self.load_and_eval( _cmd, _args ) # Locate & execute cmd from external module
			gc.collect() # grab as many bytes from RAM as possible
			if ret_code == 100: # Not located
				self.println( 'undefined command %s!' % _cmd )
				return 0 # not an ERROR
			else: # External commande executed
				return ret_code

	# ---- Toolbox ----
	def file_size( self, fname ):
		try:
			return os.stat(fname)[6]
		except OSError:
			return -1


	def run( self ):
		while True:
			try:
				_err = self.read_eval()
				if _err != 0:
					self.println( 'ERROR %i' % _err )
			except Exit:
				self.println('Exiting Mini Shell')
				break
			except EAbort:
				self.println('Abort!')


_ms = None

def run():
	global _ms
	print( "                   __        ___          " )
	print( " |\/| | |\ | |    /__` |__| |__  |    |   " )
	print( " |  | | | \| |    .__/ |  | |___ |___ |___" )
	print( "%s%s" % (" "*36, __version__) )
	print( "build-in:", ", ".join(COMMANDS) )
	print( "Python  : %s" % sys.version )
	print( "Free Mem: %i bytes" % gc.mem_free() )
	print( "Use mshell.run() to restart!")
	print( " " )
	if _ms == None:
		_ms = MiniShell()
	_ms.run()

run()
