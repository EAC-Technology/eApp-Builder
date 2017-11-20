from xml.dom.minidom import Document
from vdom_xml_node import Node

class XMLResource( Node ):
	def __init__( self, dom=None ):

		if dom == None:
			dom = Document()
			m = dom.createElement( 'resource' )
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
	def res_source( self ):
		return self.find( 'res_source' ).text

	@res_source.setter
	def res_source( self, value ):
		self.find( 'res_source' ).text = value
