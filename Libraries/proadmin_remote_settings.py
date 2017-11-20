import ProAdmin
from class_db import Database

class RemoteSettings( object ):
	""" save settings for remote connection to ProAdmin
	"""

	# version of remote settings database
	__version__ = 2

	def __init__( self, login = None, password = None , server = None ):
		self._attributes 	= {}

		self[ 'server' ]	= server
		self[ 'login' ] 	= login
		self[ 'password' ]	= password



	def __getitem__( self, key ):
		return self._attributes.get( key, None )

	def __setitem__( self, key, value ):
		self._attributes[ key ] = value

	def __delitem__( self, key ):
		if key in self._attributes:
			del self._attributes[ key ]

	def keys( self ):
		return self._attributes.keys()



	def _fill_from_row( self, row ):
		self[ 'id' ] = row[0]
		self[ 'server' ] = row[1]
		self[ 'login' ] = row[2]
		self[ 'password' ] = row[3]
		
		#for key in row.keys():
		#	self[ key ] = row[ key ]

		return self



	def _ispersistent( self ):
		# check by id
		query = """
			SELECT id from remote_settings
			WHERE id = ?
		"""

		args = ( self.id, )
		row = Database.maindb().fetch_one( query, args )
		if row: return True


		# check by content
		query = """
			SELECT id from remote_settings
			WHERE server = ? AND login = ? and password = ?
		"""

		args = ( self.server, self.login, self.password )
		row = Database.maindb().fetch_one( query, args )
		if row: return True

		return False





	def _update( self ):
		if self.id is None:
			return self

		query = """
			UPDATE remote_settings
			SET
				server = ?,
				login = ?,
				password = ?

			WHERE id = ?
		"""

		args = ( self.server, self.login. self.password, self.id, )
		Database.maindb().commit( query, args )

		return self



	def _insert( self ):
		query = """
			INSERT INTO remote_settings (server, login, password)
			VALUES (?, ?, ?)
		"""

		args = ( self.server, self.login, self.password, )

		self.id = Database.maindb().commit( query, args )

		return self



	def _check_proadmin_host( self ):
		""" check that entered correct proadmin host
		"""
		return True
		# import urllib2

		# f = None
		# try:
		# 	url = self.server + '/sso_auth?test'

		# 	if not 'http://' in url:
		# 		url = 'http://' + url

		# 	f = urllib2.urlopen( url )
		# 	data = f.read()

		# 	if data.strip() != 'success':
		# 		raise Exception()

		# except:
		# 	return False

		# finally:
		# 	if f: f.close()

		# return True



	def _check_server_connection( self ):
		""" check that entered correct server connection settings
		"""
		from md5 import md5
		from vdom_remote_api import VDOMService

		service = VDOMService( self.server, self.login, md5( self.password ).hexdigest(), ProAdmin.PROADMIN_APPLICATION_GUID )

		try:
			service = service.open_session()
		except:
			return False

		return True





	def _check( self ):
		return self._check_server_connection() and self._check_proadmin_host()


	
	def save( self ):
		""" save data tot database
		"""

		if not self._check():
			return None

		# delete all old settings
		self.delete()

		if self._ispersistent():
			return self._update()
		else:
			return self._insert()

		return self




	@property
	def id( self ):
		return self[ 'id' ]

	@id.setter
	def id( self, value ):
		self[ 'id' ] = value


	@property
	def server( self ):
		return self[ 'server' ]

	@server.setter
	def server( self, value ):
		self[ 'server' ] = value


	@property
	def login( self ):
		return self[ 'login' ]

	@login.setter
	def login( self, value ):
		self[ 'login' ] = value


	@property
	def password( self ):
		return self[ 'password' ]

	@password.setter
	def password( self, value ):
		self[ 'password' ] = value




	@classmethod
	def get_remote_settings( self ):
		""" get remote settings from database
		"""
		query = """
			SELECT
				id as id,
				server as server,
				login as login,
				password as password

			FROM `remote_settings`
		"""

		row = Database.maindb().fetch_one( query )
		return self()._fill_from_row( row ) if row else None

	@classmethod
	def get_remote_setting( self ):
		""" alias for compatibility
		"""
		return self.get_remote_settings()


	@classmethod
	def get_all( self ):
		query = """
			SELECT
				id as id,
				server as server,
				login as login,
				password as password

			FROM `remote_settings`
		"""

		rows = Database.maindb().fetch_all( query )
		return [ self()._fill_from_row( row ) for row in rows ]



	@classmethod
	def delete( self ):
		Database.maindb().commit( 'DELETE FROM remote_settings' )




	# -------------------------------------------------
	#		Database modifications
	# -------------------------------------------------

	# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	@property
	def _version( self ):
		if not self._ispersistent():
			return None

		query = """
			SELECT version as version
			FROM remote_settings
			WHERE id = ?
		"""

		args = ( self.id, )

		row = Database.maindb().fetch_one( query, args )
		return int( row[ 'version' ] ) if row else 1


	@_version.setter
	def _version( self, value ):
		if not self._ispersistent():
			return

		query = """
			UPDATE remote_settings
			SET version = ?
			WHERE id = ?
		"""

		args = ( value, self.id, )
		Database.maindb().commit( query, args )



	def _update_database( self ):
		if self._version is None:
			return

		if self._version < RemoteSettings.__version__:
			self._update_2()



	def _update_2( self ):
		if self._version != 1:
			return

		# create `version` column
		query = """
			ALTER TABLE remote_settings
			ADD COLUMN version
		"""
		Database.maindb().commit( query )

		self._version = 2






