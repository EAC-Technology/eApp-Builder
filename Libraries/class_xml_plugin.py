from xml.dom.minidom import Document
from vdom_xml_node import Node

class XMLPlugin( Node ):
	def __init__( self, dom=None ):

		if dom == None:
			dom = Document()
			m = dom.createElement( 'plugin' )
			dom.appendChild( m )

		Node.__init__( self, dom )


	def find( self, key, recursive=False, comparer=None ):
		return self[key] if key in self.keys() else ""


	@property
	def name( self ):
		return self.find( 'name' )

	@name.setter
	def name( self, value ):
		self['name'] = value

	@property
	def guid( self ):
		return self.find( 'guid' )

	@guid.setter
	def guid( self, value ):
		self['guid'] = value

	@property
	def description( self ):
		return self.find( 'description' )

	@description.setter
	def description( self, value ):
		self['description'] = value

	@property
	def picture( self ):
		return self.find( 'picture' )

	@picture.setter
	def picture( self, value ):
		self['picture'] = value

	@property
	def version( self ):
		return self.find( 'version' )

	@version.setter
	def version( self, value ):
		self['version'] = value

	@property
	def author( self ):
		return self.find( 'author' )

	@author.setter
	def author( self, value ):
		self['author'] = value

	@property
	def protected( self ):
		return self.find( 'protected' )

	@protected.setter
	def protected( self, value ):
		self['protected'] = value


