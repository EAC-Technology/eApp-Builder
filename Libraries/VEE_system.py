from utils.system import get_hd_size, get_free_space
from VEE_utils import AutoCast, encodeUTF8
from vscript import generic, version
#from promail_tasks import logger as tasks_logger


#logger = tasks_logger.getChild("VEE_system")

APPLICATION_LIBRARIES_VERSION = 2

class v_smartcard( object ):

	@classmethod
	@AutoCast
	def v_getparameterbyid( self, id ):
		from utils.card_connect import get_system_attribute
		return get_system_attribute( id )


	#obsolete methods names
	v_get_parameter = v_getparameterbyid


class v_system( object ):

	@staticmethod
	@AutoCast
	def v_applicationid( ):
		return application.id


	@staticmethod
	@AutoCast
	def v_applicationname( ):
		import config
		return config.config[ "app_name" ]


	@staticmethod
	@AutoCast
	def v_applicationversion( ):
		import config
		return config.config[ "version" ]


	@staticmethod
	@AutoCast
	def v_applicationhosts( ):
		return v_system.application_hosts()


	@classmethod
	def application_hosts( self ):
		try:
			import managers
			app_virtual_host = managers.virtual_hosts.get_site
			app_sites		 = managers.virtual_hosts.get_sites()
			app_id 			 = application.id
			return [  site for site in app_sites if app_id == app_virtual_host( site ) ]
		except Exception as ex:
#			logger.debug('Err: system.application_hosts {}'.format(ex))
			return [request.headers.get('host', '').split(':')[0]]


	@staticmethod
	@AutoCast
	def v_serverversion( ):
		return server.version


	@staticmethod
	def v_enabledebug( ):
		v_system.debug( True )


	@staticmethod
	def v_disabledebug( ):
		v_system.debug( False )


	@staticmethod
	def debug( value, disp ):
		disp.debug = value

	@staticmethod
	def v_clearlog( disp ):
		disp.clear_log()


	@staticmethod
	@AutoCast
	def log( msg , disp ):
		disp.info(  msg  )


	@staticmethod
	@AutoCast
	def v_sendemail( to_email, from_email, subject, body, reply="" ):
		server.mailer.send( fr=from_email,to=to_email,subj=subject,msg=body,reply=reply )


	@staticmethod
	@AutoCast
	def v_httprequest( url ):
		import urllib2
		urllib2.urlopen( url )


	@staticmethod
	@AutoCast
	def v_vscriptversion( ):
		return "{major}.{minor}.{build}.{env}".format( 	major = version.major,
														minor = version.minor,
														build = version.build,
														env = APPLICATION_LIBRARIES_VERSION )

	class v_hdd( object ):
		@staticmethod
		@AutoCast
		def v_totalspace():
			#         Gb         Mb      Kb      bytes
			return get_hd_size()*1024.0*1024.0*1024.0


		@staticmethod
		@AutoCast
		def v_freespace():
			#         Gb         Mb      Kb      bytes
			return get_free_space()*1024.0*1024.0*1024.0



	#obsolete methods names
	v_application_id 		= v_applicationid
	v_application_name 		= v_applicationname
	v_application_version 	= v_applicationversion
	v_application_hosts 	= v_applicationhosts
	v_server_version 		= v_serverversion
	v_enable_debug 			= v_enabledebug
	v_disable_debug 		= v_disabledebug
	v_clear_log 			= v_clearlog
	v_send_email 			= v_sendemail
	v_http_request 			= v_httprequest


environment = (
	( "v_smartcard",			v_smartcard	),
	( "v_system",				v_system	),
)
