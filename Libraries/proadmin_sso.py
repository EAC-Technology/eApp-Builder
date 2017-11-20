import ProAdmin

import json
import base64
import urllib2
import urllib
import copy
import string
import random
import md5
import os
import threading
import ssl

from Crypto.PublicKey import RSA
from proadmin_remote_settings import RemoteSettings



def https_urlopen(url, *args, **kwargs):
	if not 'https://' in url[:8].lower():
		return urllib2.urlopen(url, *args, **kwargs)

	if not 'context' in kwargs:
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		kwargs['context'] = ctx

	return urllib2.urlopen(url, *args, **kwargs)




# ==============================================================================
#					CRYPTO
# ==============================================================================

class SSOCrypto( object ):
	""" class implements crypt routines
	"""

	# -----------------------------------------
	#		CONSTS
	# -----------------------------------------

	# alphabet
	ALPHABET = string.digits + string.letters + string.punctuation

	# TODO: generate keys-pairs for each application !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	server_private_key 	= '-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQCwyaGooifV5+HsSoxfXaUC3txofCAeKoxQkDG6YAtYB+oF1dMC\nZUmdsgH70fhv82rhHqQhGYBSujvHs0y9Y6D1fI9Xpxdnl1UIo2y9EknmasWuTaVv\nVuYieHSPTRwZ03eE3LDRwvtXpzJ7uY2mx1YB9xx/fVvyurX463d1pfY2DwIDAQAB\nAoGAIYhtaH4xjipouRg+3gv2M8AwEIWS1gX+DX38YLy9ChqeMjMnzimGOCo+pBRk\nyl9io4bbXQfoRkja8/s3kCjoq7aMZqmmmh/P47kMY+2dCBEpG0WPFK+mWbz1vNO8\nELag6G0PC2e3IuKv9b2fJKlaVTRoUcOXv/Q8PTVsNq1qIFkCQQC9J4uLI50TW9DR\ni3NbORXIfk4DXqzPRl6k2oUY3qlIbJopHAWlk71l7HWVUnOKrZL3Yx3CJ5MnQ2Ah\ncfYbfY01AkEA70NHxe1UTJ4PNdwpHX/c140Tqv9l0pWVbDDp3L1buq8Bj6f7J+Av\nz1T3V+Hw+hQlyzMQ9vT0Qzs2FzKod9vSswJACPhrIboapORhzs4yNk1KvyteP8Kp\np1rK+j5yuW81z/12giSWD/glr0O7f81dNWJt6dWFf8Oost/7GxrwdPVLUQJAOcyv\nEgl7S+cDFafR5uZ0mz3henWoS28HYdOPK1wzRK3yWpnh+ogWBKgp+HkEleU4HBaC\nCqayO2uabZA3Un0wMQJAP1tLvFACcwW4LqZg3Uk5+vnKKraF2l2VtBTF5GuiXfbv\nCqwvBjcXDw+jRp8/Wnjvmtk1rlsOAzuo7jHnBhedCQ==\n-----END RSA PRIVATE KEY-----'
	server_public_key 	= '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwyaGooifV5+HsSoxfXaUC3txo\nfCAeKoxQkDG6YAtYB+oF1dMCZUmdsgH70fhv82rhHqQhGYBSujvHs0y9Y6D1fI9X\npxdnl1UIo2y9EknmasWuTaVvVuYieHSPTRwZ03eE3LDRwvtXpzJ7uY2mx1YB9xx/\nfVvyurX463d1pfY2DwIDAQAB\n-----END PUBLIC KEY-----'

	client_private_key	= '-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDleLlPj/Ha0YRLjF1meV8fu70x8aY979dWx58/lvYjY2UU8xpR\nnYhG0hGuEfFTWnk3dWv2IGPU18Ll7PnohXZUsYLRcVzj7Asp+H9Yg2RYHbRG5Xe2\nyY4sYFKX8QyvlvPAOomPHwpQneK6nTv5MdciUzxk+NkF7yFm6Ik2bX4msQIDAQAB\nAoGAJZAlhYiippc1eMh5YZTspV0uE0bjV7AzJ9l1kAs+L3zNxygkXsfSzwUEL+Jw\nBp0AyrtF+PxEW0sWdFzea9mtDNC7rD2GMF9pNGE1dqBRdaD6d5jLp0mv0/m0dGXr\nMGOXBnCL5ew4xndfwZfTCgX7JmzIHsMchMGb9q6MyGACZqECQQDqCgYZb8+xXWsE\nHX5y2kj60AI6Tqpt8LbMgO/vzuLkleWSYjov8sTyvdoFCMq1VMgORfYlBor0NYbl\n8W7L5C3PAkEA+wD62X2kavB4pR0hg9edTONMzK58rAGMQho+kfSIkuG4HR739i+5\n3QMQhWGG2YvK50Op7haiu4ZO3UjFm54DfwJBAMTDlqsuGQS6UK3OCjCPmwnbdfQF\njT4PQfCfepo4awPZjoBKuzbyuWiH+1N+N8bKN8PgR/iLDqoQkpCiMg+TkHsCQBmK\nvvwU0f9j2xMKRNfSwBoL40vM0bj7K1eqrgVSOfegaojkFt2Be8tmvW6lPwCyPgKM\nmyU0PnkQsMPJ3Pn5+WcCQGS44GfQA9ds8Ib9wvdNG8xgYpEvkTmh3i8Fc9n7/2rJ\ndN+KEXe4CU5EuJ7XqTSyTq8qtpmbz8B2Mr4lB6q6VP0=\n-----END RSA PRIVATE KEY-----'
	client_public_key	= '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDleLlPj/Ha0YRLjF1meV8fu70x\n8aY979dWx58/lvYjY2UU8xpRnYhG0hGuEfFTWnk3dWv2IGPU18Ll7PnohXZUsYLR\ncVzj7Asp+H9Yg2RYHbRG5Xe2yY4sYFKX8QyvlvPAOomPHwpQneK6nTv5MdciUzxk\n+NkF7yFm6Ik2bX4msQIDAQAB\n-----END PUBLIC KEY-----'




	# -----------------------------------------
	#		SELF-METHODS
	# -----------------------------------------

	def __init__( self, crypto_pair ):
		self._crypto = crypto_pair


	def keysize( self ):
		return ( self._crypto.size() + 1 ) / 8


	def encrypt( self, text ):
		""" encrypt text
		"""
		# get length of key
		n = self.keysize()

		# split text by n-length parts
		parts = [ text[ i:i+n ] for i in xrange( 0, len(text), n) ]

		# encrypt parts
		encrypt = lambda a: self._crypto.encrypt( a, None )[0]
		encrypted_parts = [ encrypt(s) for s in parts ]

		result = ''.join( encrypted_parts )
		if not result:
			return None

		return result


	def decrypt( self, code ):
		""" decrypt code
		"""
		# get length of key
		n = self.keysize()

		# split text by n-length parts
		encrypted_parts = [ code[ i:i+n ] for i in xrange( 0, len(code), n) ]

		# decrypt parts
		decrypt = lambda a: self._crypto.decrypt( a )
		parts = [ decrypt(s) for s in encrypted_parts ]

		result = ''.join( parts )
		return result






	# -----------------------------------------
	#		STATIC METHODS
	# -----------------------------------------

	@classmethod
	def salt( self, n ):
		""" create solt-string with n-length
		"""
		return ''.join( [ random.choice( SSOCrypto.ALPHABET ) for i in xrange( n ) ] )


	@classmethod
	def urandom( self, n ):
		""" create random solt-string using system os urandom
		"""
		return os.urandom( n )


	@classmethod
	def md5( self, text ):
		""" return md5-hexdigest of text
		"""
		return md5.md5( text ).hexdigest()


	@classmethod
	def generate_crypto_pair( self, bits=2048 ):
		""" generate RSA crypto keys-pair
		"""
		return RSA.generate( bits, self.urandom )




	@classmethod
	def server( self ):
		""" create server crypto-service
		"""
		server_pair = RSA.importKey( SSOCrypto.server_private_key + SSOCrypto.server_public_key )
		return self( server_pair )


	@classmethod
	def client( self ):
		""" create client crypto-service
		"""
		client_pair = RSA.importKey( SSOCrypto.client_private_key + SSOCrypto.client_public_key )
		return self( client_pair )



# alias for SSOCrypt class
Crypto = SSOCrypto











# ==============================================================================
#					URL
# ==============================================================================
class SSOUrl( object ):
	""" class for creating and parsing SSO-urls
	"""
	def __init__( self, url='' ):
		self._host = ''
		self.arguments = {}

		self._fill_from_url( url )

	def __str__( self ):
		return self.build()


	def _fill_from_url( self, url ):
		""" fill object from url string
		"""

		parts = url.split( '?' )

		# get host
		self.host = ''.join( parts[:1] ) if parts else url

		# get args
		args_str = ''.join( parts[1:] )

		# parse args
		args = args_str.split( '&' )
		for arg in args:
			item = arg.split( '=' )

			key = item[0] if item else None
			value = item[1] if len(item) > 1 else ''

			if key:
				self.arguments[ key ] = value

		return self


	def _args( self ):
		""" create get-arguments
		"""
		# create arguments string
		args = '&'.join( [ '%s=%s' % (key,value,) for (key,value) in self.arguments.iteritems() ] )
		return args if args else ''



	@property
	def host( self ):
		return self._host

	@host.setter
	def host( self, value ):
		self._host = value



	@property
	def cont_url( self ):
		cont = self.arguments.get( 'continue', '' )
		return urllib.unquote( cont )

	@cont_url.setter
	def cont_url( self, value ):
		self.arguments[ 'continue' ] = urllib.quote( value )



	@property
	def session_id( self ):
		sid = self.arguments.get( 'session_id', '' )
		return sid

	@session_id.setter
	def session_id( self, value ):
		self.arguments[ 'session_id' ] = value



	@property
	def auth_token( self ):
		token = self.arguments.get( 'auth_token' )
		return token

	@auth_token.setter
	def auth_token( self, value ):
		self.arguments[ 'auth_token' ] = value



	@property
	def user_login(self):
		login = self.arguments.get('user_login', '')
		return urllib.unquote(login)

	@user_login.setter
	def user_login(self, value):
		self.arguments['user_login'] = urllib.quote(value)






	def build( self ):
		""" create url-link
		"""
		# create arguments string
		result = self.host
		args = self._args()
		if args: result += '?' + args
		return result


	def loads( self, url ):
		self._fill_from_url( url )





	@classmethod
	def is_ip( self, host ):
		""" define that host is ip address
		"""
		if not host: return False

		if host.lower() == 'localhost': return True

		parts = host.split( '.' )
		for p in parts:
			if not p.isdigit(): return False

		return True



	def catch_exception( fn ):
		def wrapper( *args, **kwargs ):
			try:
				return fn( *args, **kwargs )
			except:
				return None

		return wrapper


	@classmethod
	@catch_exception
	def current_protocol( self ):
		if request.environment.get( 'SERVER_PORT', '80' ) == '443':
			return 'https'

		return request.protocol.name.lower()


	@classmethod
	@catch_exception
	def current_host( self ):
		return request.server.host


	@classmethod
	@catch_exception
	def current_page( self ):
		try:
			return request.environment.get( 'SCRIPT_NAME', '' )
		except:
			return None


	@classmethod
	@catch_exception
	def current_query( self ):
		try:
			return request.environment.get( 'QUERY_STRING', '' )
		except:
			return None


	@classmethod
	@catch_exception
	def current_url( self ):
		""" get current url
		"""
		return self.current_protocol() + '://' + self.current_host() + self.current_page() + '?' + self.current_query()


	@classmethod
	@catch_exception
	def current( self ):
		""" create Url-object from current request-url
		"""
		return self.parse( self.current_url() )


	@classmethod
	def parse( self, url ):
		""" parse url to Url-instance
		"""
		return self()._fill_from_url( url )


	@classmethod
	def sort_hosts_by_current( self, hosts ):
		""" sort hosts by samesess with current host
		"""
		if not hosts: return hosts

		current = SSOUrl.current_host()
		if not current: return hosts

		current = list( current.lower() )
		current.reverse()

		def distance( host ):
			""" calculate value of sameness any host with current
			"""
			if not host: return 0

			host = list( host.lower() )
			host.reverse()

			n = min( len(current), len(host) )
			for i in xrange( n ):
				if current[i] != host[i]:
					return i

			return n

		hosts.sort( cmp=lambda a,b: cmp(distance(a), distance(b)), reverse=True )
		return hosts




	@classmethod
	def proadmin_internal_url( self, page='' ):
		remote = RemoteSettings.get_remote_settings()
		host = remote.server

		if self.is_ip( host ):
			host += '/' + ProAdmin.PROADMIN_APPLICATION_GUID

		# check protocol
		if '://' not in host:
			host = SSOUrl.current_protocol() + '://' + host

		# check page
		if '/' in page[:1]:
			page = page[1:]

		host = '%(host)s%(page)s' % {
			'host'		: host,
			'page'		: '/' + page if page else '',
		}

		return self( host )



	@classmethod
	def proadmin_url( self, page='' ):
		""" get proadmin url from settings
		"""
		scheme = ProAdmin.scheme()

		hosts = scheme.get_option( 'proadmin_hosts', [ scheme.get_option( 'proadmin_host', '' ) ] )
		hosts = SSOUrl.sort_hosts_by_current( hosts )

		host = hosts[0] if hosts else ''

		# return internal url in bad situation
		if not host: return self.proadmin_internal_url( page )

		# complete host for normal situation
		# check protocol
		if '://' not in host:
			host = SSOUrl.current_protocol() + '://' + host

		# check page
		if '/' in page[:1]:
			page = page[1:]

		host = '%(host)s%(page)s' % {
			'host'		: host,
			'page'		: '/' + page if page else '',
		}

		return self( host )




	@classmethod
	def proadmin_sso_auth_url( self ):
		"""
		"""
		return self.proadmin_url( 'sso_auth' )

	@classmethod
	def proadmin_internal_sso_auth_url( self ):
		""" sso auth url for internal use
		"""
		return self.proadmin_internal_url( 'sso_auth' )










# ==============================================================================
#					SSO TOKEN
# ==============================================================================
class SerializationError( Exception ):
	""" serialization routines error
	"""
	pass



class SSOToken( object ):
	""" implement sso-routines user
	"""

	def __init__( self ):
		self.attributes = {}


	def _fill_from_token( self, token ):
		self.attributes = copy.copy( token.attributes )



	def _serialize( self, crypto=None ):
		""" serialize token. if exists crypto - crypt it
		"""
		try:
			# json - serialization
			js_attribs = json.dumps( self.attributes )

			# crypt token
			if crypto:
				crypted_attribs = crypto.encrypt( js_attribs )

			# base64
			result = base64.urlsafe_b64encode( crypted_attribs )
			return unicode( result )
		except:
			raise SerializationError()


	def _deserialize( self, b64_code, crypto=None ):
		try:
			# unbase64
			crypted_attribs = base64.urlsafe_b64decode( b64_code.encode( 'utf8' ) )

			# decrypt
			if crypto:
				js_attribs = crypto.decrypt( crypted_attribs )

			# deserialize json
			self.attributes = json.loads( js_attribs )
			return self
		except:
			raise SerializationError()




	def pack( self, crypto=None ):
		""" exception-safe serialization method
		"""
		try:
			return self._serialize( crypto )
		except SerializationError:
			return ''


	@classmethod
	def unpack( self, pack, crypto=None ):
		""" exception-safe deserialization method
		"""
		try:
			return self()._deserialize( pack, crypto )
		except SerializationError:
			pass




	# -----------------------------------------
	#		PROPERTIES
	# -----------------------------------------

	@property
	def user_guid( self ):
		return self.attributes.get( 'uid', '' )

	@user_guid.setter
	def user_guid( self, value ):
		self.attributes[ 'uid' ] = value




	@property
	def session_id( self ):
		return self.attributes.get( 'sid', '' )

	@session_id.setter
	def session_id( self, value ):
		self.attributes[ 'sid' ] = value





	@property
	def access_token( self ):
		value = self.attributes.get( 'tok', '' )
		if not value: return None

		return SSOAccessToken( value )


	@access_token.setter
	def access_token( self, token ):
		if type( token ) == SSOAccessToken:
			value = token.value
		else:
			value = token

		self.attributes[ 'tok' ] = value




	# -----------------------------------------
	#		COOKIES
	# -----------------------------------------

	TOKEN_KEY = '_token'
	GROUP_KEY = '_group'

	@classmethod
	def clear_auth_group_key( self ):
		"""
		"""
		if SSOToken.GROUP_KEY in request.cookies:
			response.cookies[ SSOToken.GROUP_KEY ] = ''
			response.cookies[ SSOToken.GROUP_KEY ]['max-age'] = 0


	@classmethod
	def auth_group_key( self ):
		"""
		"""
		def generate_key():
			return SSOCrypto.md5( SSOCrypto.salt( 32 ))[:8]

		def save_auth_group( value ):
			response.cookies[ SSOToken.GROUP_KEY ] = value
			response.cookies[ SSOToken.GROUP_KEY ][ 'max-age' ] = 15 * 60 * 1000 # 15min to ms

		# try to get from cookies
		cook = request.cookies.get( SSOToken.GROUP_KEY, None )

		if cook:
			result = cook.value
		else:
			result = generate_key()

		# update cookie
		save_auth_group( result )
		return result




	def save( self ):
		""" save current token in browser cookies
		"""
		# need to save only user_guid
		token = SSOToken()
		token.user_guid = self.user_guid

		# save to browser
		response.cookies[ SSOToken.TOKEN_KEY ] = token.pack( SSOCrypto.server() )
		response.cookies[ SSOToken.TOKEN_KEY ]['max-age'] = 15 * 60 * 1000 # 15min to ms


	@classmethod
	def current( self ):
		cook = request.cookies.get( SSOToken.TOKEN_KEY, None )
		result = None

		try:
			result = self()._deserialize( cook.value, SSOCrypto.server() ) if cook else None

		except SerializationError:
			self.clear()

		return result


	@classmethod
	def clear( self ):
		if SSOToken.TOKEN_KEY in request.cookies:
			response.cookies[ SSOToken.TOKEN_KEY ] = ''
			response.cookies[ SSOToken.TOKEN_KEY ]['max-age'] = 0

		# clear auth group
		self.clear_auth_group_key()














# ==============================================================================
#					ACCESS TOKEN
# ==============================================================================

class AccessTokenUsedError( Exception ):
	""" error that access token now using in ProAdmin for other token
	"""
	pass

class AuthorizeError( Exception ):
	""" error that
	"""


class SSOAccessToken( object ):
	""" class for auth_token routines
	"""

	_local = threading.local()

	@classmethod
	def _local_saveresult( self, data ):
		SSOAccessToken._local.checked_token = data

	@classmethod
	def _local_ischecked( self, data ):
		value = getattr( SSOAccessToken._local, 'checked_token', '' )
		return data == value




	def __init__( self, token=None ):
		self._data 	= token if token else self._create_token_key()

	def __str__(self):
		return self.data


	@property
	def data( self ):
		return self._data if self._data else '-'


	@property
	def key( self ):
		"""
		"""
		return self.data.split( '-' )[0]

	def _set_key( self, key ):
		self._data = '%(key)s-%(value)s' % {
			'key'	: key,
			'value'	: self.value,
		}



	@property
	def value( self ):
		""" property for get token-value
		"""
		return self.data.split( '-' )[1]




	@classmethod
	def _create_token_key( self ):
		""" create new token value
		"""
		generate = lambda: SSOCrypto.md5( SSOCrypto.salt( random.randint(200, 1000) ) )
		tok = generate() + generate()
		return '-%s' % tok



	def check( self ):
		""" check this token in ProAdmin
		"""
		import ProAdmin
		# TODO: use a local ProAdmin Agent-Server !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		# not need to check rights in local scheme
		if not ProAdmin.scheme().is_remote():
			return True

		# --------------------------------------------------------------------- Fake
		keys = [ 'fc2221b2', '794b4c40', '991f6c7c', '2f61dbc2' ]
		if self.key in keys:
			return True
		# ---------------------------------------------------------------------

		# check saved result in threading.local()
		if self._local_ischecked( self.data ):
			return True

		url = SSOUrl.proadmin_internal_sso_auth_url()
		url.arguments[ 'check_token' ] = '1'
		url.arguments[ 'access_token' ] = self.data

		# HTTP GET Request
		f = https_urlopen( url.build() )
		result = f.read()
		f.close()

		if result.strip() != 'success':
			return False

		# save result in threading.local()
		self._local_saveresult( self.data )
		return True


	# ----------------------------------------------------------------------------------
	@classmethod
	def get_sudo_accesstoken( self, user ):
		access_token = self()
		keys = [ 'fc2221b2', '794b4c40', '991f6c7c', '2f61dbc2' ]
		import random
		key = random.choice( keys )
		access_token._set_key( key )
		return access_token




	# ----------------------------------------------------------------------------------
	def __fake_prosearch_login( self ):
		keys = [ 'fc2221b2', '794b4c40', '991f6c7c', '2f61dbc2' ]
		if self.key not in keys:
			return False

		ssn = ProAdmin.session()
		ssn[ 'access_token' ] = self
		ssn[ 'current_user' ] = ProAdmin.application().get_users( 'root' )[0]

		self._local_saveresult( self.data )
		return True



	def login( self ):
		""" login by this access token
		"""
		if not ProAdmin.scheme().is_remote():
			auth_token = self.create_auth_token( ProAdmin.session().id )
			ProAdmin.login_token( auth_token )
			return

		# temp fake login for prosearch only -------------------------------------------
		if self.__fake_prosearch_login():
			return
		# ------------------------------------------------------------------------------

		url = SSOUrl.proadmin_internal_sso_auth_url()

		# set session and token
		url.arguments[ 'session_id' ] = ProAdmin.session().id
		url.arguments[ 'login_access_token' ] = '1'
		url.arguments[ 'access_token' ] = self.data

		# HTTP GET Request
		f = https_urlopen( url.build() )
		result = f.read()
		f.close()

		result = result.strip()

		if result == 'error':
			return

		ProAdmin.login_token( result )


	def authorize( self, token ):
		""" authorize this access token to user
		"""
		if not token:
			raise AuthorizeError()

		# check that access_token not used in ProAdmin
		if self.is_authorized():
			raise AccessTokenUsedError()

		# modify auth_group_key in access_token
		key = token.auth_group_key()
		self._set_key( token.auth_group_key() )

		# save token as authorized in memory
		if key not in ProAdmin.authorized_tokens:
			ProAdmin.authorized_tokens[ key ] = {}

		# append this access token to group of tokens
		ProAdmin.authorized_tokens[ key ][ self.value ] = token
		token.access_token = self.data



	def create_auth_token( self, session_id ):
		""" create new auth_token eq for this access token
		"""
		import copy

		if not self.is_authorized():
			return None

		# get user
		token = copy.deepcopy( self.get_token() )
		if not token: return None

		# modify session_id
		token.session_id = session_id

		# create new access_token for new auth
		access_token = SSOAccessToken()
		access_token._set_key( self.key )
		access_token.authorize( token )

		return token.pack( SSOCrypto.client() )




	def get_token( self ):
		"""
		"""
		if not self.is_authorized():
			return None

		return ProAdmin.authorized_tokens.get( self.key, {} ).get( self.value, None )



	def is_authorized( self ):
		""" check that this token authorized in ProAdmin
		"""
		# get auth group key
		key = self.key

		# check that it valid
		if self.value not in ProAdmin.authorized_tokens.get( key, {} ):
			return False

		return True



	@classmethod
	def from_url( self, url=None, name=None ):
		"""
		"""
		if not url: url = SSOUrl.current()
		if not name: name = 'access_token'

		token = url.arguments.get( name )
		if not token: token = url.arguments.get( 'token' ) # for old version capability

		if not token: return None
		return self( token )



	@classmethod
	def is_access_token( self, token ):
		if type( token ) == self:
			return True

		if len( token.split('-') ) != 2: return False
		if len( token ) > 100: return False


		return True








# ==============================================================================
#					SSO Helpers
# ==============================================================================


class SSOLoginBase( object ):
	""" implements various login mechanisms
	"""
	def __init__( self, request, response, back_url=None ):
		self.request = request
		self.response = response
		self._default_back_url = back_url or '/home'

		self.vdom_page = None


	def set_action_mode( self, vdom_page ):
		self.vdom_page = vdom_page

	def is_action_mode( self ):
		return self.vdom_page is not None


	def redirect( self, url ):
		# onload mode
		if self.vdom_page is None:
			self.response.redirect( url )
			return

		# action mode
		self.vdom_page.action( 'goTo', [ url ] )
		return


	def login( self ):
		pass


	@property
	def back_url( self ):
		""" get back_url
		"""
		back_url = self.request.arguments.get( "back_url", '' )
		back_url = urllib.unquote( back_url )

		if not back_url: back_url = self._default_back_url
		return back_url


	def get_language( self ):
		return ProAdmin.session().get( 'lang', None )


	def login_by_password( self ):
		""" login user in local scheme by entered user name and password
		"""
		if 'login' not in self.request.arguments:
			return

		# get login and password
		login 		= self.request.arguments.get( 'login', '' )
		password 	= self.request.arguments.get( 'password', '' )

		# check login
		if not login:
			raise ProAdmin.ProAdminEmptyLoginError()

		# try to login in application
		ProAdmin.login( login, password )


	def check_current_user( self ):
		""" check that current user exists
		"""
		if not ProAdmin.current_user():
			return

		self.redirect( self.back_url )


# obsolete name
LoginHelper = SSOLoginBase





class SSOClient( SSOLoginBase ):
	"""
	"""
	def __init__( self, request, response, back_url=None ):
		LoginHelper.__init__( self, request, response, back_url )


	def login_by_password( self ):
		LoginHelper.login_by_password( self )

		if ProAdmin.current_user():
			self.redirect( self.back_url )


	def login_by_token( self ):
		""" login user by auth_token returned from ProAdmin /login page
		"""
		if not ProAdmin.scheme().is_remote():
			return

		if 'auth_token' not in self.request.arguments:
			return

		# get auth_token
		auth_token = self.request.arguments.get( 'auth_token', '' )
		token = SSOToken.unpack( auth_token, SSOCrypto.client() )

		# auth_token can't unpack
		if not token:
			self.redirect( '/login?back_url=%s' % self.back_url )

		# login user by token
		try:
			ProAdmin.login_token( token )
		except ProAdmin.TokenSessionExpiredError:
			self.redirect( '/login?back_url=%s' % self.back_url )

		# go to back url
		self.redirect( self.back_url )



	def login_by_proadmin( self, user_login=None ):
		""" ask auth_token from ProAdmin
		"""
		if not ProAdmin.scheme().is_remote():
			return

		cont_url = SSOUrl.current()
		cont_url.arguments[ 'back_url' ] = urllib.quote( self.back_url )

		# check server
		url = SSOUrl.proadmin_sso_auth_url()

		url.session_id = ProAdmin.session().id
		url.cont_url = cont_url.build()

		if user_login is not None:
			url.user_login = user_login

		self.redirect( url.build() )



	def test_sso( self, url='', check=False, get_url=False ):
		""" test sso redirects
		"""
		# check response from ProAdmin
		if check:
			result = self.request.arguments.get( 'test_sso', None )
			return result == 'success'

		# define back url
		back_url = SSOUrl.current_url()
		if self.is_action_mode():
			back_url = SSOUrl.current_protocol() + '://' + SSOUrl.current_host() + '/' + self.vdom_page.name + '?' + SSOUrl.current_query()

		# send request to proadmin
		if not url:
			url = SSOUrl.proadmin_url().build()

		if SSOUrl.is_ip( url ):
			url = SSOUrl.proadmin_internal_url().build()

		if not '://' in url:
			url = SSOUrl.current_protocol() + '://' + url

		url = SSOUrl( url + '/sso_auth' )

		url.arguments[ 'test_sso' ] = 1
		url.arguments[ 'continue' ] = back_url

		if get_url:
			return url.build()

		self.redirect( url.build() )



# obsolete name
ClientLoginHelper = SSOClient




class SSOServer( SSOLoginBase ):
	"""
	"""
	def __init__( self, request, response ):
		LoginHelper.__init__( self, request, response )


	def login_by_access_token( self ):
		try:
			access_token = SSOAccessToken.from_url()
			if not access_token: raise Exception()

			session_id = self.request.arguments.get( 'session_id' )

			auth_token = access_token.create_auth_token( session_id )

			self.response.write( auth_token, True )

		except Exception as er:
			self.response.write( 'error', True )


	def check_token( self ):
		try:
			# create user object
			access_token = SSOAccessToken.from_url( SSOUrl.current() )

			# check that user authorized
			if not access_token.is_authorized():
				raise Exception()

			response.write( 'success', True )

		except Exception as ex:
			self.response.write( 'error', True )



	def login_by_browser_token( self, token ):
		""" login user by token, saved in browser
		"""
		if not token:
			return

		# modify token for browser session
		token.session_id = ProAdmin.session().id
		ProAdmin.login_token( token )



	def sso_redirect( self ):
		user = ProAdmin.current_user()

		if user and 'continue' in self.request.arguments:
			url			= self.request.arguments.get( 'continue', '' )
			session_id 	= self.request.arguments.get( 'session_id', '' )

			# create cont_url
			cont_url = SSOUrl.parse( url )

			# set language
			ln = self.get_language()
			if ln: cont_url.arguments[ 'ln' ] = ln

			# create login token
			token = SSOToken()
			token.user_guid = user.guid

			# save in browser cookies
			token.save()

			# modify token for user session
			token.session_id = session_id

			# create access token
			access_token = SSOAccessToken()
			access_token.authorize( token )

			token.access_token = access_token.data

			cont_url.auth_token = token.pack( SSOCrypto.client() )
			self.redirect( cont_url.build() )



	def test_sso( self ):
		""" test sso redirects
		"""
		if 'test_sso' not in self.request.arguments:
			return

		url = SSOUrl( self.request.arguments.get( 'continue' ) )
		url.arguments[ 'test_sso' ] = 'success'

		self.redirect( url.build() )




# obsolete name
ServerLoginHelper = SSOServer
