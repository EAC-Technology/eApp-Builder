#encoding: utf8

# version:	4

from xml.dom.minidom import getDOMImplementation, parseString
import cgi



class SimpleXMLError( Exception ):
	def __init__( self, *args ):
		Exception.__init__( self, "SimpleXML can't parse xml data.", args )





class SimpleXML( object ):
	""" functionality for generating xml from simple objects and restore objects from xml
	"""
	def __init__( self ):
		self.document	= getDOMImplementation().createDocument( None, 'xml', None )
		self.node		= self.document.createElement( 'list' )


# -----------------------------------------------------------------------
#		Create methods
# -----------------------------------------------------------------------

	def create_object( self, obj ):
		""" add object to xml
		"""
		if   type(obj) in [str, unicode]: return self.create_str( obj )
		elif type(obj) == list	: return self.create_list( obj )
		elif type(obj) == tuple	: return self.create_tuple( obj )
		elif type(obj) == dict	: return self.create_dict( obj )
		elif type(obj) in [int, long]	: return self.create_int( obj )
		elif type(obj) == bool	: return self.create_bool( obj )
		elif type(obj) == float	: return self.create_float( obj )
		elif obj	== None		: return self.create_none( obj )
		return None



	def create_list( self, list_obj ):
		""" create xml element for list
		"""
		if not isinstance( list_obj, list ):
			return

		list_xml = self.document.createElement( 'list' )

		for o in list_obj:
			elem = self.create_object( o )
			if elem:
				list_xml.appendChild( elem )

		return list_xml


	def create_tuple( self, tuple_obj ):
		""" create xml element for list
		"""
		if not isinstance( tuple_obj, tuple ):
			return

		tuple_xml = self.document.createElement( 'tuple' )

		for o in tuple_obj:
			elem = self.create_object( o )
			if elem:
				tuple_xml.appendChild( elem )

		return tuple_xml


	def create_dict( self, dict_obj ):
		""" create xml element for dict
		"""
		if not isinstance( dict_obj, dict ):
			return

		dict_xml = self.document.createElement( 'dict' )

		for key in dict_obj:
			value = self.create_object( dict_obj[ key ] )
			if value:
				elem_xml = self.document.createElement( 'element' )
				elem_xml.setAttribute( 'key', unicode(key) )
				elem_xml.appendChild( value )

				dict_xml.appendChild( elem_xml )

		return dict_xml


	def create_int( self, i ):
		""" create xml element for int
		"""
		if type(i) not in [ int, long ]:
			return

		value = self.document.createTextNode( str(i) )

		int_xml = self.document.createElement( 'int' )
		int_xml.appendChild( value )

		return int_xml


	def create_str( self, s ):
		""" create xml element for str
		"""
		if type(s) not in [ str, unicode ]:
			return

		value = self.document.createTextNode( s )

		str_xml = self.document.createElement( 'str' )
		str_xml.appendChild( value )

		return str_xml


	def create_bool( self, b ):
		""" create xml element for bool
		"""
		if not isinstance( b, bool ):
			return

		value = self.document.createTextNode( str(b).lower() )

		bool_xml = self.document.createElement( 'bool' )
		bool_xml.appendChild( value )

		return bool_xml


	def create_float( self, f ):
		""" create xml element for float
		"""
		if type(f) not in [ float ]:
			return

		value = self.document.createTextNode( str(f) )

		float_xml = self.document.createElement( 'float' )
		float_xml.appendChild( value )

		return float_xml



	def create_none( self, n ):
		""" create xml element for None
		"""
		return self.document.createElement( 'none' )



# -----------------------------------------------------------------------
#		Parse methods
# -----------------------------------------------------------------------

	def parse_object( self, dom ):
		"""
		"""
		if not dom:
			return None

		tag = dom.tagName.lower()

		if   tag == 'list'	: return self.parse_list( dom )
		elif tag == 'tuple'	: return self.parse_tuple( dom )
		elif tag == 'dict'	: return self.parse_dict( dom )
		elif tag == 'int'	: return self.parse_int( dom )
		elif tag == 'str'	: return self.parse_str( dom )
		elif tag == 'bool'	: return self.parse_bool( dom )
		elif tag == 'float'	: return self.parse_float( dom )

		elif tag == 'none'	: return None
		return None



	def parse_list( self, dom ):
		""" parse list xml structure
		"""
		if dom.tagName.lower() != 'list':
			return None

		result = []
		for node in dom.childNodes:
			if node.nodeType == self.document.TEXT_NODE: continue
			result.append( self.parse_object( node ) )

		return result


	def parse_tuple( self, dom ):
		""" parse list xml structure
		"""
		if dom.tagName.lower() != 'tuple':
			return None

		result = tuple()
		for node in dom.childNodes:
			if node.nodeType == self.document.TEXT_NODE: continue

			value = self.parse_object( node )
			if type(value) != list:
				value = [ value ]

			result += tuple( value )

		return result


	def parse_dict( self, dom ):
		""" parse dict xml structure
		"""
		if dom.tagName.lower() != 'dict':
			return None

		result = {}
		for node in dom.childNodes:
			if node.nodeType == self.document.TEXT_NODE: continue

			key = str( node.attributes[ 'key' ].value )
			result[ key ] = None

			for child in node.childNodes:
				if child.nodeType == self.document.TEXT_NODE: continue
				result[ key ] = self.parse_object( child )

		return result


	def parse_int( self, dom ):
		""" parse int xml structure
		"""

		if dom.tagName.lower() != 'int':
			return None

		for node in dom.childNodes:
			value = node.nodeValue.strip()
			if value:
				return int( value )



	def parse_str( self, dom ):
		""" parse str xml structure
		"""
		if dom.tagName.lower() != 'str':
			return None

		for node in dom.childNodes:
			value = node.nodeValue.strip()
			if value:
				return value

		# protection for empty string
		return ''




	def parse_bool( self, dom ):
		""" parse str xml structure
		"""
		if dom.tagName.lower() != 'bool':
			return None

		for node in dom.childNodes:
			value = node.nodeValue.strip()
			if value:
				return True if value.lower() == 'true' else False


	def parse_float( self, dom ):
		""" parse float xml structure
		"""

		if dom.tagName.lower() != 'float':
			return None

		for node in dom.childNodes:
			value = node.nodeValue.strip()
			if value:
				return float( value )


	def parse_none( self, dom ):
		""" parse None xml structure
		"""
		if dom.tagName.lower() != 'none':
			return None

		return None



# -----------------------------------------------------------------------
#		Class methods
# -----------------------------------------------------------------------

	@classmethod
	def dumps( self, obj ):
		""" create xml structure from objects
		"""
		result = self().create_object( obj )
		return result.toprettyxml() if result else ''



	@classmethod
	def loads( self, xml_data ):
		""" repair object from xml structure
		"""
		if not xml_data:
			return None

		try:
			dom = parseString( xml_data.encode('utf8') )
		except:
			raise SimpleXMLError( cgi.escape(xml_data) )

		return self().parse_object( dom.firstChild )





if __name__ == '__main__':
	test = {'1': (1.552000,), "3": [-15.686868]}
	xml = SimpleXML.dumps( test )

	print xml

	res = SimpleXML.loads( xml )
	print res, res == test

