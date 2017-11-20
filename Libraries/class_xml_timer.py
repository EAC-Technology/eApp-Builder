from xml.dom.minidom import Document
from vdom_xml_node import Node

class XMLTimer( Node ):
	def __init__( self, dom=None ):

		if dom == None:
			dom = Document()
			m = dom.createElement( 'timer' )
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
	def guid( self ):
		return self.find( 'guid' ).text

	@guid.setter
	def guid( self, value ):
		self.find( 'guid' ).text = value

	@property
	def period( self ):
		return self.find( 'period' ).text

	@period.setter
	def period( self, value ):
		self.find( 'period' ).text = value

	@property
	def plugin_guid( self ):
		return self.find( 'plugin_guid' ).text

	@plugin_guid.setter
	def plugin_guid( self, value ):
		self.find( 'plugin_guid' ).text = value
