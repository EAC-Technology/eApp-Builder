import traceback, sys, cgi
import cProfile


__version__ = '1.0.10'


# ---------------------------------------------------------------------------------
#		Functions, usefull for debug prints
# ---------------------------------------------------------------------------------

def r(o, cont=None):
	text = '<pre style="word-wrap: break-word;">{0}</pre>'.format( cgi.escape(str(o)) )
	response.write( text, bool(cont) )

def d(o, cont=None): r( dir(o), cont )
def l(o, cont=None): r( len(o), cont )
def t(o, cont=None): r( type(o), cont )
def fa(f,cont=None): r( f.im_func.func_code.co_varnames, cont )



class ProfilerStats( object ):
	""" Wrapper for cProfile Stat object. Provide sorts and pretty output prints.
	"""
	def __init__( self, stats ):
		self.stats = stats


	def sort_by_totaltime( self ):
		self.stats.sort( cmp=lambda a,b: cmp( a.totaltime, b.totaltime ), reverse=True )

	def sort_by_inlinetime( self ):
		self.stats.sort( cmp=lambda a,b: cmp( a.inlinetime, b.inlinetime ), reverse=True )

	def sort_by_callcount( self ):
		self.stats.sort( cmp=lambda a,b: cmp( a.callcount, b.callcount ), reverse=True )


	def to_string( self ):
		def parse_code( c ):
			if isinstance(c,basestring): return c

			result = '{0:50}\t{1:4} : {2}'.format( c.co_name, c.co_firstlineno, c.co_filename )
			return result

		result = []

		header = '{0:9}\t{1:9}\t{2:9}\t{3:50}\t{4:6} {5}'.format( 'call count', 'total time', 'inline time', 'function', 'line', 'file' )
		result.append( header )
		result.append( '-' * 220 )

		for s in self.stats:
			line = '{0:9}\t{1:9f}\t{2:9f}\t{3}'.format( s.callcount, s.totaltime, s.inlinetime, parse_code(s.code) )
			result.append( line )

		return '\n'.join( result )


	def to_escaped_string( self ):
		return cgi.escape( self.to_string() )


	def to_s( self ):
		return self.to_string()

	def to_es( self ):
		return self.to_escaped_string()




class Debug( object ):
	""" Provide methods for debug information like stack traces, frames dump and profiling.
	"""
	@classmethod
	def exception_trace( self ):
		_type, val, tb = sys.exc_info()
		return traceback.format_exception( _type, val, tb )

	@classmethod
	def exception_trace_s( self ):
		return '\n'.join( self.exception_trace() )

	@classmethod
	def exception_trace_es( self ):
		return cgi.escape( self.exception_trace_s() )

	@classmethod
	def print_traceback( self ):
		""" this method returns exception trace, used in VEE
		"""
		type, val, exc_tb = sys.exc_info()
		return [ u"""File: "{file_name}", line {line}, in {func}""".format(
					file_name 	= line[ 0 ].split( "/" )[ -1 ],
					line 		= line[ 1 ] - 3 , #get real line number
					func		= line[ 2 ] )
			for line in traceback.extract_tb( exc_tb ) ]



	@classmethod
	def stack_trace( self ):
		return traceback.format_stack()

	@classmethod
	def stack_trace_s( self ):
		return '\n'.join( self.stack_trace() )

	@classmethod
	def stack_trace_es( self ):
		return cgi.escape( self.stack_trace_s() )



	@classmethod
	def frames_dump( self, thread_id=None ):
		threads = {}

		thread_id = thread_id or []
		if not isinstance(thread_id, list): thread_id = [thread_id]

		for threadId, stack in sys._current_frames().items():
			if thread_id and threadId not in thread_id: continue

			threads[ threadId ] = []
			code = threads[ threadId ]

			for filename, lineno, name, line in traceback.extract_stack(stack):
				code.append('File: "%s", line %d, in %s' % (filename, lineno, name))

				if line:
					code.append("  %s" % (line.strip()))

		return threads

	@classmethod
	def frames_dump_s( self, thread_id=None ):
		result = []
		threads = self.frames_dump( thread_id )

		for id in threads:
			result.append( '-' * 120 )
			result.append( 'ThreadID: {0}'.format( id ) )
			result += threads[ id ]
			result.append( '' )
			result.append( '' )

		return '\n'.join( result )

	@classmethod
	def frames_dump_es( self, thread_id=None ):
		return cgi.escape( self.frames_dump_s(thread_id) )




	@classmethod
	def profile( self, f, *args, **kwargs ):
		profiler = cProfile.Profile()
		profiler.runcall( f, *args, **kwargs )
		stats = profiler.getstats()

		return ProfilerStats( stats )

	@classmethod
	def profile_s( self, f, *args, **kwargs ):
		res = self.profile( f, *args, **kwargs )
		res.sort_by_totaltime()
		return res.to_string()

	@classmethod
	def profile_es( self, f, *args, **kwargs ):
		return cgi.escape( self.profile_s( f, *args, **kwargs ) )







# -----------------------------------
#	Obsolete. Use for compatibility.
# -----------------------------------

class Trace( object ):
	@classmethod
	def exception_trace( self, stacksize=0 ):
		return Debug.exception_trace_es()


	@classmethod
	def stack_trace( self ):
		return Debug.stack_trace_es()


	@classmethod
	def print_traceback( self ):
		return Debug.print_traceback()

	@classmethod
	def print_trace( self ):
		return self.print_traceback()



