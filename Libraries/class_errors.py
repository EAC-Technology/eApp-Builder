class AccessDeniedError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'You have no permissions to perform this action.' )


class SessionExpiredError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Session has expired.' )


class AuthorisationError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'No one is logged in.' )


class UknownAccessTypeError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Unkwon access type provided.' )


class RemoteApplicationDisconnected( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Application disconnected. ID : %s.')


class RemoteSchemeProtection( Exception ):
	pass
