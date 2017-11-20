from api_helper import *


#@license_confirmed
#@authenticated
@error_handler
def main( ):

	import json, ProAdmin

	try:
		params = json.loads( request.arguments.get( 'xml_data' ) )
	except Exception, ex:
		raise Exception(str(request.arguments.get( 'xml_data' )))
		raise APICallFailedException("errBadJSONFormat")

	token 		= params.get( 'token', '' )
	login 		= params.get( 'login', '' )
	password 	= params.get( 'password', '' )

	if not token and not any( (login, password) ):
		raise APICallFailedException( "errEmptyPassword" )


	try:
		if token:
			ProAdmin.login_token( token )
		else:
			ProAdmin.login( login, password )

		user = ProAdmin.current_user()

		data = {
			"guid" 			: user.guid,
			"email" 		: user.email,
			"first_name" 	: user.first_name,
			"last_name"		: user.last_name
		}

		write_response( data )

	except ProAdmin.ProAdminEmptyPasswordError, ex:
		raise APICallFailedException( "errEmptyPassword" )

	except ProAdmin.ProAdminLoginError, ex:
		raise APICallFailedException( "errLoginError" )


main()
