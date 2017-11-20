#Tools for compilation and execution
from vscript.errors import generic, python, internal_error
from vscript.engine import vcompile, vexecute
import sys, time

VScriptExecutionError 	= VScriptComlipationError 	= generic
PythonExecutionError 	= PythonCompilationError  	= python
VScriptInternalError    = internal_error


def safe_execute( routine, timeout, *arguments, **keywords ):
	__trace = sys.gettrace()
	get_time, deadline = time.time, time.time() + timeout

	def trace( frame, event, arguments ):
		if get_time() > deadline:
			raise VScriptExecutionError("Execution timeout")
		return trace

	try:
		if not __trace:
			sys.settrace(trace)
		return routine(*arguments, **keywords)
	finally:
		if not __trace:
			sys.settrace( None )



class StopExecutionError( python ):
	pass


def compile( source_code, environment = None, silent = False, context = None ):
	try:
		return vcompile(source_code, anyway = silent, environment = environment)
	except VScriptComlipationError:
		raise
	except PythonCompilationError:
		raise


TIME_OUT = 300 #5 minutes
def execute( byte_code, source_code, environment = None, safe = True ):
	try:
		if not safe:
			vexecute( byte_code, source_code, environment = environment )
		else:
			safe_execute( vexecute, TIME_OUT, byte_code, source_code, environment = environment )
	except VScriptExecutionError:
		raise
	except PythonExecutionError:
		raise


def register_lib(name, cache, debuginfo, environment, context):
	server.vscript.libraries.register(name, cache, debuginfo, environment=environment, context=context)


def unregister_lib(name, context):
	try:
		server.vscript.libraries.unregister(name, context=context)
	except KeyError:
		pass
