import copy

# -------------------------------------------------------------------
#		Description of object type
# -------------------------------------------------------------------

class ACLObjectType( object ):
	""" class for descript ACLObjectType - contains: name, icon, and access types
	"""
	def __init__( self, name="", guid="", icon=None ):
		self.name 			= name
		self.guid			= guid
		self.icon			= icon
		
		self._accesstypes 	= {}


	@property
	def access_types( self ):
		return self._accesstypes
	
	@access_types.setter
	def access_types( self, value ):
		self._accesstypes = copy.deepcopy( value )
	

	def get_access_types( self ):
		""" obsolete. need for compatibility
		"""
		return self.access_types

	def set_access_types( self, value ):
		""" obsolete. need for compatibility
		"""
		self.access_types = value



	@property
	def object_icon_url( self ):
		return self.icon.resource_url


	def get_object_icon_url( self ):
		""" obsolete. need for compatibility
		"""
		return self.icon.resource_url


	def __eq__( self, other ):
		return self.guid == other.guid




# -------------------------------------------------------------------
#		Icon
# -------------------------------------------------------------------

class Icon( object ):
	""" class for Icon routines in ProAdmin
	"""
	def __init__( self, res_name="" ):
		self._resource_url	= res_name


	@classmethod
	def on_resource( self, res_name ):
		""" create Icon object from resource image
		"""
		url = "/%s.res" % res_name
		return Icon( url ) 


	@property
	def resource_url( self ):
		return self._resource_url
		
		
	def get_resource_url( self ):
		"""
		"""
		return self.resource_url







# -------------------------------------------------------------------
#		Base class for ProAdmin Schemas
# -------------------------------------------------------------------

class BaseProAdminScheme( object ):
	""" Base class for ProAdmin scheme
	"""
	def __init__( self, guid=None, objects_connection=None, subjects_connection=None ):
		# connections
		self._objects_conn	= objects_connection
		self._subjects_conn	= subjects_connection

		# main attributes
		self.guid		= guid
		self.name		= ''
		self.icon		= None
		self.type 		= ''
		self.config		= None

		# application instance
		self._application = None

		# specific scheme oprtions
		self.options			= {}

		# acl object types
		self._acl_object_types	= []
		self.prepare_synchronize = None
	
	
	# --------------------------------
	#	Properties
	# --------------------------------
	
	@property
	def application( self ):
		return self._application
		
	def get_application( self ):
		""" obsolete. need for compatibility
		"""
		return self.application
		
		
		
		
	@property
	def objects_connection( self ):
		return self._objects_conn
		
	@property	
	def connection( self ):
		""" obsolete. need for compatibility
		"""
		return self.objects_connection
		
	def get_connection( self ):
		""" obsolete. need for compatibility
		"""
		return self.objects_connection


		
	@property
	def subjects_connection( self ):
		return self._subjects_conn

	def userconnection( self ):
		""" obsolete. need for compatibility
		"""
		return self.subjects_connection
		
		
			
		
	
	def is_remote( self ):
		return self.type == 'remote'


	def synchronize( self ):
		pass





	def register( self, make_default=None ):
		""" register this scheme
		"""
		from proadmin_acl_object import ACLObject
		import ProAdmin
		self._application = ACLObject.application( self.name, self.guid, self )

		ProAdmin.register_scheme( self )
		
		
	def unregister( self ):
		""" unregister this scheme
		"""
		import ProAdmin
		ProAdmin.unregister_default_scheme()


	def delete( self ):
		""" delete this scheme from LDAP
		"""
		import ProAdmin

		self.application.delete()
		ProAdmin.delete_scheme( self )




	def set_information( self, name="", icon=None ):
		""" set information about scheme: name and icon
		"""
		self.name = name
		self.icon = icon


	def set_option( self, key, value ):
		""" set value for option specific for application
		"""
		self.options[ key ] = value


	def get_option( self, key, default_value=None ):
		"""
		"""
		return self.options.get( key, default_value )


	def set_api_guid( self, api_guid ):
		""" set api guid
		"""
		self.set_option( 'api_guid', api_guid )


	def get_registered_applications( self ):
		""" get applications info that can connecting via API from this applicatino
		"""
		import ProAdmin
		
		app_info = {
			'name'		: self.name,
			'guid'		: self.guid,
			'ip'		: '127.0.0.1',
			'api_guid'	: self.get_option( 'api_guid' ),
			'hosts'		: ProAdmin.hosts(),
		}

		return { self.name : app_info }

	def get_registred_applications( self ):
		""" obsolete. need for compatibility
		"""
		return self.get_registered_applications()




	def get_application_icon_url( self ):
		""" return resource URL to application icon
		"""
		return self.icon.get_resource_url()

	def add_aclobjecttype( self, object_type):
		if not (object_type in self._acl_object_types):
			self._acl_object_types.append( object_type )

	def get_aclobjecttypes( self ):
		return self._acl_object_types


	application_icon_url = property( get_application_icon_url )




	def create_root_user( self ):
		pass
		
	def create_admins_group( self ):
		pass

	def create_user( self ):
		pass

	def create_group( self ):
		pass

	def get_users( self, email='', guid='' ):
		pass

	def get_groups( self, guid='', name='', user=None ):
		pass



	def check_password( self, user, password ):
		return False



