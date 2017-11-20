import threading

from proadmin_db_scheme import DbApplicationScheme
from proadmin_remote_sync import RemoteSyncClient
from datetime import datetime


class RemoteApplicationScheme( DbApplicationScheme ):
	_local = threading.local()

	def __init__( self, guid, connection ):
		DbApplicationScheme.__init__( self, guid, connection )

		self.type = 'remote'
		
		self.remote_sync = None
		self.real_objects_discovery = None	# it's function

		self.sync_datetime = None



	def touch( self ):
		""" touch this scheme - update sync datetime
		"""
		self.sync_datetime = datetime.now()

	def is_sync_active( self ):
		if self.sync_datetime is None: return False
		return (datetime.now() - self.sync_datetime).total_seconds() < 60



	@property
	def prepare_synchronize( self ):
		""" obsolete. this field renamed to 'real_objects_discovery'
		"""
		return self.real_objects_discovery

	@prepare_synchronize.setter
	def prepare_synchronize( self, value ):
		""" obsolete. this field renamed to 'real_objects_discovery'
		"""
		self.real_objects_discovery = value



	def is_remote( self ):
		if getattr(self._local, 'is_remote', None) is None:
			from proadmin_remote_settings import RemoteSettings
			is_remote = bool(RemoteSettings.get_remote_settings())
			
			self._local.is_remote = is_remote

			if not is_remote:
				import ProAdmin
				ProAdmin.unregister_default_scheme()

		return self._local.is_remote


	def proadmin_version( self, details=False ):
		if self.remote_sync:
			return self.remote_sync.proadmin_version( details )

		return None


	def set_sync_service( self, service ):
		self.remote_sync = RemoteSyncClient( service )


	def update( self ):
		self.update_subjects()
		self.update_objects()

		self.touch()


	def update_subjects( self ):
		if self.remote_sync:
			self.remote_sync.update_subjects()

			self.touch()


	def update_objects( self ):
		if self.remote_sync:
			self.remote_sync.update_objects()

			self.touch()


	def commit( self ):
		if self.remote_sync:
			self.remote_sync.commit_objects()

			self.touch()


	def remove_acl_zombie( self ):
		import ProAdmin

		# get real objects
		objects = {}
		if self.real_objects_discovery:
			objects = self.real_objects_discovery()
		else: return

		# need guids only
		objects = objects.keys() if isinstance( objects, dict ) else objects

		# get acls guids
		acls = [ o.guid for o in ProAdmin.application().child_objects( recursive=True ) ]

		# define list of acl zombie
		acl_zombie = list( set(acls) - set(objects) )
			
		# delete acl objects if not exists
		for guid in acl_zombie:
			obj = ProAdmin.application().get_by_guid( guid )
			if not obj: continue
			
			obj.delete( parent_dirty=True )

			
		# add dirty-bit to application - for commit it to ProAdmin
		ProAdmin.application().save()


	def register( self, make_default=None ):
		import ProAdmin

		DbApplicationScheme.register( self )
		if self.remote_sync:
			data = self.remote_sync.register() or {}

			# try to define proadmin host throw API get_registered_applications
			
			hosts = []

			# find Proadmin
			apps = self.get_registred_applications()
			for name in apps:
				app = apps[ name ]
				if app[ 'guid' ] != ProAdmin.PROADMIN_APPLICATION_GUID:	continue

				hosts = app.get( 'hosts', [] )
				break

			# define one host from server response
			host = data.get( 'proadmin_host', hosts[0] if hosts else '' )

			# save option in remote sheme options
			self.set_option( 'proadmin_hosts', hosts )
			self.set_option( 'proadmin_host', host  )
			
			# flag for register_syn completeon
			self.set_option( 'register_sync', False )

			# update subjects
			self.remote_sync.update_subjects()


		ProAdmin.start_sync()
		# ProAdmin.sync()




	def sync( self ):
		# firstly start register sync
		if not self.get_option( 'register_sync', False ):
			self.remote_sync.register_sync()
			self.remove_acl_zombie()

			self.set_option( 'register_sync', True )
			return 5 # next sync after 5 sec

		# update
		self.update_subjects()
		self.update_objects()

		# commit
		self.commit()

		return 20 # timeout for next sync






	def get_registered_applications( self ):
		apps = {}
		
		if self.remote_sync:
			apps = self.remote_sync.get_registred_applications()

		return apps

	def get_registred_applications( self, *args, **kwargs ):
		""" obsolete, method for compatibility.
		"""
		return self.get_registered_applications( *args, **kwargs )
						
			
	def check_password( self, user, password ):
		if self.remote_sync:
			try:
				result = self.remote_sync.check_password( user.email, password )
				if result:
					user.password = password
					user.save()
				
				return True if result else False
			except:
				pass
				
		return user.check_local_password( password )				



	def create_root_user( self, password = 'root' ):
		return DbApplicationScheme.create_root_user( self, password=password )


	def create_admin_group( self ):
		return


			
			
			

