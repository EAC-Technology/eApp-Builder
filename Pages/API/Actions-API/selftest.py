import ProAdmin
import managers
import json


def is_admin():
	# get server's user
	user = managers.request_manager.current.session().user
	return user == u'root'


def success_result():
	send_response( json.dumps( ["success"] ) )


def error_result( message = '' ):
	send_response( json.dumps( ["error", message] ) )


def send_response( message ):
	session[ 'response' ] = message


class PermissionDeniedError( Exception ):
	pass


try:
	if not is_admin():
		raise PermissionDeniedError()

	success_result()

except PermissionDeniedError:
	error_result( 'Permission denied' )

except Exception as ex:
	error_result( ex.message )
