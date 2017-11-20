from proadmin_base_scheme import BaseProAdminScheme
from proadmin_ldapconfig import LDAPConfig

class LocalLDAPApplicationScheme( BaseProAdminScheme ):
	""" ProAdmin scheme working with 
	"""
	def __init__( self, guid=None, connection=None ):
		BaseProAdminScheme.__init__( self, guid, connection, connection )
		
		
		self.type 	= 'local'		
		self.config = LDAPConfig.create_config( config = 'local' )
		
		self.set_option( 'base_dn', "dc=vdombox,dc=local" )

		self.set_option( 'root_user', 'root' )
		self.set_option( 'admin_group', 'Administrators' )



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
		users = self.get_users( email ) if email else []
		if users: return users[0]
		
		from proadmin_subject import LDAPUser
		return LDAPUser.create( scheme = self, email = email )

	def create_group( self, name='' ):
		groups = self.get_groups( name ) if name else []
		if groups: return groups[0]
		
		from proadmin_subject import LDAPGroup
		return LDAPGroup.create( scheme = self, name = name )

	def get_users( self, email=None, guid=None ):
		from proadmin_subject import LDAPUser		
		return LDAPUser.get_users( self, email=email, guid=guid )

	def get_groups( self, name=None, user=None, guid=None ):
		from proadmin_subject import LDAPGroup
		groups = user.get_groups() if user else LDAPGroup.get_groups( scheme = self, guid = guid, name = name )
		return groups



	def check_password( self, user, password ):
		return user.check_local_password( password )


