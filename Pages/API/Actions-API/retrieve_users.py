from api_helper import *


#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	guids 	= data.get( "guid", None )
	withGroups 	= bool( data.get( "groups", False ) )

	if guids and not isinstance( guids, list ):
		guids = ( guids, )

	import ProAdmin
	app = ProAdmin.application()
	users = []
	append = users.append

	group_to_dict = lambda group: {
			"guid" 			: group.guid,
			"email" 		: group.name,
		}

	def user_to_dict( user ):
		user_dict = {
			"guid" 			: user.guid,
			"email" 		: user.email,
			"first_name" 	: user.first_name,
			"last_name"		: user.last_name
		}
		if withGroups: user_dict[ "groups" ] = map( group_to_dict, user.get_groups() )
		return user_dict

	if guids:
		for guid in guids:
			user = app.get_users( guid = guid )
			if user: append( user_to_dict( user[ 0 ] ) )

	else:
		users = map( user_to_dict, app.get_users() )


	write_response( users )


main()
