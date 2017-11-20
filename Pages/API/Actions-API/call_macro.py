from api_helper import *

#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	require_fileds = [ "plugin_guid", "name" ]
	for field in require_fileds:
		if 	field not in data or data[ field ] == "" :
			raise APICallFailedException( "errBadObjectFormat", field )

	from VEE_events import VEE_CustomEvent
	from VEE_core import engine
	from VEE_utils import AutoCast

	event = VEE_CustomEvent()
	event.name = data[ "name" ]
	event.plugin_guid = data[ "plugin_guid" ]
	event.data = data.get( "data", None )

	if data.get( "async", True ):
		event.activate()
		write_response( None )

	else:
		dispatcher = engine.get_dispatcher_by_event( event )
		if not dispatcher:
			raise APICallFailedException( "errBadObjectFormat", "No dispatcher for given data" )


		class v_response( object ):
			def __init__( self ):
				self.value = ""

			@AutoCast
			def v_write( self, value ):
				self.value = value

		v_responseObj = v_response()

		dispatcher(  event 		= event,
					 env_mask 	= 0b1111,
					 custom_env = ( ( "v_response", v_responseObj ), ),
					 safe = False 	)

		try:
			write_response( v_responseObj.value )
		except:
			raise APICallFailedException( "errBadObjectFormat", "Bad response format" )



main()
