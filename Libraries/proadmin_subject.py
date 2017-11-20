from abc import abstractmethod
from md5 import md5

import copy
import cgi
import re
import base64

import uuid

import ProAdmin


# ----------------------------------------------------------------
#		Subject
# ----------------------------------------------------------------

class Subject( object ):
	""" Base class for subject structures
	"""
	def __init__( self, scheme ):
		self._guid = ''
		self.scheme = scheme


	def fill_guid_list( self ):
		pass


	def get_guid_list( self ):
		return [ self.guid ]


	@abstractmethod
	def save( self ):
		""" save subject changes
		"""
		return self


	def delete( self, force=False ):
		""" delete subject
		"""
		self.force_delete( force=force )


	@abstractmethod
	def force_delete( self, force=True ):
		raise Exception('Subclass resposibility')


	@classmethod
	def _escape( self, value ):
		""" escape string values
		"""
		if not value:
			value = ''

		return cgi.escape( value )


	@classmethod
	def _modify_dn( self, dn ):
		""" This method get attribute value from dn string.
			Example: dn = 'Cn=Users'. In this case the method returnes 'Users'. ###
		"""
		if type( dn ) == list:
			dn = dn[0]

		dn = self._escape( dn ).split( '=' )

		if len( dn ) == 1:
			return dn[0]

		result = ''
		dn = dn[1:]
		for i in dn:
			result += i

		return result


	@classmethod
	def _scalar( self, value ):
		if not value: value = ''
		if type( value ) == list:
			return self._scalar( value[0] )

		return value.strip()


	def is_admin( self ):
		""" get answer for subject is admin: user-root, group-admin
		"""
		return False

	def is_user( self ):
		""" get answer that subject is user
		"""
		return False

	def is_group( self ):
		""" get answer that subject is group
		"""
		return False


	def is_persistent( self ):
		""" get answer that subject persistent or non persistent
		"""
		pass


	@property
	def guid( self ):
		""" return guid of subject
		"""
		return self._guid

	@guid.setter
	def guid( self, value ):
		""" set guid for subject
		"""
		self._guid = self._scalar( value )


	def __hash__( self ):
		return hash( self.guid )


	def _is_addled_instance( self ):
		""" check, maybe this instance is addled
		"""
		try:
			import ProAdmin
		except ImportError:
			return True

		return False






# ----------------------------------------------------------------
#		User
# ----------------------------------------------------------------

class User( Subject ):
	""" Base class for users
	"""
	def __init__( self, scheme ):
		Subject.__init__( self, scheme )

		# addition attributes
		self._email 		= ''
		self._phone 		= ''
		self._first_name 	= ''
		self._last_name 	= ''
		self._password 		= ''

		self._notification_email = ''
		self._cell_phone	= ''
		self._country		= ''
		self._keywords		= ''

		self._options 		= {}

		# save user-group relationship
		self.group_guid_list = []


	def is_user( self ):
		return True

	def is_group( self ):
		return False


	@property
	def email( self ):
		return self._email

	@email.setter
	def email( self, value ):
		self._email = self._scalar( value )


	@property
	def phone( self ):
		return self._phone

	@phone.setter
	def phone( self, value ):
		self._phone = self._scalar( value )


	@property
	def first_name( self ):
		return self._first_name

	@first_name.setter
	def first_name( self, value ):
		self._first_name = self._scalar( value )


	@property
	def last_name( self ):
		return self._last_name

	@last_name.setter
	def last_name( self, value ):
		self._last_name = self._scalar( value )


	@property
	def name( self ):
		name = '%s %s' % (self.first_name, self.last_name,)
		name = name.strip()
		name = name if name else self.email
		return name


	@property
	def password( self ):
		return self._password

	@password.setter
	def password(self, value ):
		self._password = value



	@property
	def notification_email( self ):
		return self._notification_email

	@notification_email.setter
	def notification_email( self, value ):
		self._notification_email = value


	@property
	def cell_phone( self ):
		return self._cell_phone

	@cell_phone.setter
	def cell_phone( self, value ):
		self._cell_phone = value


	@property
	def country( self ):
		return self._country

	@country.setter
	def country( self, value ):
		self._country = value


	@property
	def keywords( self ):
		return self._keywords

	@keywords.setter
	def keywords( self, value ):
		self._keywords = value
	

	@property
	def options(self):
		return self._options

	@options.setter
	def options(self, value):
		self._options = value




	def get_groups( self ):
		""" return list of groups which contains user
		"""
		return [ Everyone( self.scheme ) ]


	@classmethod
	def get_users( self, scheme, email, guid ):
		return []


	def get_name( self ):
		""" OBSOLETE. need for capability.
		"""
		return self.name


	def check_local_password( self, password ):
		return False

	def get_guid_list( self ):
		groups = self.get_groups()
		return [ group.guid for group in groups ] + [ self.guid ]


	def __pack( self ):
		attributes = {
			'guid'					: self.guid,
			'email'					: self.email,
			'first_name'			: self.first_name,
			'last_name'				: self.last_name,
			'phone'					: self.phone,
			'password'				: self.password,
			'notification_email'	: self.notification_email,
			'cell_phone'			: self.cell_phone,
			'country'				: self.country,
			'keywords'				: self.keywords,
			'options' 				: self.options,
			'root'					: self.is_root(),
		}

		return attributes
	
	def _pack(self):
	    return self.__pack()

	def is_root(self):
		return False


	def __eq__( self, other ):
		if not other: return False
		if not other.is_user(): return False
		return self.__pack() == other.__pack()



	def check_password( self, password ):
		"""
		"""
		return self.scheme.check_password( self, password )

	def set_password_hash(self, hash_p):
		raise Exception("should be implemented in subclass")

# ----------------------------------------------------------------
#		Group
# ----------------------------------------------------------------

class Group( Subject ):
	""" Base class for groups
	"""
	def __init__( self, scheme ):
		Subject.__init__( self, scheme )

		# addition fields
		self._name 	= ''
		self._guid 	= ''

		# save group-user relationship
		self.user_guid_list = []


	def is_user( self ):
		return False

	def is_group( self ):
		return True


	def add_user( self, user ):
		raise Exception('Subclass resposibility')

	def remove_user( self, user ):
		raise Exception('Subclass resposibility')

	def delete_user( self, user, force=False ):
		raise Exception('Subclass resposibility')


	@abstractmethod
	def get_users( self ):
		raise Exception('Subclass resposibility')


	@classmethod
	def get_groups( self, scheme, name=None, guid=None ):
		return Everyone.get_groups( scheme, name, guid )


	@classmethod
	def create( self, scheme, name ):
		raise Exception('Subclass resposibility')



	@property
	def name( self ):
		return self._name

	@name.setter
	def name( self, value ):
		self._name = self._scalar( value )


	@property
	def guid( self ):
		return self._guid

	@guid.setter
	def guid( self, value ):
		self._guid = self._scalar( value )

	
	def _is_everyone_group( self ):
		return self.guid == Everyone.GUID


	def __pack( self ):
		# get group's users guids
		#members = list(set( [ user.guid for user in group.get_users() ] ))

		attributes = {
			'guid'		: self.guid,
			'name'		: self.name,
			#'members'	: members,
		}

		return attributes


	def __eq__( self, other ):
		if not isinstance( other, Group ): return False
		return self.__pack() == other.__pack()





class Everyone( Group ):
	""" Special group contains all users
	"""
	GUID = u'all-0e88aeaa-9384-43a4-b068-96bfc54c9d7b'
	NAME = u'Everyone'

	def __init__( self, scheme ):
		Group.__init__( self, scheme )
		self.guid = Everyone.GUID
		self.name = Everyone.NAME

	def get_users( self ):
		import ProAdmin
		return ProAdmin.application().get_users()

	@classmethod
	def get_groups( self, scheme, name=None, guid=None ):
		if guid and guid == Everyone.GUID:
			return [ Everyone(scheme) ]

		if not guid and name and name == Everyone.NAME:
			return [ Everyone(scheme) ]

		if not name and not guid:	
			return [ Everyone(scheme) ]

		return []

	def force_delete( self, force=True ):
		pass


	def __eq__( self, other ):
		if not isinstance( other, Everyone ): return False
		return True


	def add_user( self, user ):
		pass
		
	def remove_user( self, user ):
		pass

	def delete_user( self, user, force=False ):
		pass



# ----------------------------------------------------------------
#		LDAP User
# ----------------------------------------------------------------

class LDAPUser( User ):
	""" implementation of User for LDAP base
	"""

	# marker that group attribute of ldap object are empty
	_EMPTY_GROUP_VALUE = 'dc=vdombox'



	def __init__( self, scheme, ldapobject = None ):
		User.__init__( self, scheme )

		# create ldap object
		self._ldapobject = self.create( email = '' ).ldapobject if not ldapobject else ldapobject



	def _fill_ldapobject( self ):
		""" fill ldap object
		"""
		from proadmin_ldap_object import LDAPObject

		config = self.scheme.config
		dn = self.scheme.get_option( 'base_dn' )

		# filled by config settings
		attributes = {
			'objectClass'						: config.get_attribute( 'user_class' ),
			config.get_attribute( 'user_guid' )	: '',	#  self.guid,
			config.get_attribute( 'email' )		: '', 	#  self.email,
			config.get_attribute( 'last_name' )	: '', 	#  self.last_name or self.email,
			config.get_attribute( 'first_name')	: '', 	#  self.first_name or self.email,
			config.get_attribute( 'password' )	: '', 	#  self.password,
			config.get_attribute( 'phone' )		: '', 	#  self.phone,

			config.get_attribute( 'notification_email' ): '',	#  self.notification_email
			config.get_attribute( 'cell_phone' )		: '',	#  self.cell_phone
			config.get_attribute( 'country' )			: '',	#  self.country
			config.get_attribute( 'keywords' )			: '',	#  self.keywords
		}

		return LDAPObject( dn, attributes )



	def _set_ldap_attribute( self, key, value ):
		if not value: value = [ ' ' ]
		if not isinstance( value, list ): value = [ value ]

		ldap_attribute = self.scheme.config.get_attribute( key )
		self.ldapobject.attributes[ ldap_attribute ] = value


	def _get_ldap_attribute( self, key ):
		ldap_attribute = self.scheme.config.get_attribute( key )
		value = self.ldapobject.attributes.get( ldap_attribute, '' )

		return self._scalar( value )





	@property
	def ldapobject( self ):
		return self._ldapobject

	@ldapobject.setter
	def ldapobject( self, value ):
		self._ldapobject = value




	@property
	def guid( self ):
		return self._get_ldap_attribute( 'user_guid' )

	@guid.setter
	def guid( self, value ):
		value = self._scalar( value )
		self.ldapobject.dn = self.scheme.config.get_user_dn( value, self.scheme.get_option( 'base_dn' ) )
		self._set_ldap_attribute( 'user_guid', value )



	@property
	def email( self ):
		return self._get_ldap_attribute( 'email' )

	@email.setter
	def email( self, value ):
		value = self._scalar( value )
		self._set_ldap_attribute( 'email', value )



	@property
	def phone( self ):
		return self._get_ldap_attribute( 'phone' ) or '0'

	@phone.setter
	def phone( self, value ):
		value = self.modify_phone( value )
		self._set_ldap_attribute( 'phone', value )

	def modify_phone( self, value ):
		value = self._scalar( value )
		new_value = ''
		available = ' +1(234)567-890'
		for i in str(value):
			new_value += unicode( i ) if i in available else ''
		return new_value if new_value else '0'



	@property
	def first_name( self ):
		return self._get_ldap_attribute( 'first_name' )

	@first_name.setter
	def first_name( self, value ):
		value = self._scalar( value )
		self._set_ldap_attribute( 'first_name', value )



	@property
	def last_name( self ):
		return self._get_ldap_attribute( 'last_name' )

	@last_name.setter
	def last_name( self, value ):
		value = self._scalar( value )
		self._set_ldap_attribute( 'last_name', value )



	@property
	def password( self ):
		return self._get_ldap_attribute( 'password' )

	@password.setter
	def password( self, value ):
		if not value: return

		value = self._get_hash( self._scalar( value ) )
		self._set_ldap_attribute( 'password', value )



	@property
	def notification_email( self ):
		return self._get_ldap_attribute( 'notification_email' )

	@notification_email.setter
	def notification_email( self, value ):
		value = self._scalar( value )
		self._set_ldap_attribute( 'notification_email', value )


	@property
	def cell_phone( self ):
		return self._get_ldap_attribute( 'cell_phone' )

	@cell_phone.setter
	def cell_phone( self, value ):
		value = self.modify_phone( value )
		self._set_ldap_attribute( 'phone', value )
		self._set_ldap_attribute( 'cell_phone', value )


	@property
	def country( self ):
		return self._get_ldap_attribute( 'country' )

	@country.setter
	def country( self, value ):
		value = self._scalar( value )
		self._set_ldap_attribute( 'country', value )


	@property
	def keywords( self ):
		ldap_attr = self.scheme.config[ 'keywords' ]
		value = self.ldapobject.attributes.get( ldap_attr, [] )

		# remove duplicated values
		value = list( set(value) )
		self.ldapobject.attributes[ ldap_attr ] = value

		return value

	@keywords.setter
	def keywords( self, value ):
		if not value: value = []

		if not isinstance( value, list ):
			value = [ value ]

		# remove duplicated values
		value = list( set(value) )

		ldap_attr = self.scheme.config[ 'keywords' ]
		self.ldapobject.attributes[ ldap_attr ] = value



	def get_dn( self ):
		""" get user's DN, according to LDAP config
		"""
		config = self.scheme.config
		base_dn = scheme.get_option( 'base_dn' )
		user_dn = config.get_attribute( 'user_dn' )
		user_guid = config.get_attribute( 'user_guid' ) + '=' + self.guid
		return user_guid + ',' + user_dn + ',' + base_dn



	# NEED TO REIMPLEMENT IT
	def is_admin( self ):
		""" obsolete. need for old versions support.
		"""
		return self.is_root()

	def is_root( self ):
		root_user_email = self.scheme.get_option( 'root_user' )
		return True if self.email == root_user_email else False



	@classmethod
	def create( self, scheme, email = '' ):
		""" create user
		"""
		ldapconnection 	= scheme.userconnection()
		config = scheme.config

		baseDN			= scheme.get_option( 'base_dn' )
		user_dn 		= config[ 'user_dn' ]

		# create guid for new user
		guid = str(uuid.uuid4())

		ldap_attributes = {
			'objectClass'					: config[ 'user_class' ],
			config[ 'user_guid' ]			: [ guid ],
			config[ 'email'	]				: [ email ],
			config[ 'password' ]			: [ ' ' ],
			config[ 'first_name' ]			: [ ' ' ],
			config[ 'last_name' ]			: [ ' ' ],
			config[ 'phone' ]				: [ '0' ],

			config[ 'notification_email' ]	: [ ' ' ],
			config[ 'cell_phone' ]			: [ '0' ],
			config[ 'country' ]				: [ ' ' ],
			config[ 'keywords' ]			: [ ' ' ],

		}

		# modify ldap attributes for support 'groups in user' attribute
		groups_in_user = config[ 'groups_in_user' ]
		if groups_in_user:
			ldap_attributes[ groups_in_user ] = [ self._EMPTY_GROUP_VALUE ]

		# create ldap object
		ldap_user = ldapconnection.create_object(
				["%s=%s" % ( config[ 'user_guid' ], guid, ), "%s," % user_dn + baseDN],
				ldap_attributes
		)

		# create nonpersistent LDAPUser
		return LDAPUser( scheme, ldapobject = ldap_user )





	def _exist( self ):
		users = self.scheme.get_users( guid = self.guid )
		return True if users else False



	def save( self ):
		ldapconnection = self.scheme.userconnection()
		if self._exist():
			ldapconnection.update( self.ldapobject )
		else:
			ldapconnection.insert( self.ldapobject )
		return self



	def add_group( self, group, debug = False ):
		if not group: return
		group.add_user( self )
		return self



	def remove_group( self, group ):
		if not group: return
		group.remove_user( self )
		return self



	@classmethod
	def get_users( self, scheme, email = None, guid = None ):
		""" get scheme users
		"""
		config = scheme.config
		filter = '(objectClass=%s)' % config.get_attribute( 'user_class' )[-1]

		if email:
			filter += '(%s=%s)' % ( config.get_attribute( 'email'), email )
		if guid:
			filter += '(%s=%s)' % ( config.get_attribute( 'user_guid' ), self._modify_dn( guid ) )

		filter = '(&' + filter + ')'

		user_dn = config.get_attribute( 'user_dn' )

		if user_dn:
			search_location = '%s,'% user_dn + scheme.get_option( 'base_dn' )

		else:
			search_location = '%s'% scheme.get_option( 'base_dn' )

		ldapobjects = scheme.userconnection().search( search_location, filter, True )


		users = [ LDAPUser( scheme, ldapobject = ldapobject ) for ldapobject in ldapobjects ]


		try:
			users.sort( cmp=lambda a,b: cmp( a.name.lower(), b.name.lower() ) )
		except:
			pass

		return users




	def get_groups( self ):
		""" get scheme groups
		"""
		config = self.scheme.config

		# group.users
		users_in_group = config.get_attribute( 'users_in_group' )
		if users_in_group:
			groups = LDAPGroup.get_groups( self.scheme )
			result = []
			for group in groups:
				if group._is_everyone_group(): continue

				user_dns = group.ldapobject.attributes.get( users_in_group, [] )
				for dn in user_dns:
					if dn == self.ldapobject.dn:
						result.append( group )

			# we experimenting with limited ldap attributes mapping
			try:
				result.sort( cmp=lambda a,b: cmp( a.name.lower(), b.name.lower() ) )
			except:
				pass

			return User.get_groups( self ) + result

		# user.groups
		groups_in_user = config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			group_dns = self.ldapobject.attributes.get( groups_in_user, [] )
			result = []
			for dn in group_dns:
				ldapobject = connection.get_by_dn( dn )
				result.append( LDAPGroup( self.scheme, ldapobject = ldapobject ) )

			# we experimenting with limited ldap attributes mapping
			try:
				result.sort( cmp=lambda a,b: cmp( a.name.lower(), b.name.lower() ) )
			except:
				pass

			return User.get_groups( self ) + result

		return [ Everyone(self.scheme) ]



	def force_delete( self, force = True ):
		if self.is_admin() and not force:
			return
		rules = self.scheme.application.child_rules( subject = self, recursive = True )
		for rule in rules:
			rule.delete()
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' )
		if users_in_group:
			groups = self.get_groups()
			for group in groups:
				group.delete_user( self, force )
		self.scheme.userconnection().delete( self.ldapobject )



	def delete_from_group( self, group, force = False ):
		if self.is_admin() and not force:
			return
		# user.groups
		groups_in_user = self.scheme.config.get_attribute( 'groups_in_user' ) # user.groups
		if groups_in_user:
			self.ldapobject.attributes[ groups_in_user ].remove( group.ldapobject.dn )
			self.save()
			return self

		# group.users
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' ) # group.users
		if users_in_group:
			group.delete_user( user = self, force = force )
			group.save()
		return self



	def _get_hash( self, text ):
		return '{MD5}' + base64.b64encode( md5( text.encode('utf8') ).digest() )


	def set_password_hash( self, hash ):
		self._password = self._scalar( hash )
		if self.ldapobject:
			password_attribute = self.scheme.config.get_attribute( 'password' )
			self.ldapobject.attributes[ password_attribute ] = hash


	def check_password( self, password ):
		"""
		"""
		return self.scheme.check_password( self, password )


	def check_local_password( self, password ):
		hash = self._get_hash( password )
		return hash == self.password



	def __eq__( self, other ):
		if not isinstance( other, LDAPUser ): return False
		return self.ldapobject == other.ldapobject



# ----------------------------------------------------------------
#		LDAP Group
# ----------------------------------------------------------------

class LDAPGroup( Group ):
	""" Group implementation for LDAP base
	"""
	# hack - need for required parameter 'member' in class groupOfNames in LDAP
	# it's value represent empty group.
	_EMPTY_GROUP_VALUE = 'dc=vdombox'


	def __init__( self, scheme, ldapobject = None ):
		Group.__init__( self, scheme )
		self._ldapobject = ldapobject if ldapobject else self.create( name = '' ).ldapobject



	@property
	def ldapobject( self ):
		return self._ldapobject

	@ldapobject.setter
	def ldapobject( self, value ):
		self._ldapobject = value



	@property
	def name( self ):
		name = self._scalar( self.ldapobject.attributes.get( self.scheme.config.get_attribute( 'group_name' ) ) )
		return name or self.guid

	@name.setter
	def name( self, value ):
		value = self._scalar( value )
		if self.ldapobject:
			self.ldapobject.attributes[ self.scheme.config.get_attribute( 'group_name' ) ] = value



	@property
	def guid( self ):
		return self._scalar( self.ldapobject.attributes[ self.scheme.config.get_attribute( 'group_guid' ) ] )

	@guid.setter
	def guid( self, value ):
		value = self._scalar( value )
		self.ldapobject.dn = self.scheme.config.get_user_dn( value, self.scheme.get_option( 'base_dn' ) )
		self.ldapobject.attributes[ self.scheme.config.get_attribute( 'group_guid' ) ] = [ value ]



	def _exist( self ):
		groups = self.scheme.get_groups( guid = self.guid )
		return True if groups else False

	def save( self ):
		self.add_empty_user()
		ldapconnection = self.scheme.userconnection()
		if self._exist():
			ldapconnection.update( self.ldapobject )
		else:
			ldapconnection.insert( self.ldapobject )
		return self



	def is_admin( self ):
		root_group_name = self.scheme.get_option( 'admin_group' )
		return True if self.name == root_group_name else False



	@classmethod
	def create( self, scheme, name='Administrators' ):
		""" create user
		"""
		name = self._scalar( name )

		ldapconnection 	= scheme.userconnection()
		config = scheme.config

		baseDN = config.get_attribute( "base_dn" )
		group_dn = config.get_attribute( 'group_dn' )
		object_class = config.get_attribute( 'group_class' )

		guid_attr_name = config.get_attribute( 'group_guid' )
		name_attr_name = config.get_attribute( 'group_name' )
		user_in_group_attr = config.get_attribute( 'users_in_group' )

		# set default parameters
		guid = str( uuid.uuid4() )
		name = name if name else self.name

		if user_in_group_attr:
			ldap_group = ldapconnection.create_object(
					[ "%s=%s" % ( guid_attr_name, guid ), "%s," % group_dn + baseDN ],
					{
						'objectClass'		: object_class,
						guid_attr_name		: [ guid ],
						name_attr_name		: [ name ],
						user_in_group_attr	: [ self._EMPTY_GROUP_VALUE ],
					})
		else:
			ldap_group = ldapconnection.create_object(
					["%s=%s" % ( guid_attr_name, guid ), "%s," % group_dn + baseDN],
					{
						'objectClass'		: object_class,
						guid_attr_name		: [ guid ],
						name_attr_name		: [ name ],
					})

		return LDAPGroup( scheme, ldapobject = ldap_group )



	def _get_members_dns( self ):
		# vector method was changed
		return self._scalar( 'member' )



	def add_user( self, user ):
		""" add user to group
		"""
		# group.users
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' )
		if users_in_group:
			if user.ldapobject.dn not in self.ldapobject.attributes[ users_in_group ]:
				self.ldapobject.attributes[ users_in_group ].append( user.ldapobject.dn )
				self.save()
			return self

		groups_in_user = self.scheme.config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			if self._scalar( self.ldapobject.dn ) not in user.ldapobject.attributes[ groups_in_user ]:
				user.ldapobject.attributes[ groups_in_user ].append( self._scalar( self.ldapobject.dn ) )
				user.save()
			return self



	def remove_user( self, user ):
		""" remove user from group
		"""
		# group.users
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' )
		if users_in_group:
			self.ldapobject.attributes[ users_in_group ].remove( user.ldapobject.dn )
			self.save()
			return self

		groups_in_user = self.scheme.config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			user.ldapobject.attributes[ groups_in_user ].remove( self.ldapobject.dn )
			self.scheme.userconnection().save( user.ldapobject )
			return self

		return self.force_remove_user( user, force=False )



	def force_remove_user( self, user, force=True ):
		""" remove user from group
		"""

		if self.is_admin() and user.is_admin() and not force:
			return

		user.delete_from_group( group = self, force = force )
#
#		if user in self.users:
#			self.users.remove( user )

#		members = self._get_members_dns()
#
#		#remove default entry
#		if user.ldapobject.dn in members:
#			members.remove( user.ldapobject.dn )
#
#		if not members:
#			members = [ self._EMPTY_GROUP_VALUE ]
#
#		self._set_attribute( 'member', members )
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ||| || ||| || ||| || ||| || ||| || ||| || ||| || ||| || ||| || ||| || ||| || |
# ==============================================================================


	@classmethod
	def get_groups( self, scheme, name = None, guid = None ):
		"""
		"""
		config = scheme.config

		filter = '(objectClass=%s)' % config.get_attribute( 'group_class' )[-1]

		users_in_group = config.get_attribute( 'users_in_group' )

		if name:
			filter += '(%s=%s)' %( config.get_attribute( 'group_name'), name )
		if guid:
			filter += '(%s=%s)' %( config.get_attribute( 'group_guid' ), self._modify_dn( guid ) )

		filter = '(&' + filter + ')'


		group_dn = config.get_attribute( 'group_dn' )

		if group_dn:
			search_location = '%s,'% group_dn + scheme.get_option( 'base_dn' )
		else:
			search_location = '%s'% scheme.get_option( 'base_dn' )

		groups = scheme.userconnection().search( search_location, filter, True )

		result = [ LDAPGroup( scheme, ldapobject = group ) for group in groups ]

		# we experimenting with limited ldap attributes mapping
		try:
			result.sort( cmp=lambda a,b: cmp( a.name.lower(), b.name.lower() ) )
		except:
			pass

		return Group.get_groups( scheme, name, guid ) + result


	def get_users( self ):
		"""
		"""
		# get users if user_dn stores in group object
		config = self.scheme.config

		#group.users
		users_in_group = config.get_attribute( 'users_in_group' )
		if users_in_group:
			result = []
			user_dns = self.ldapobject.attributes.get( users_in_group, [] )
			for dn in user_dns:
				if self._scalar( dn ) != self._EMPTY_GROUP_VALUE:
					ldapuser = self.scheme.userconnection().get_by_dn( self._scalar( dn ) )
					if ldapuser:
						user = LDAPUser( scheme = self.scheme, ldapobject = ldapuser )
						result.append( user )

			# we experimenting with limited ldap attributes mapping
			try:
				result.sort( cmp=lambda a,b: cmp(a.email.lower(), b.email.lower()) )
			except:
				pass

			return result

		# if group_dn stores in user object: get all users and check if each user belongs this group ( self )
		groups_in_user = config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			users = LDAPUser.get_users( self.scheme )
			result = []
			for user in users:
				group_dns = user.ldapobject.attributes.get( groups_in_user, [] )
				for dn in group_dns:
					if dn == self.ldapobject.dn:
						result.append( user )

			# we experimenting with limited ldap attributes mapping
			try:
				result.sort( cmp=lambda a,b: cmp(a.email.lower(), b.email.lower()) )
			except:
				pass

			return result

		return []



	def delete_user( self, user, force = False ):
		if self.is_admin() and not force:
			return

		# group.users
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' ) # group.users
		if users_in_group:
			if self._scalar( user.ldapobject.dn ) != self._EMPTY_GROUP_VALUE:
				self.ldapobject.attributes[ users_in_group ].remove( self._scalar( user.ldapobject.dn ) )
				self.save()
			return self

		# user.groups
		groups_in_user = self.scheme.config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			users = self.get_users()
			for user in users:
				user.delete_from_group( group = self, force = force )
			return self


	def add_empty_user( self ):
		users_in_group = self.scheme.config.get_attribute( 'users_in_group' )
		if users_in_group not in self.ldapobject.attributes:
			self.ldapobject.attributes[ users_in_group ] = []
		if not self.ldapobject.attributes[ users_in_group ]:
			self.ldapobject.attributes[ users_in_group ].append( self._EMPTY_GROUP_VALUE )

	def force_delete( self, force = True ):
		""" delete user
		"""
		if self.is_admin() and not force:
			return
		rules = self.scheme.application.child_rules( subject = self, recursive = True )
		for rule in rules:
			rule.delete()
		groups_in_user = self.scheme.config.get_attribute( 'groups_in_user' )
		if groups_in_user:
			users = self.get_users()
			for user in users:
				user.delete_from_group( group = self, force = force )
		self.scheme.userconnection().delete( self.ldapobject )


	def __eq__( self, other ):
		if not isinstance( other, LDAPGroup ): return False
		return self.ldapobject == other.ldapobject



