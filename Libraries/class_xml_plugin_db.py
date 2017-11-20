from xml.dom.minidom import Document
from vdom_xml_node import Node

class XMLPluginDB( Node ):
	def __init__( self, dom=None ):

		if dom == None:
			dom = Document()
			m = dom.createElement( 'database' )
			dom.appendChild( m )

		Node.__init__( self, dom )


	def find( self, obj, recursive=False, comparer=None ):
		result = Node.find( self, obj, recursive, comparer )

		if type(obj) not in [ str, unicode ]:
			return result

		if not result:
			result = self.create_child( obj )

		return result


	@property
	def name( self ):
		return self.find( 'name' ).text

	@name.setter
	def name( self, value ):
		self.find( 'name' ).text = value

	@property
	def db_source( self ):
		return self.find( 'db_source' ).text

	@db_source.setter
	def db_source( self, value ):
		self.find( 'db_source' ).text = value
