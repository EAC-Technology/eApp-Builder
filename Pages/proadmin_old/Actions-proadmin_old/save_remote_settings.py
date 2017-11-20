from proadmin_utils import Utils


class SilentException( Exception ):
	pass


server = request.arguments.get( 'server', '' )
login = request.arguments.get( 'login', '' )

password = request.arguments.get( 'password', '' )
password = '' if password == '*'*8 else password


try:
	if not Utils.is_admin():
		raise SilentException()

	if Utils.is_proadmin():
		raise SilentException()

	# try to save settings
	Utils.set_remote_settings( server, login, password )

	self.action( 'goTo', '/proadmin' )


except SilentException:
	pass