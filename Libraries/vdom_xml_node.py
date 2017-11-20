class InvalidDomError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Incorrect argument. Wait link to DOM model of xml' )


class Node( object ):
	""" class represent node of xml and have hard link to dom model
	"""
	# --------------------------------------------------
	#		PYTHON OPERATORS
	# --------------------------------------------------

	def __init__( self, dom ):
		if not dom:
			raise InvalidDomError()

		# get dom structure from node element
		if isinstance( dom, Node ):
			dom = dom.dom

		# check may be node is document
		if dom.nodeType == dom.DOCUMENT_NODE:
			dom = dom.firstChild

		# save link to dom model
		self._dom = dom



	def __str__( self ):
		return 'Node( %s )' % self.tag



	def __del__( self ):
		""" remove this node and all subnodes
		"""
		return
		self.dom.parentNode.removeChild( self.dom )



	def __getitem__( self, key ):
		""" get attribute value by key
		"""
		# check type of key
		if type( key ) not in [ str, unicode ]:
			return None

		# find key,
		for k in self.keys():
			if k.lower() == key.lower():
				key = k
				break

		# return attribute by key
		attr = self.dom.getAttribute( key )
		return attr



	def __setitem__( self, key, value ):
		""" set attribute
		"""
		if type( value ) not in [ str, unicode ]:
			value = str( value )

		if type( key ) not in [ str, unicode ]:
			return

		self.dom.setAttribute( key, value )



	def __delitem__( self, key ):
		""" delete attribute
		"""
		if type( key ) not in [ str, unicode ]:
			return

		self.dom.removeAttribute( key )


	def __hash__( self ):
		s = ''
		s += self.tag.lower() + ':' + str( len( self.childs ) )
		s += ','.join( ['%s=%s' % (key.lower(), self[key],) for key in self.keys()] )
		s += self.value

		return hash( s )



	def isequal( self, other ):
		""" compare for equaling
		"""
		if not other: return False

		# check by dom objects - easyst way
		if self.dom.isSameNode( other.dom ): return True


		def compare_nodes( this, node ):
			""" compare self node and other
			"""
			return hash( this ) == hash( node )

		def compare_childs( this, node ):
			""" recursive comparing of lists of childs
			"""
			n = len( this.childs )

			this.childs.sort()
			node.childs.sort()

			# fast flat comparing
			index = range( n )
			for i in range( n ):
				obj1 = this.childs[ i ]

				for j in range( n ):
					if j not in index: continue
					obj2 = node.childs[ j ]

					if compare_nodes( obj1, obj2 ):
						index.remove( j )

			if index: return False

			# detailed comparing
			index = range( n )
			for i in range( n ):
				obj1 = this.childs[ i ]

				for j in range( n ):
					if j not in index: continue
					obj2 = node.childs[ j ]

					if obj1 == obj2:
						index.remove( j )

			if index: return False

			return True



		if not compare_nodes( self, other ):
			return False

		if not compare_childs( self, other ):
			return False


		return True






	def __eq__( self, other ):
		""" compare to equal
		"""
		return self.isequal( other )








	# --------------------------------------------------
	#		PROPERTIES
	# --------------------------------------------------

	# --- LINKS ---

	@property
	def dom( self ):
		""" property for read only dom link
		"""
		if not self._dom: return None
		return self._dom



	@property
	def document( self ):
		""" get hight document node of xml
		"""
		if self.dom.nodeType == self.dom.DOCUMENT_NODE:
			return self

		return self.dom.ownerDocument



	@property
	def root( self ):
		""" get root-node (top level container)
		"""
		return Node( self.document.firstChild )



	@property
	def parent( self ):
		""" return parent node structure
		"""
		parent = self.dom.parentNode

		if not parent:
			return None

		if parent == self.document:
			return None

		return self.create( parent )



	@property
	def path( self ):
		""" return list of nodes - path from root-node to this node
		"""
		path = []

		# go from self to root
		node = self
		while node:
			path.append( node )
			node = node.parent

		path.reverse()
		return path






	# --- NODE VALUES ---

	@property
	def tag( self ):
		""" return tag-name of this node
		"""
		ignore_node_types = [ self.dom.DOCUMENT_NODE, self.dom.TEXT_NODE, self.dom.CDATA_SECTION_NODE ]

		if self.dom.nodeType in ignore_node_types:
			return u''

		name = self.dom.tagName.strip()
		return name

	@tag.setter
	def tag( self, value ):
		if not value: return
		self.dom.tagName = value



	@property
	def text( self ):
		""" get text-value of this node
		"""
		data_dom = self.dom.firstChild

		if not data_dom:
			return u''

		if data_dom.nodeType != self.dom.TEXT_NODE:
			return u''

		return data_dom.nodeValue.strip()

	@text.setter
	def text( self, value ):
		""" set text-value of this node
		"""
		data_dom = self.dom.firstChild

		if data_dom and data_dom.nodeType == self.dom.CDATA_SECTION_NODE:
			self.dom.removeChild( data_dom )

		data_dom = self.dom.firstChild

		if not data_dom:
			data_dom = self.dom.appendChild( self._create_text_node_dom() )

		data_dom.nodeValue = value



	@property
	def cdata( self ):
		""" property get text node data
		"""
		data_dom = self.dom.firstChild
		if not data_dom:
			return u''

		if data_dom.nodeType != self.dom.CDATA_SECTION_NODE:
			return u''

		return data_dom.nodeValue

	@cdata.setter
	def cdata( self, value ):
		""" set text-node data
		"""
		data_dom = self.dom.firstChild

		if data_dom and data_dom.nodeType == self.dom.TEXT_NODE:
			self.dom.removeChild( data_dom )

		data_dom = self.dom.firstChild

		if not data_dom:
			data_dom = self.dom.appendChild( self._create_cdata_node_dom() )

		data_dom.nodeValue = value



	@property
	def value( self ):
		text = self.text
		if text: return text

		cdata = self.cdata
		if cdata: return cdata

		return u''

	@value.setter
	def value( self, value ):
		data_dom = self.dom.firstChild
		if data_dom and data_dom.nodeType == self.dom.CDATA_SECTION_NODE:
			self.cdata = value
			return

		self.text = value









	@property
	def childs( self ):
		""" return list of subnodes or empty list
		"""
		# node types that ignore like childs
		ignore_node_types = [ self.dom.TEXT_NODE, self.dom.CDATA_SECTION_NODE ]
		result = []

		for node in self.dom.childNodes:
			if node.nodeType in ignore_node_types:
				continue
			result.append( self.create( node ) )

		return result






	# --------------------------------------------------
	#		METHODS
	# --------------------------------------------------

	def save( self, writer ):
		""" save changes to file
		"""
		self.dom.writexml( writer )



	def delete( self ):
		""" remove this node from tree
		"""
		if not self.parent:
			return None

		if self.parent:
			self.parent.remove_child( self )

		return self



	def _add_prefix_indent( self ):
		"""
		"""
		# add indend
		indent = '\n' + '\t' * len( self.path )
		self.dom.appendChild( self._create_text_node_dom( indent ) )



	def append_child( self, node ):
		""" add node to subnodes
		"""
		self._add_prefix_indent()

		# add child
		self.dom.appendChild( node.dom )

		return node



	def _remove_prefix_indent( self, node ):
		""" remove indent-text-node from xml
		"""
		# check index bound
		bound = lambda index: index >= 0 and index < len( self.dom.childNodes )

		index = self.dom.childNodes.index( node.dom )
		if bound( index ):
			index -= 1 # get index of prefix node

		if bound( index ):
			indent = self.dom.childNodes[ index ]
			if indent and indent.nodeType == self.dom.TEXT_NODE:
				self.dom.removeChild( indent )



	def remove_child( self, node ):
		""" remove child node from subnodes
		"""
		self._remove_prefix_indent( node )
		self.dom.removeChild( node.dom )
		return node



	def keys( self ):
		""" attributes keys
		"""
		keys = self.dom.attributes.keys()
		keys.sort()
		return keys



	# --------------------------------------------------
	#		FIND-METHODS
	# --------------------------------------------------

	def find( self, obj, recursive=False, comparer=None ):
		""" find one in childs combaine
		"""
		if not obj: return None

		result = self.find_all( obj, recursive, one=True, comparer=comparer )
		if not result: return None

		return self.create( result[ 0 ] )



	def find_all( self, obj, recursive=False, one=False, comparer=None ):
		""" find all in childs
			recursive - enable finding in tree deep
			one - try to find single resultat
			comparer - function with two arguments. determine compare rules for node and other objects. return True or False
		"""
		if not obj: return []

		# define default comparers for different objects
		def tag_comparer( node, tag ):
			""" compare tag name
			"""
			return node.tag == tag

		def node_comparer( node1, node2 ):
			""" compare nodes
			"""
			return node1.isequal( node2 )


		# set default comparer if comparer not setted
		if not comparer:
			# text
			if type( obj ) in [ str, unicode ]:
				comparer = tag_comparer

			# node
			if isinstance( obj, Node ):
				comparer = node_comparer


		# get results
		result = []

		for node in self.childs:
			if comparer( node, obj ):
				result.append( node )

			if one and result:
				return result

			if recursive:
				result += node.find_all( obj, recursive, one, comparer )

		return [ self.create( n ) for n in result ]



	def find_in_dom( self, dom, comparer=None ):
		""" find this structure in another dom
		"""
		node = Node( dom )
		result = node.find( self, recursive=True, comparer=comparer )

		# modify type of result
		return self.create( result )









	# --------------------------------------------------
	#		CREATE-METHODS
	# --------------------------------------------------

	def create_empty_node( self, tag='' ):
		""" create empty node
		"""
		dom = self.document.createElement( tag )

#		# create separator
#		text = self._create_text_node_dom()
#		text.nodeValue = '\n'
#		dom.apeendChild( text )

		return Node( dom )



	def _create_cdata_node_dom( self, value='' ):
		return self.document.createCDATASection( value )

	def _create_text_node_dom( self, value='' ):
		return self.document.createTextNode( value )




	def clone( self, deep=True ):
		""" clone this node
		"""
		dom = self.dom.cloneNode( deep )
		return self.create( dom )



	def clear( self ):
		""" clear attributes, value, childs, etc
		"""
		#clear tag
		self.tag = ' '

		# clear attributes
		for key in self.keys():
			del self[ key ]

		# clear childs
		for node in self.childs:
			self.remove_child( node )

		return self



	def create_child( self, tag ):
		""" create new child node
		"""
		child = self.childs[0].clone(False) if self.childs else self.create_empty_node()
		child.clear()

		child.tag = tag
		self.append_child( child )

		return child



	def base_node( self ):
		""" create instance of base node from self
		"""
		return Node( self )



	@classmethod
	def create( self, obj ):
		""" create new instance from dom or node.
			Need in child classes
		"""
		if not obj: return None
		return Node( obj )









	# --------------------------------------------------
	#		PRINT-METHODS
	# --------------------------------------------------

	def toxml( self ):
		""" return string representation of xml
		"""
		return self.dom.toxml()

	def toprettyxml( self ):
		""" return pretty representation with tabs and whitespaces
		"""
		return self.dom.toprettyxml()


def append_cdata(doc, parent, data):
    start = 0
    while True:
        i = data.find("]]>", start)
        if i == -1:
            break
        parent.appendChild(doc.createCDATASection(data[start:i+2]))
        start = i + 2
    parent.appendChild(doc.createCDATASection(data[start:]))
