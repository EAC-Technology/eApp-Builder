from proadmin_utils import Utils


login = request.arguments.get( 'login', '' )
password = request.arguments.get( 'password', '' )

try:
	if login:
		Utils.login( login, password )

	self.action( 'goTo', '/proadmin' )


except:
	pass