import ldap
import ldap.modlist as modlist
import shlex
from subprocess import Popen, PIPE
from proadmin_ldap_object import LDAPObject


class LDAPConnection( object ):
	""" wraper for LDAP routines
	"""
	def __init__( self, editable = True ):
		self.editable = editable

		self.host 		= ''
		self.user_dn 	= ''
		self.passwd		= ''
		self.port 		= 389

		self.connection = None



	def bind( self, host, dn, passwd ):
		""" connect to ldap server
		"""
		self.host 		= host
		self.user_dn 	= dn
		self.passwd		= passwd

		self.rebind()



	def rebind( self ):
		try:
			self.unbind()
		except:
			pass

		self.connection = ldap.open( self._encode(self.host), port=self.port )
		self.connection.simple_bind_s( self._encode(self.user_dn), self._encode(self.passwd) )



	def unbind( self ):
		""" close connection
		"""
		if self.connection:
			self.connection.unbind()



	@classmethod
	def try_bind( self, host, user_dn, password ):
		""" try connect to LDAP server
		"""
		conn = None

		try:
			conn = self()
			conn.bind( host, user_dn, password )
			return True

		except:
			pass

		finally:
			if conn: conn.unbind()

		return False



	def exists( self, ldap_object ):
		""" check that ldap object exists in LDAP base
		"""
		return False if not self.search( basedn = ldap_object.parent_dn, filter = ldap_object.rdn, recursive = True ) else True



	def save( self, ldapobject ):
		""" save node - insert or update if node exists
		"""
		if not self.editable:
			return
		if not self.exists( ldapobject ):
			self.insert( ldapobject = ldapobject )
		else: # self.exists( ldapobject ):
			self.update( ldapobject = ldapobject )



	def insert( self, ldapobject ):
		""" insert to LDAP tree
		"""
		if not self.editable:
			return

		dn 			= self._encode( ldapobject.dn )
		attributes 	= self._encode( ldapobject.attributes )

		ldif = modlist.addModlist( attributes )

		self.connection.add_s( dn, ldif )




	def update( self, ldapobject ):
		""" update node in LDAP tree
		"""
		if not self.editable:
			return
		dn 			= self._encode( ldapobject.dn )
		attributes 	= self._encode( ldapobject.attributes )

		mod_attrs = []
		for attr_name, attr_value in attributes.iteritems():
			mod_attrs.append((ldap.MOD_REPLACE, attr_name, attr_value))

		object = self.get_by_dn( dn )
		if not object:
			return

		for attr_name, attr_value in object.attributes.iteritems():
			if attr_name not in ldapobject.attributes:
				mod_attrs.append((ldap.MOD_DELETE, attr_name, None))

		self.connection.modify_s( dn, mod_attrs )



	def _ldapmodify( self, ldif ):
		""" implementation of ldap_modify function with using system command
		"""
		cmd = """/usr/local/bin/ldapmodify -h 127.0.0.1 -x -D 'cn=admin,dc=vdombox,dc=local' -w 'passwd'"""

		# create subproccess and call ldapmodify
		p = Popen( shlex.split( cmd.encode( 'utf8' ) ), stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1, close_fds=True )
		result = p.communicate( input=ldif )

		del result
		del p



	def search( self, basedn, filter, recursive = False ):
		""" search in LDAP tree
		"""
		basedn 	= self._encode( basedn )
		filter	= self._encode( filter )

		searchScope = ldap.SCOPE_SUBTREE if recursive else ldap.SCOPE_ONELEVEL
		retrieveAttributes = None

		result_set = []
		try:
			
			# try to get result, if some exception rebind to ldap and try search again
			ldap_result_id = None
			try:
				ldap_result_id = self.connection.search( basedn, searchScope, filter, retrieveAttributes )
			except:
				self.rebind()
				ldap_result_id = self.connection.search( basedn, searchScope, filter, retrieveAttributes )


			result_type, result_data = self.connection.result( ldap_result_id, 1 )		
			result_data = result_data or []

			for item in result_data:
				dn 			= self._decode( item[0] )
				attributes	= self._decode( item[1] )

				ldap_object = LDAPObject( dn, attributes )
				result_set.append( ldap_object )


			# result_type, result_data = self.connection.result( ldap_result_id, 0 )

			# while result_data:
			# 	if result_type == ldap.RES_SEARCH_ENTRY:

			# 		dn 			= self._decode( result_data[0][0] )
			# 		attributes	= self._decode( result_data[0][1] )

			# 		ldap_object = LDAPObject( dn, attributes )
			# 		result_set.append( ldap_object )

			# 	result_type, result_data = self.connection.result( ldap_result_id, 0 )


			return result_set

		except ldap.LDAPError, e:
			return result_set



	def delete( self, ldapobject ):
		""" delete ldap object
		"""
		if not self.editable:
			return

		dn = self._encode( ldapobject.dn )

		result = self.search( dn, "objectClass=*", True )
		sorted_result = sorted( result, cmp=lambda x,y: cmp(len(y.dn.split(',')), len(x.dn.split(','))))

		for o in sorted_result:
			o_dn = self._encode( o.dn )
			self.connection.delete_s( o_dn )


	def create_object( self, dn, attributes ):
		return LDAPObject( dn, attributes )



	def get_by_dn( self, dn ):
		""" get ldap object by DN
		"""
		obj = LDAPObject( dn, None )
		result = self.search( obj.parent_dn, obj.rdn, recursive=False )
		return result[0] if result else None




	def _encode( self, obj ):
		""" encode structure to utf-8
		"""
		if type( obj ) == unicode:
			return obj.encode( 'utf8' )

		elif type( obj ) == list:
			return [ self._encode( o ) for o in obj ]

		elif type( obj ) == dict:
			result = {}
			for k in obj:
				try:
					result[ self._encode(k) ] = self._encode( obj[ k ] )
				except:
					continue
			return result


		else:
			return obj


	def _decode( self, obj ):
		""" decode structure to unicode
		"""
		if type( obj ) == str:
			return obj.decode( 'utf8' )

		elif type( obj ) == list:
			return [ self._decode( o ) for o in obj ]

		elif type( obj ) == dict:
			result = {}
			for k in obj:
				try:
					result[ self._decode(k) ] = self._decode( obj[ k ] )
				except:
					continue
			return result

		else:
			return obj
