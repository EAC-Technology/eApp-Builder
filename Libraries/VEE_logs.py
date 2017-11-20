from datetime import datetime



class LogMessage( object ):

	def __init__( self, name, message  ):
		self.__message 	= message
		self.date	 	= datetime.now()
		self.name 		= name


	message = property( lambda self: self.__message )


	def displayed_message( self ):
		return u"[{name}] :: {msg}".format( name = self.name, msg = self.message )



class EngineMessage( LogMessage ):

	def __init__( self, message ):
		LogMessage.__init__( self, u"Engine", message )


class CompilerMessage( LogMessage ):

	def __init__( self,  name, message, plugin_guid, macros_guid ):
		LogMessage.__init__( self, "Compiler: "+name, message )
		self.plugin_guid 	= plugin_guid
		self.macros_guid 	= macros_guid
		

class PluginMessage( LogMessage ):

	def __init__( self,  name, message, plugin_guid, macros_guid ):
		LogMessage.__init__( self, name, message )
		self.plugin_guid 	= plugin_guid
		self.macros_guid 	= macros_guid



class PluginMessageError( PluginMessage ):
	pass