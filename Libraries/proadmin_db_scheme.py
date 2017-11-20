from proadmin_base_scheme import BaseProAdminScheme
from proadmin_db_aclobject import DbACLObject

class DbApplicationScheme( BaseProAdminScheme ):
	""" ProAdmin scheme working with 
	"""
	def __init__( self, guid=None, connection=None ):
		BaseProAdminScheme.__init__( self, guid, connection, connection )
		
		self.type 	= 'local'		
		self.set_option( 'root_user', 'root' )
		self.set_option( 'admin_group', 'Administrators' )



	def register( self, make_default=None ):
		""" register this scheme
		"""
		import ProAdmin
		self._application = DbACLObject.application( self.name, self.guid, self )

		ProAdmin.register_scheme( self )





	def create_root_user( self, password='root' ):
		"""	 create super user for this scheme
		"""
		# get root user
		email = self.get_option( 'root_user' )
		users = self.get_users( email )
		root = users[0] if users else None
		
		if not root:
			root = self.create_user( email )
			root.first_name = email
			root.password = password
			root.save()
		
		# try to get admins group
		name = self.get_option( 'admin_group' )
		admins = self.get_groups( name )
		admins = admins[0] if admins else None
		
		if not admins:
			return root
			
		# check that root in admins group
		if root not in admins.get_users():
			admins.add_user( root )
			admins.save()
		
		return root



	def create_admins_group( self ):
		""" group of application administrators
		"""
		# try to get admins group
		name = self.get_option( 'admin_group' )
		admins = self.get_groups( name )
		admins = admins[0] if admins else None
		
		# creat group if need
		if not admins:
			admins = self.create_group( name )
			admins.save()
		
		# add root user to group
		email = self.get_option( 'root_user' )
		users = self.get_users( email )
		root = users[0] if users else None
		
		if not root: return admins
		
		if root not in admins.get_users():
			admins.add_user( root )
			admins.save()
				
		return admins
		


	def create_user( self, email='' ):
		from proadmin_db_user import DbUser

		if email:
			users = self.get_users( email = email )
			if users: return users[0]
	
		user = DbUser( scheme = self )
		user.email = email
		return user

	def create_group( self, name='' ):
		from proadmin_db_group import DbGroup
		groups = self.get_groups( name = name ) if name else []
		if groups: return groups[0]
		
		group = DbGroup( scheme = self )
		group.name = name
		return group

	def get_users( self, email=None, guid=None ):
		from proadmin_db_user import DbUser
		return DbUser.get_users( scheme=self, email=email, guid=guid )

	def get_users_in_group( self, group):
		from proadmin_db_user import DbUser
		return DbUser.get_in_group( self, group )


	def get_groups( self, name=None, user=None, guid=None ):
		from proadmin_db_group import DbGroup
		return user.get_groups() if user else DbGroup.get_groups( scheme = self, guid = guid, name = name )


	def check_password( self, user, password ):
		return user.check_local_password( password )