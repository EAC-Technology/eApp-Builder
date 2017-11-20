import ldif
from StringIO import StringIO


class LDAPIncorrectDN( Exception ):
	""" Exception in dn data in init of ldap object
	"""
	def __init__( self ):
		Exception.__init__( self, 'Incorrect DN data' )


class LDAPObject:
	def __init__(self, dn, attributes):
		"""
		"""
		# tree nodes of this LDAP object
		self._nodes = []
		self.set_dn( dn )

		# object attributes
		self.attributes = attributes


	def get_dn( self ):
		""" get dn-string of this LDAP object
		"""
		return unicode( ",".join( self._nodes ) )

	def set_dn( self, dn ):
		""" set dn. It can be list of nodes, or string.
		"""
		# fill nodes from dn
		if type( dn ) in [ unicode ]:
			self._nodes = dn.split( ',' )
		elif type( dn ) in [ str ]:
			self._nodes = dn.decode( 'utf8' ).split( ',' )
		elif type( dn ) in [ list, tuple ]:
			self._nodes = ",".join( dn ).split( "," )
		else:
			raise LDAPIncorrectDN()


	def get_rdn( self ):
		return unicode( ",".join( self._nodes[:1] ) )

	def set_rdn( self, value ):
		"""
		"""
		self._nodes[0] = value


	def get_parent_dn(self):
		return unicode( ",".join( self._nodes[1:] ) )


	def get_ldif( self, mod_attrs=None ):
		""" get ldif of ldap object
		"""
		output = StringIO()

		if not mod_attrs:
			mod_attrs = self.attributes

		writer = ldif.LDIFWriter( output )
		writer.unparse( self.dn, mod_attrs )

		result = output.getvalue()
		output.close()

		return result


	dn 			= property( get_dn, set_dn )
	rdn 		= property( get_rdn, set_rdn )
	parent_dn 	= property( get_parent_dn )


	def __eq__( self, other ):
		if not other: return False
		return 	self.attributes == other.attributes	and self.dn == other.dn

	def __str__( self ):
		return str( self.dn ) + str( self.attributes )
