from proadmin_ldap_connection import LDAPConnection
from proadmin_ldap_object import LDAPObject

import uuid as uuid
import cgi

class ACLObject( object ):

	def __init__( self, ldapobject, scheme ):
		self.ldapobject 	= ldapobject
		self.scheme			= scheme


	def _scalar( self, atr_name, default_value=None ):
		""" return scalar LDAP attribute value
		"""
		vector = self._vector( atr_name, [] )
		return vector[0] if vector else default_value

	def _vector( self, atr_name, default_value=[] ):
		""" return vector LDAP attribute value
		"""
		attr = self.ldapobject.attributes
		return attr[ atr_name ] if atr_name in attr else default_value

	def _set_attribute( self, name, value ):
		if not value: value = []
		else:
			if type( value ) != list:
				value = [ value ]

		self.ldapobject.attributes[ name ] = value



	# -----------------------------
	#		dirty-bit methods
	# -----------------------------

	def _get_dirty_bit( self ):
		value = self._scalar( 'documentVersion', 0 )
		if not value:
			value = 0

		return int( value )


	def _set_dirty_bit( self ):
		dirty_bit = self._get_dirty_bit()
		value = '0' if dirty_bit < 0 else '1'
		self._set_attribute( 'documentVersion', value )


	def is_dirty( self ):
		dirty_bit = self._get_dirty_bit()
		return True if dirty_bit > 0 else False


	def clear_dirty_bit( self ):
		self._set_attribute( 'documentVersion', '-1' )





	def get_type( self ):
		return self._scalar( 'cn' )


	def get_guid( self ):
		return self._scalar( 'documentIdentifier' )

	def set_guid( self, guid ):
		# modify attributes
		self._set_attribute( 'documentIdentifier', guid )

		# modify dn
		if guid and type(guid) in [str, unicode]:
			baseDN = self.ldapobject.parent_dn
			self.ldapobject.dn = "documentIdentifier=" + guid + ',' + baseDN
			self.ldapobject.rdn = "documentIdentifier=" + guid



	def get_name( self ):
		return self._scalar( 'documentTitle', '' )

	def set_name( self, value ):
		value = cgi.escape( value )
		self._set_attribute( 'documentTitle', value )




	def get_rules_tuples( self ):
		"""
		"""
		result = []

		strings = self._vector( 'description' )
		for s in strings:
			s_guid 		= s.split(',')[0]
			s_access	= s.split(',')[1]

			result.append( (s_guid, s_access) )

		return result


	def get_parent( self ):
		ldapconnection 	= self.scheme.connection
		ldapobject 		= ldapconnection.get_by_dn(self.ldapobject.parent_dn)

		acl_object = ACLObject( ldapobject, self.scheme )
		if acl_object.type == 'Application':
			return ACLApplication( ldapobject, self.scheme )

		return acl_object


	type 	= property( get_type )
	guid 	= property( get_guid, set_guid )
	name 	= property( get_name, set_name )
	parent 	= property( get_parent )



	def delete( self, parent_dirty=True ):
		# mark dirty-bit in parent object
		if parent_dirty and self.parent:
			self.parent.save()

		# remove ldap-object
		ldapconnection = self.scheme.connection
		ldapconnection.delete( self.ldapobject )


	def create_child( self, type, name, guid = '' ):

		baseDN = self.ldapobject.dn

		if not guid:
			guid = str( uuid.uuid4() )

		ldapconnection = self.scheme.connection

		child = ldapconnection.create_object(
					[ "documentIdentifier=" + guid, baseDN ],
					{
						'objectClass': [ 'top', 'document' ],
						'cn': [ type ],
						'documentIdentifier' : [ guid ],
						'documentTitle': [ name ]
					} )

		return ACLObject( child, self.scheme )




	def get_by_guid( self, guid ):
		""" search ACL object by guid in subtree include this object
		"""
		if not guid: return None
		if guid == self.guid:
			return self

		objects = self.child_objects( guid=guid, recursive=True )
		if objects:
			return objects[ 0 ]

		return None



	def child_objects(self, guid=None, type=None, name=None, recursive=None):
		""" return list of child objects
		"""

		if not guid: guid = ''
		if not type: type = ''
		if not name: name = ''
		if not recursive: recursive = False

		filter = ''

		if type:
			filter += "(cn=%s)" % type
		if guid:
			filter += "(documentIdentifier=%s)" % guid
		if name:
			filter += "(documentTitle=%s)" % name

		if not( type and guid and name ):
			filter += "(documentIdentifier=*)"

		filter = '(&' + filter + ')'

		ldapconnection = self.scheme.connection
		child_list = ldapconnection.search(self.ldapobject.dn, filter, recursive)

		result = []
		for child in child_list:
			if self.ldapobject.dn != child.dn:
				result.append( ACLObject( child, self.scheme ))

		result.sort( cmp=lambda a,b: cmp(a.name, b.name) )
		return result



	def rules( self, subject=None, access=None ):
		""" return list of rules of this object
		"""
		from proadmin_rule import Rule
		return Rule.get_rules( object=self, subject=subject, access=access )



	def child_rules( self, objecttype=None, subject=None, access=None, recursive=False ):
		"""
		"""

		if not objecttype	: objecttype 	= ''
		if not recursive	: recursive 	= ''
		if not subject		: subject 		= []
		if not access		: access		= []

		#get all need child objects
		childs = self.child_objects( type=objecttype, recursive=recursive )

		#get all need rules for it's objects
		result = []
		for c in childs:
			result += c.rules( subject=subject, access=access )

		return result



	def fast_rules( self, *args, **kwargs ):
		from proadmin_rule import Rule
		return Rule.fast_rules( self, *args, **kwargs )



	def add_rule( self, subject, access ):
		if "description" not in self.ldapobject.attributes:
			self.ldapobject.attributes["description"] = []

		rule = subject.guid + "," + access
		if rule not in self.ldapobject.attributes["description"]:
			self.ldapobject.attributes["description"].append( rule )


	def remove_rule( self, subject, access ):
		""" remove rules but can't remove admins rights
		"""
		return self.force_remove_rule( subject, access, force=False )


	def force_remove_rule( self, subject, access, force=True ):
		""" can remove rights for root!
		"""
		if not subject: return

		if "description" not in self.ldapobject.attributes:
			self.ldapobject.attributes["description"] = []

		rule = subject.guid + "," + access
		if rule in self.ldapobject.attributes["description"]:
			self.ldapobject.attributes["description"].remove( rule )






	@classmethod
	def application( self, name, guid, scheme ):
		ldapconnection = scheme.connection

		# create organization unit
		baseDN = "dc=vdombox,dc=local"
		baseou = ldapconnection.create_object(
					["ou=" + guid, baseDN],
					{
						'objectClass': ['top', 'organizationalUnit'],
						'ou': [ guid ]
					})

		ldapconnection.save( baseou )
		

		# create application document object
		userou = ldapconnection.create_object(
					["ou=users,ou=" + guid, baseDN],
					{
						'objectClass': ['top', 'organizationalUnit'],
						'ou': ['users', guid]
					})

		ldapconnection.save( userou )


		# get application document or create
		dn = "documentIdentifier={0},ou={0},{1}".format( guid, baseDN )
		document = ldapconnection.get_by_dn( dn )

		if not document:
			document = ldapconnection.create_object(

					["documentIdentifier=" + guid + ",ou=" + guid, baseDN],
					{
						'objectClass': ['top', 'document'],
						'documentIdentifier': [ guid ],
						'cn': ['Application'],
						'documentTitle': [ name ]
					})

		ldapconnection.save( document )

		return ACLApplication( document, scheme )




	def _exist( self ):
		objects = self.scheme.application.get_by_guid( guid = self.guid )
		return True if objects else False


	def save( self ):
		# set dirty-bit
		self._set_dirty_bit()

		ldapconnection = self.scheme.connection
		if self._exist():
			ldapconnection.update( self.ldapobject )
		else:
			ldapconnection.insert( self.ldapobject )
		return self


	def __eq__( self, other ):
		if not other: return False
		return self.ldapobject == other.ldapobject

	def __hash__( self ):
		return hash( self.guid )

	def __str__( self ):
		return "ACLObject: (Type: " + self.type + ", Name: " + self.name + ")"






class ACLApplication( ACLObject ):
	""" class represent ACLApplication
	"""
	def get_parent(self):
		return None

	parent = property(get_parent)

	def delete(self):
		import ProAdmin
		ldapconnection = self.scheme.connection
		ldapconnection.delete( ldapconnection.get_by_dn(self.ldapobject.parent_dn) )
		ProAdmin.unregister_default_scheme()


	def refresh( self ):
		""" refresh ldapobject
		"""
		dn = self.ldapobject.dn
		self.ldapobject = self.scheme.connection.get_by_dn( dn )


	def get_subjects( self, guid=None ):
		users = self.get_users( guid=guid )
		groups = self.get_groups( guid=guid )
		return users + groups

	def get_subject( self, guid ):
		result = self.get_subjects( guid=guid )
		return result[0] if result else None


	def create_user(self, email=''):
		""" create new application user
		"""
		users = self.get_users( email = email )
		if users: return users[0]

		user = self.scheme.create_user()
		user.email = email

		return user


	def create_root_user( self, password='root' ):
		""" create root user if not exists. root-is default password
		"""
		root = self.scheme.create_root_user()
		if not self.rules( root, 'a' ):
			self.add_rule( root, 'a' )
			self.save()


	def get_users( self, email=None, guid=None ):
		""" get application users
		"""
		return self.scheme.get_users( email = email, guid = guid )



	def create_group( self, name ):
		""" create new application group
		"""
		groups = self.get_groups( name = name )
		if groups: return groups[0]

		group = self.scheme.create_group( name = name )
		#group.name = name

		return group



	def create_admins_group( self ):
		""" create admin group if not exists
		"""
		admins = self.scheme.create_admins_group()
		if not self.rules( admins, 'a' ):
			self.add_rule( admins, 'a' )
			self.save()




	def get_groups( self, name=None, guid=None, user=None ):
		""" get application groups
		"""
		return self.scheme.get_groups( name=name, guid=guid, user=user )


	def get_admin( self ):
		"""get application admin user
		"""
		return self.scheme.get_admin()



	def force_remove_rule( self, subject, access, force=True ):
		""" special remove for application.
		"""
		if not subject: return

		if subject.is_admin() and access == 'a' and not force:
			return

		ACLObject.force_remove_rule( self, subject, access, force )
