from api_error_code import error_code


def api_response_pair(success, value):
	return { "success" if success else "error": value}



class APICallFailedException( Exception ):
	def __init__(self, message, additional_info = None ):
		Exception.__init__( self, message )
		self.info = additional_info



#used for API methods
def _write_response( data ):
	import json
	session[ 'response' ] = json.dumps( data )


def write_response( data = None ):
	_write_response( [ 'success', data ] if data is not None else [ 'success' ] )


def write_error( error_type, error_msg ):
	_write_response( [ 'error', error_type, error_msg ] )


def authenticated( method ):
	def wrapper( *args, **kwargs ):
		import ProAdmin
		if ProAdmin.current_user() is None:
			write_error( *error_code[ 'errNotLoggedIn' ] )
		else:
			return method()
	return wrapper


def license_confirmed( method ):
	def wrapper( *args, **kwargs ):
		from class_license import License
		if not License().confirmed:
			write_error( *error_code[ 'errNoLicense' ] )
		else:
			return method()
	return wrapper


def error_handler( method ):
	def wrapper( *args, **kwargs ):
		try:
			return method()
		except APICallFailedException, cfex:
			err = error_code[ cfex.message ]
			write_error( err[ 0 ], err[ 1 ] + ( ( ": " + cfex.info ) if cfex.info else "" )  )

		except:
			from vdom_trace import Trace
			write_error( error_code[ 'errScriptError' ][0], Trace.exception_trace() )

	return wrapper


def parse_json( method ):
	def wrapper( *args, **kwargs ):
		import json
		try: data = json.loads( request.arguments.get( 'xml_data' ) )
		except Exception, ex: raise APICallFailedException( "errBadJSONFormat" )
		return method( data, *args, **kwargs )
	return wrapper
