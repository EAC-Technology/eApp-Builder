from xml.dom.minidom import Document
from vdom_xml_node import Node

class XMLMacros( Node ):
	def __init__( self, dom=None ):

		if dom == None:
			dom = Document()
			m = dom.createElement( 'macro' )
			dom.appendChild( m )

		Node.__init__( self, dom )


	def find( self, obj, recursive=False,  comparer=None ):
		result = Node.find( self, obj, recursive, comparer )

		if type(obj) not in [ str, unicode ]:
			return result

		if not result:
			result = self.create_child( obj )

		return result


	@property
	def source( self ):
		return self.find( 'source' ).text #or self.find( 'source' ).cdata

	@source.setter
	def source( self, value ):
		self.find( 'source' ).text = value

	@property
	def name( self ):
		return self.find( 'name' ).text

	@name.setter
	def name( self, value ):
		self.find( 'name' ).text = value

	@property
	def class_name( self ):
		return self.find( 'class_name' ).text

	@class_name.setter
	def class_name( self, value ):
		self.find( 'class_name' ).text = value

	@property
	def is_button( self ):
		return self.find( 'is_button' ).text

	@is_button.setter
	def is_button( self, value ):
		self.find( 'is_button' ).text = value


	@property
	def on_board( self ):
		return self.find( 'ob_board' ).text

	@on_board.setter
	def on_board( self, value ):
		self.find( 'ob_board' ).text = value

	@property
	def macros_picture( self ):
		return self.find( 'macros_picture' ).text

	@macros_picture.setter
	def macros_picture( self, value ):
		self.find( 'macros_picture' ).text = value

	@property
	def guid( self ):
		return self.find( 'guid' ).text

	@guid.setter
	def guid( self, value ):
		self.find( 'guid' ).text = value

	@property
	def description( self ):
		return self.find( 'description' ).text

	@description.setter
	def description( self, value ):
		self.find( 'description' ).text = value

	@property
	def timer_guid( self ):
		return self.find( 'timer_guid' ).text

	@timer_guid.setter
	def timer_guid( self, value ):
		self.find( 'timer_guid' ).text = value

	@property
	def custom_event_guid( self ):
		return self.find( 'custom_event_guid' ).text

	@custom_event_guid.setter
	def custom_event_guid( self, value ):
		self.find( 'custom_event_guid' ).text = value

	@property
	def plugin_guid( self ):
		return self.find( 'plugin_guid' ).text

	@plugin_guid.setter
	def plugin_guid( self, value ):
		self.find( 'plugin_guid' ).text = value

	@property
	def page( self ):
		return self.find( 'page' ).text

	@page.setter
	def page( self, value ):
		self.find( 'page' ).text = value


	@property
	def type(self):
		return self.find('type').text


	@type.setter
	def type(self, value):
		self.find('type').text = value


