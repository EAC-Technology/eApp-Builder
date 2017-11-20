import ProAdmin


class ACLUser( object ):

	def __init__( self, user ):
		self.user = user

	@property
	def guid( self ):
		return self.user.guid


	@property
	def first_name( self ):
		return self.user.first_name


	@property
	def last_name( self ):
		return self.user.last_name


	def is_admin( self ):
		return bool( ProAdmin.application().rules( subject = self.user, access='a' ) )

	@staticmethod
	def current():
		user = ProAdmin.current_user()
		return ACLUser( user ) if user else None



