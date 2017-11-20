import json


class AuthorizationError( Exception ):
	def __init__( self ):
		message = 'Need administrative rights. Relogin to application as "root".'
		Exception.__init__( self, message )





# -----------------------------------------------------------------------------
#		Common Utils for all applications
# -----------------------------------------------------------------------------

class CommonUtils( object ):
	@classmethod
	def is_proadmin( self ):
		""" define that current application is ProAdmin
		"""
		import ProAdmin
		return application.id == ProAdmin.PROADMIN_APPLICATION_GUID


	# ---------------------------------
	#  Server user authorization utils
	# ---------------------------------

	@classmethod
	def current_user( self ):
		""" get current server's user
		"""
		import managers
		return managers.request_manager.current.session().user


	@classmethod
	def login( self, login, password ):
		""" login user to server
		"""
		import managers
		managers.request_manager.current.session().set_user( login, password )


	@classmethod
	def logoff( self ):
		import managers
		managers.request_manager.current.session().set_user( 'guest', '' )


	@classmethod
	def is_admin( self ):
		""" check that current user admin
		"""
		return self.current_user().lower() in [ 'root', 'admin' ]




	# ---------------------------------
	#  Diagnostinc utils
	# ---------------------------------

	@classmethod
	def ping( self, showerror=False, raiseerror=False ):
		""" ping ProAdmin components for available
		"""
		import ProAdmin

		# define return formats
		def error_result( message='' ):
			error = {
				'status'	: 'error',
				'message'	: str( message )
			}

			if showerror:
				return json.dumps( error, indent=4 )

			return 'error'

		def success_result():
			success = {
				'status'	: 'success',
				'message'	: '',
			}

			if showerror:
				return json.dumps( success, indent=4 )

			return 'success'



		try:
			# check that scheme exists
			scheme = ProAdmin.scheme()
			if not scheme: raise Exception( "Can't create application scheme" )

			app = scheme.application
			if not app: raise Exception( "Can't create application ACL object" )

			# check objects ldap
			app.child_objects()

			# check users ldap
			app.get_users()

			if not scheme.is_remote():
				return success_result()

			# check sync thread
			if not ProAdmin.sync_thread: raise Exception( "Synchronization thread has crashed. Need server reboot." )

			# try to synchronize
			scheme.sync()


		except Exception as ex:
			if raiseerror: raise
			return error_result( ex.message )

		return success_result()





	@classmethod
	def info( self ):
		""" return information about current proadmin scheme
		"""
		if not self.is_admin():
			raise AuthorizationError()

		import ProAdmin
		from collections import OrderedDict
		info = OrderedDict()

		# application info
		app = ProAdmin.application()
		app_info = OrderedDict()
		app_info[ 'name' ] = app.name
		app_info[ 'guid' ] = app.guid
		app_info[ 'api' ] = app.scheme.get_option( 'api_guid' )
		info[ 'application' ] = app_info

		# scheme info
		scheme = ProAdmin.scheme()
		scheme_info = OrderedDict()
		scheme_info[ 'type' ] = scheme.type
		if scheme.is_remote():
			from proadmin_remote_settings import RemoteSettings
			settings = RemoteSettings.get_remote_settings()
			scheme_info[ 'host' ] = settings.server
			scheme_info[ 'login' ] = settings.login
		info[ 'scheme' ] = scheme_info

		return json.dumps( info, indent=4 )


	@classmethod
	def set_local_scheme( self ):
		""" set local scheme
		"""
		if not self.is_admin():
			raise AuthorizationError()

		from proadmin_remote_settings import RemoteSettings
		try:
			if RemoteSettings.get_remote_settings(): RemoteSettings.delete()
		except: pass

		import ProAdmin
		ProAdmin.unregister_default_scheme()



	@classmethod
	def set_remote_settings( self, server, user, password ):
		""" set another proadmin settings
		"""
		import ProAdmin
		from proadmin_remote_settings import RemoteSettings

		if not self.is_admin():
			raise AuthorizationError()

		if self.is_proadmin(): return

		remote = RemoteSettings.get_remote_settings()
		if remote and not password: password = remote.password

		RemoteSettings( user, password, server ).save()
		ProAdmin.logoff()
		ProAdmin.unregister_default_scheme()


	@classmethod
	def reset_root_password( self ):
		if not self.is_admin():
			raise AuthorizationError()

		import ProAdmin

		try:
			# find root user of create it
			root = ProAdmin.application().get_users( 'root' )
			if not root:
				root = ProAdmin.application().create_user( 'root' )
			else:
				root = root[0]

			# reset password to default
			root.password = 'root'
			root.save()

		except: raise







# -----------------------------------------------------------------------------
#		Utils specific only for ProAdmin application
# -----------------------------------------------------------------------------

class ProAdminUtils( CommonUtils ):
	@classmethod
	def info( self ):
		from collections import OrderedDict
		from class_db_application import DB_Application

		# get common information
		info = CommonUtils.info()
		info = json.loads( info, object_pairs_hook=OrderedDict )

		# get information about connected applications
		apps = DB_Application.get_all()

		def app_info( app ):
			result = OrderedDict()

			result[ 'name' ] = app.name
			result[ 'guid' ] = app.app_box_guid
			result[ 'host' ] = app.ip
			result[ 'api' ] = app.api_guid
			result[ 'ldap_guid' ] = app.guid

			return result
		info[ 'applications' ] = [ app_info(a) for a in apps ]

		return json.dumps( info, indent=4 )



	@classmethod
	def set_local_scheme( self ):
		""" set local scheme
		"""
		if not self.is_admin():
			raise AuthorizationError()

		
		from proadmin_external_settings import ProAdminSchemeConfig

		try:
			external = ProAdminSchemeConfig.get_active()
			if not external: return

			external.set_is_active( False )
			external.save()

		except: pass

		import ProAdmin
		ProAdmin.unregister_default_scheme()






# -----------------------------------------------------------------------------
#		Define correct class for concrete situation
# -----------------------------------------------------------------------------

Utils = ProAdminUtils if ProAdminUtils.is_proadmin() else CommonUtils
