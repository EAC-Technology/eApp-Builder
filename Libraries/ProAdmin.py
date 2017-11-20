from hashlib import md5
import managers
import threading


class ProAdminRegisterSchemeError( Exception ):
	def __init__( self, message=None ):
		if not message: message = 'Application scheme is not registred in ProAdmin'
		Exception.__init__( self, message )

class ProAdminLoginError( Exception ):
	def __init__( self, message=None ):
		if not message: message = 'Invalid user name or password'
		Exception.__init__( self, message )

class ProAdminEmptyPasswordError( ProAdminLoginError ):
	def __init__( self, message=None ):
		if not message: message = 'Password must not be empty'
		Exception.__init__( self, message )

class ProAdminEmptyLoginError( ProAdminLoginError ):
	def __init__( self, message=None ):
		if not message: message = 'Login must not be empty'
		Exception.__init__( self, message )

class SubjectsLimitationError( Exception ):
	def __init__( self, message=None ):
		if not message: message = 'Subjects limitation error'
		Exception.__init__( self, message )

class TokenSessionExpiredError( Exception ):
	def __init__( self, message=None ):
		if not message: message = 'Required session is over'
		Exception.__init__( self, message )



# version of library
__version__ = '1.09'




# save globals variables
SESSION 	= session
APPLICATION = application




# -----------------------------------------------------
#	Fake Session - need for macros background threads
# -----------------------------------------------------

class FakeSession( object ):
	def __init__( self ):
		import uuid
		self.__id	= str(uuid.uuid4())
		self.__data = {}


	@property
	def id( self ):
		return self.__id


	@property
	def _data( self ):
		return self.__data



	def get( self, key, default_value=None ):
		return self._data.get( key, default_value )

	def keys( self ):
		return self._data.keys()



	def __getitem__( self, key ):
		return self._data[ key ]

	def __setitem__( self, key, value ):
		self._data[ key ] = value

	def __delitem__( self, key ):
		if key in self._data:
			del self._data[ key ]



	def __iter__( self ):
		for key in self._data:
			yield self._data[ key ]



# thread-safe Singleton of _FakeSession
_local = threading.local()

class FakeSessionSingleton( FakeSession ):
	def __new__( cls, *args, **kwargs ):
		try:
			return _local.instance
		except:
			pass

		# create new object
		_local.instance = FakeSession.__new__( cls, *args, **kwargs )
		_local.instance.__created = True

		return _local.instance

	def __init__( self ):
		if self.__created:
			self.__created = False
			FakeSession.__init__( self )




def session():
	# check that real session exists
	try:
		SESSION.id
		return SESSION
	except:
		pass

	# create fake session for this thread
	return FakeSessionSingleton()

def _session():
	""" obsolete for capability
	"""
	return session()





# const
PROADMIN_APPLICATION_GUID = '491d4c93-4089-4517-93d3-82326298da44'



# global variable for save current scheme
current_scheme = None

# global variable - saves thread for synchronization
sync_thread = None

# authorized_tokens
authorized_tokens = {}


def register_scheme( scheme ):
	""" register scheme in ProAdmin memory
	"""
	# stop synchronization
	stop_sync()

	global current_scheme
	current_scheme = scheme
	logoff()


def unregister_default_scheme():
	global current_scheme
	current_scheme = None
	logoff()


def delete_scheme( schema ):
	""" delete scheme from ProAdmin memory
	"""
	global current_scheme
	current_scheme = None
	logoff()





def local_scheme( guid="", connection=None ):
	""" create new instance of local scheme
	"""
	from proadmin_local_ldap_application_scheme import LocalLDAPApplicationScheme
	return LocalLDAPApplicationScheme( guid, connection )


def remote_scheme( guid="", connection=None ):
	""" create new instance of remote scheme
	"""
	from proadmin_remote_application_scheme import RemoteApplicationScheme
	return RemoteApplicationScheme( guid, connection )


def external_scheme( guid="", connection=None, userconnection=None, config=None ):
	""" create external application scheme
	"""
	from proadmin_external_application_scheme import ExternalApplicationScheme
	return ExternalApplicationScheme( guid, connection, userconnection, config )





def scheme():
	""" return current active scheme
	"""
	# try to create default scheme
	try:
		if not current_scheme:
			from proadmin_config import create_default_scheme
			create_default_scheme()
			logoff()
	except Exception, ex:
		raise

	# if scheme not registred - raise Exception
	if not current_scheme:
		raise ProAdminRegisterSchemeError()

	# if scheme exists
	return current_scheme



def application():
	return scheme().application





def get_registered_applications( guid_key=False ):
	from proadmin_sso import SSOUrl

	apps = scheme().get_registered_applications() or {}

	# sort hosts by samesess with current host
	for name in apps:
		app = apps[ name ]
		SSOUrl.sort_hosts_by_current( app.get('hosts', []) )

	# transform result
	if guid_key:
		apps_names = apps.keys()
		for name in apps_names:
			# pop application info from dictionary
			app = apps[ name ]
			del apps[ name ]

			# save it by guid-key
			apps[ app['guid'] ] = app

	return apps


def get_registred_applications( guid_key=False ):
	""" OBSOLETE. NEED FOR COMPATIBILITY.
	"""
	return get_registered_applications( guid_key )


def get_scheme_discovery():
	return [ scheme().guid, scheme().name ]






def start_sync():
	global sync_thread

	# create background sync thread and start it
	if not sync_thread:
		from proadmin_time_trigger import ProAdminTimeTrigger
		sync_thread = ProAdminTimeTrigger()
		sync_thread.start()

	# set synchronization procedure to background thread
	if scheme().is_remote():
		from proadmin_remote_application_scheme import RemoteApplicationScheme
		sync_thread.set_action( RemoteApplicationScheme.sync )


def stop_sync():
	global sync_thread

	if not sync_thread:
		return

	sync_thread.unset_action()

	# stop background thread
	try:
		sync_thread.stop()
	except:
		pass
	finally:
		sync_thread = None






def login_token( token ):
	""" accpet user by token
	"""
	from proadmin_sso import SSOToken, SSOAccessToken, SSOCrypto

	if type( token ) in [ unicode, str ]:
		if SSOAccessToken.is_access_token( token ):
			token = SSOAccessToken( token )
		else:
			token = SSOToken.unpack( token, SSOCrypto.client() )

	# login by access token
	if type( token ) == SSOAccessToken:
		token.login()
		return

	user_guid = token.user_guid
	session_id = token.session_id

	if session().id != session_id:
		raise TokenSessionExpiredError()

	# login user
	user = application().get_subject( user_guid )
	if not user:
		token.clear()
		raise ProAdminLoginError()

	# save user and token to current session
	session()[ 'current_user' ] = user
	session()[ 'access_token' ] = token.access_token



def sudo_accesstoken( user ):
	""" get authorized access token for user
	"""
	from proadmin_sso import SSOToken, SSOAccessToken, SSOCrypto
	return SSOAccessToken.get_sudo_accesstoken( user ).data



def login( email, password ):
	""" login user to ProAdmin
	"""
	# remove current user
	logoff()

	if not email:
		raise ProAdminLoginError()

	# empty password disabled in ProAdmin
	if not password:
		raise ProAdminEmptyPasswordError()

	# get user
	users = application().get_users( email=email )
	if not users:
		raise ProAdminLoginError()

	# check password
	user = users[ 0 ]
	if not user.check_password( password ):
		raise ProAdminLoginError()

	try:
		webdav_manager = managers.webdav_manager
	except AttributeError:
		webdav_manager = None

	if webdav_manager and hasattr(webdav_manager,"list_webdav"):
		davs = webdav_manager.list_webdav("b0a274f0-22bc-44be-be48-da6ec9180268") # ProShare ID
		dirty = False
		for dav in davs:
			davtoken = gen_dav_token(email, dav, password)
			if user.options.get("davtoken%s"%dav) != davtoken:
				user.options["davtoken%s"%dav] = davtoken
				dirty = True
		if dirty:
			user.save()

	session()[ 'current_user' ] = user

def gen_dav_token(username, realm, password):
	A1 = username + ":" + realm + ":" + password
	return md5(A1).hexdigest()

def access_token():
	""" return current auth_token
	"""
	auth_token = session().get( 'access_token', None )
	return auth_token



def current_user():
	""" return current logined user
	"""
	scheme()

	def fix_addled( user ):
		if not user._is_addled_instance(): return user
		users = application().get_users( guid=user.guid )
		return users[0] if users else None

	# try setted user
	user = session().get( 'sudo', None )
	if user: return fix_addled(user)

	# check auth_token
	token = access_token()
	if token and not isinstance(token, basestring) and not token.check():
		logoff()

	user = session().get( 'current_user', None )
	if not user:
		logoff()
		return None

	# check user
	if getattr( _local, 'current_user_guid', None ) == user.guid:
		return fix_addled(user)

	if application().get_subject( user.guid ):
		_local.current_user_guid = user.guid
		return fix_addled(user)
	else:
		logoff()

	return None



def set_user( user ):
	""" change current user
	"""
	# remove (unset) sudo-user if user is None
	if not user:
		session()[ 'sudo' ] = None
		del session()[ 'sudo' ]
		return

	session()[ 'sudo' ] = user





def create_group( name, users=None ):
	""" create group in proadmin and return it's guid
	"""
	if not name: return None
	users = users or []

	# this operation incorrect for external scheme
	if scheme().type == 'external':
		return None

	guid = None

	# create in ProAdmin
	if scheme().is_remote():
		api = scheme().remote_sync
		guid = api.create_group( name, users )

	# create group in local
	group = application().create_group( name )
	if guid: group.guid = guid

	# add users to group
	for u in users:
		user = application().get_subject( u )
		if user: group.add_user( user )

	# save changes
	group.save()
	return group.guid




def create_user( self ):
	pass











def logoff():
	""" logoff current user
	"""
	# remove user
	session()[ 'current_user' ] = None
	del session()[ 'current_user' ]

	# remove auth_token
	session()[ 'access_token' ] = None
	del session()[ 'access_token' ]

	# remove set_user
	session()[ 'sudo' ] = None
	del session()[ 'sudo' ]







def login_server( login, password ):
	""" login user to server
	"""
	import managers
	managers.request_manager.current.session().set_user( login, password )

def logoff_server():
	""" logoff server's user
	"""
	login_server( 'guest', '' )

def server_user():
	""" get current server's user
	"""
	import managers
	return managers.request_manager.current.session().user

def is_server_admin():
	""" check that current server's user is admin
	"""
	user = server_user().lower()
	return user in [ 'root', 'admin' ]







def hosts():
	""" get hosts of this application
	"""
	from managers import virtual_hosts

	appid = APPLICATION.id.lower()

	# define host by virtual hosts
	hosts = virtual_hosts.get_sites()
	hosts = [ h for h in hosts if h ]
	hosts = [ h for h in hosts if virtual_hosts.get_site(h).lower() == appid ]

	hosts.sort()
	return hosts



# obsolete. save for compatibility
from proadmin_base_scheme import ACLObjectType, Icon
