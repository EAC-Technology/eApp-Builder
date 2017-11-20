#23.01.2013
#refactor events structure
#23.05.2013
# added set_folder to VEE_DeleteFolderSmartFolder
from VEE_utils import AutoCast, AutoCastCachedProperty, v_PropertyReadOnly
from VEE_std_lib import v_timer
from VEE_proadmin import v_proadmin
#from promail_wrappers import MailboxWrapper, MailWrapper, ArchiveWrapper
#import ProMail



#Base class for all events
class VEE_AbstractEvent( object ):

	def activate( self ):
		from VEE_core import engine
		engine.put_event( self )
#		engine.info( "Event '{className}' has occured".format(
#						className = self.__class__.__name__[4:] ) )


	@classmethod
	def get_key( self, key = None):
		return hash( self.__name__ if not key else key )


	@AutoCastCachedProperty
	def v_name( self ):
		return self.__class__.__name__[4:]


	def __hash__( self ):
		return hash( self.__class__.__name__ )



class VEE_TimerEvent( VEE_AbstractEvent ):

	def __init__( self, timer ):
		self.timer = v_timer( timer )


	def __hash__( self ):
		return hash( self.timer.timer.hash_value )



class VEE_ButtonEvent( VEE_AbstractEvent ):

	def __init__( self, namespace, macros_guid ):
		self.namespace = namespace
		self.macros_guid = macros_guid


	def activate( self ):
		raise NotImplementedError


	def __hash__( self ):
		return self.get_key( self.namespace, self.macros_guid )


	@classmethod
	def get_key( self, namespace, macros_guid ):
		return hash( "{0}:{1}".format( namespace, macros_guid ) )



class VEE_StartEngineEvent( VEE_AbstractEvent ):
	pass



class VEE_StopEngineEvent( VEE_AbstractEvent ):
	pass



#Base class for applications events (except TimerEvent)
class VEE_BaseAbstractEvent( VEE_AbstractEvent ):

	def __init__( self ):
		self._user = v_proadmin.v_currentuser()


	def get_user( self ):
		return self._user


	user = property( get_user )




class VEE_CustomEvent( VEE_AbstractEvent ):

	def __init__( self, plugin_guid = None, name = None ):
		VEE_AbstractEvent.__init__( self )
		self.name = ""
		self.plugin_guid = ""
		self.data = None


	def __hash__( self ):
		return self.get_key( self.plugin_guid, self.name )


	@classmethod
	def get_key( self, plugin_guid, name ):
		return hash( "{0}:{1}".format( plugin_guid, name ) )



#class VEE_IncomingEmail( VEE_BaseAbstractEvent ):
#
#	def __init__( self, email ):
#		VEE_BaseAbstractEvent.__init__( self )
#		self.__email = None
#		self.__email_id = email.id
#
#
#	def get_msg(self):
#		if not self.__email:
#			self.__email = ProMail.Message.get(ProMail.Message.id==self.__email_id)
#		return self.__email
#
#	msg = property(get_msg)
#
#
#	def get_email(self):
#		return MailWrapper(self.msg)
#
#	email = property(get_email)
#
#
#	def get_mailbox(self):
#		return MailboxWrapper(self.msg.mailbox)
#
#	mailbox = property(get_mailbox)
#
#
#
#class VEE_IncomingEmailArchive( VEE_IncomingEmail ):
#
#	def __init__( self, email ):
#		VEE_IncomingEmail.__init__( self, email )
#
#
#	def get_archive(self):
#		return ArchiveWrapper(self.msg.archive)
#
#	archive = property(get_archive)
#
#
#
#class VEE_BeforeEmailRendering( VEE_IncomingEmailArchive ):
#	pass
#
#
#
#event_map = {
#	0 : VEE_IncomingEmail,
#	1 : VEE_IncomingEmailArchive,
#	2 : VEE_BeforeEmailRendering,
#}
