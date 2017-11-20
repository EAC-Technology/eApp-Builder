from api_helper import *


#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	guids 		= data.get( "guid", None )
	withUsers 	= bool( data.get( "users", False ) )

	if guids and not isinstance( guids, list ):
		guids = ( guids, )

	import ProAdmin
	app = ProAdmin.application()
	groups = []
	append = groups.append

	user_to_dict = lambda user: {
			"name" 			: user.guid,
			"email" 		: user.email,
			"first_name" 	: user.first_name,
			"last_name"		: user.last_name
		}

	def group_to_dict( group ):
		group_dict = { "guid" : group.guid, "name" : group.name }
		if withUsers: group_dict[ "users" ] = map( user_to_dict, group.get_users() )
		return group_dict


	if guids:
		for guid in guids:
			group = app.get_groups( guid = guid )
			if group: append( group_to_dict( group[ 0 ] ) )

	else:
		groups = map( group_to_dict, app.get_groups() )


	write_response( groups )


main()
