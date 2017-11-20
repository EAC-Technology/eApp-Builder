import managers
import ProAdmin
import json

def is_admin():
	# get server's user
	user = managers.request_manager.current.session().user
	return user == u'root'


def send_response( message ):
	session[ 'response' ] = json.dumps( message )


class PermissionDeniedError( Exception ):
	def __init__( self ):
		Exception.__init__( 'Permissions denied' )

class ArgumentsError( Exception ):
	def __init__( self, message ):
		Exception.__init__( self, 'Arguments Error: %s' % message )

class RootUserNotFoundError( Exception ):
	def __init__( self ):
		Exception.__init__( 'root-user not found!' )


class SilenException( Exception ):
	pass



try:
	if not is_admin():
		raise PermissionDeniedError()

	# get params
	args = json.loads( request.arguments.get( 'xml_data', '' ) )
	if not args:
		raise ArgumentsError( 'Action arguments not found.' )

	# get password
	password = args.get( 'password', '' )
	if not password:
		raise ArgumentsError( '"password" argument not found' )

	# get root user
	users = ProAdmin.application().get_users( 'root' )
	root = users[ 0 ] if users else None

	if not root:
		raise RootUserNotFoundError()

	# change root password
	root.password = password
	root.save()

	send_response( ['success'] ) #added [] 10.01.2013 Nikita




except PermissionDeniedError as er:
	send_response( [ 'error', er.message ] )

except ArgumentsError as er:
	send_response( [ 'error', er.message ] )

except RootUserNotFoundError as er:
	send_response( [ 'error', er.message ] )

except Exception as er:
	send_response( [ 'error', er.message ] )

except SilenException:
	pass
