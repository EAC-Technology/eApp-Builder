import urllib2, cookielib, urllib, mimetools, mimetypes, ssl, httplib, socket
from urllib2 import URLError, HTTPError
from vscript import error
from vscript.subtypes import generic, binary
from VEE_std_lib import v_BaseException
from cStringIO import StringIO
from VEE_utils import is_string, is_array, encodeUTF8, decodeUTF8,\
 AutoCast, CachedProperty, AutoCastCachedProperty, is_byte_string, is_unicode_string, \
 enum, wrapp


v_sslversion = enum( 	v_sslv23 = wrapp( ssl.PROTOCOL_SSLv23 ),
						v_tlsv1  = wrapp( ssl.PROTOCOL_TLSv1  )
					)

v_sslcert = enum( 	v_certnone 		= wrapp( ssl.CERT_NONE 		),
					v_certoptional 	= wrapp( ssl.CERT_OPTIONAL 	),
					v_certrequired 	= wrapp( ssl.CERT_REQUIRED 	),
				)


ssl_params = { 	"keyfile"	  : None,
				"certfile"	  : None,
				"server_side" : False,
				"cert_reqs"	  : ssl.CERT_NONE,
				"ssl_version" : ssl.PROTOCOL_SSLv23,
				"ca_certs"	  : None,
				"do_handshake_on_connect" : True,
				"suppress_ragged_eofs" : True,
				"ciphers"	  : None }

#######################################
#Response Object
#######################################
class v_response_object( generic ):

	def __init__( self, obj ):
		self.object = obj


	@CachedProperty
	def response( self ):
		return self.object


	@CachedProperty
	def handler( self ):
		return self.object


	@CachedProperty
	def encoding( self ):
		if self.response.headers.has_key('Content-type'):
			encoding = self.response.headers[ 'Content-type' ].split( 'charset=' )
			if len( encoding ) > 1 :
				return encoding[ -1 ]
		return None


	@AutoCastCachedProperty
	def v_encoding( self ):
		return self.encoding


	@AutoCastCachedProperty
	def v_code( self ):
		return self.response.code


	@AutoCastCachedProperty
	def v_url( self ):
		return self.response.url


	@AutoCastCachedProperty
	def v_headers( self ):
		return dict(self.response.headers)


	@AutoCastCachedProperty
	def v_msg( self ):
		return self.response.msg


	@AutoCast
	def v_encode( self, data, encoding = None ):
		if not encoding: encoding = self.encoding
		if encoding and data:
			return data.decode( encoding )
		return data


	@AutoCast
	def v_read( self, size=-1, as_binary = False ):
		return binary(self.response.read( size )) if as_binary else \
				self.response.read( size )


	@AutoCast
	def v_readline( self, size=-1, as_binary = False  ):
		return binary(self.response.readline( size )) if as_binary else \
				self.response.readline( size )


	@CachedProperty
	def handler( self ):
		return self.response



#######################################
#Request Object
#######################################
class v_InvalidURLError( v_BaseException ):
	def __init__( self, message ):
		v_BaseException.__init__( 	self,
							message = message )



@AutoCast
def v_request( url, headers = None ):

	if not url: raise v_InvalidURLError( "URL could not be empty" )
	if url.startswith( "file:", 0 ):
		raise v_InvalidURLError( u"Unsupported URL - {0}".format( url ) )

	return v_request_object(
					urllib2.Request( 	encodeUTF8( url ),
										headers = headers if headers else {} ) )



class v_request_object( generic ):

	def __init__( self, obj ):
		self.object = obj


	@CachedProperty
	def request( self ):
		return self.object


	def encoding( self ):
		return self.request.get_header( 'Content-type', '' ).split( 'charset=' )[-1]


	@AutoCast
	def v_encoding( self ):
		return self.encoding()


	@AutoCast
	def v_method( self ):
		return self.request.get_method()


	@AutoCast
	def v_hasdata( self ):
		return self.request.has_data()


	@AutoCast
	def v_data( self ):
		return decodeUTF8( self.request.get_data() )


	@AutoCast
	def v_adddata( self, data ):
		self.request.add_data( encodeUTF8( data ) if is_unicode_string( data ) else data )


	@AutoCast
	def v_addheader( self, key, value ):
		self.request.add_header( key, value )


	@AutoCast
	def v_addunredirectedheader( self, key, value ):
		self.request.add_unredirected_header( encodeUTF8( key ), encodeUTF8( value ) )


	@AutoCast
	def v_hasheader( self, key ):
		return self.request.has_header( key.title() )


	@AutoCast
	def v_fullurl( self ):
		return self.request.get_full_url()


	@AutoCast
	def v_type( self ):
		return self.request.get_type()


	@AutoCast
	def v_host( self ):
		return self.request.get_host()


	@AutoCast
	def v_selector( self ):
		return self.request.get_selector()


	@AutoCast
	def v_getheader( self, name, default=None ):
		return self.request.get_header( name.title(), default )


	@AutoCast
	def v_headers( self ):
		return dict( self.request.headers )


	def encode_headers( self ):
		request = self.request
		header_items = request.headers.items()
		request.headers.clear()
		for item in header_items: request.add_header( encodeUTF8( item[0] ), encodeUTF8( item[1] ) )



#######################################
#Connection Object
#######################################
class v_URLError( v_BaseException ):
	pass

class CertificateError( ValueError ):
	pass

class SocketError( socket.error ):
	pass

class v_CertificateError( ValueError ):
	pass

class v_SocketError( socket.error ):
	pass



@AutoCast
def v_urlopen( request, opener=None ):

	if opener is None: opener = urllib2.build_opener()
	else: opener = opener.opener

	try:
		if is_string( request ): request = encodeUTF8( request )
		else:
			request.encode_headers()
			request = request.request

		response = opener.open( request )

	except HTTPError, e: response = e
	except URLError, e:  raise  v_URLError( e.reason )
	except CertificateError, e:  raise  v_CertificateError( str(e) )
	except SocketError, e:  raise  v_SocketError( str(e) )

	return v_response_object( response )



class v_connection_object( generic ):

	def __init__( self ):
		self.object = urllib2.build_opener()
		self.cookie = self.multipart = self.proxy = self.auth = self.ssl = False


	@CachedProperty
	def opener( self ):
		return self.object


	@AutoCast
	def v_open( self, request ):
		return v_urlopen( request, self )


	def v_usercookie( self ):
		if not self.cookie:
			self.opener.add_handler( urllib2.HTTPCookieProcessor( cookielib.CookieJar() ) )
			self.cookie = True


	def v_usemultipart( self ):
		if not self.multipart:
			self.opener.add_handler( MultipartPostHandler() )
			self.multipart = True


	@AutoCast
	def v_useproxy( self, proxy_url, proxy_scheme = "http",  ):
		if not self.proxy:
			proxy_handler = urllib2.ProxyHandler( { proxy_scheme: proxy_url } )
			self.opener.add_handler( proxy_handler )
			self.proxy = True


	@AutoCast
	def v_useauthorization( self, proxy_url, proxy_user = "", proxy_pass = "", proxy_realm = None ):
		if not self.auth:
			password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
			password_mgr.add_password( proxy_realm, proxy_url, proxy_user, proxy_pass )
			self.opener.add_handler( urllib2.ProxyBasicAuthHandler( password_mgr )  )
			self.auth = True


	@AutoCast
	def v_usehttps( self, params ):
		if not self.ssl:
			d = { param : params.get( param, ssl_params[ param ] ) for param in ssl_params }

			if d[ "keyfile"  ] is not None: d[ "keyfile"  ] = d[ "keyfile"  ].path
			if d[ "certfile" ] is not None: d[ "certfile" ] = d[ "certfile" ].path
			if d[ "ca_certs" ] is not None: d[ "ca_certs" ] = d[ "ca_certs" ].path

			self.opener.add_handler( HTTPSHandler( **d ) )
			self.ssl = True



v_connection = lambda: v_connection_object()

#######################################
#URLLib utility functions
#######################################
@AutoCast
def v_quote( text, safe = "/" ):
	return urllib.quote( encodeUTF8( text ), safe )

@AutoCast
def v_quoteplus( text, safe = "/" ):
	return urllib.quote_plus( encodeUTF8( text ), safe )

@AutoCast
def v_unquote( text ):
	return urllib.unquote( text )

@AutoCast
def v_unquoteplus( text ):
	return urllib.unquote_plus( text )

@AutoCast
def v_urlencode( query, doseq = True ):
	return urllib.urlencode( { encodeUTF8( k ) : encodeUTF8( v ) for k,v in query.items() }, doseq )



class Callable:
	def __init__(self, anycallable):
		self.__call__ = anycallable

doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):
	handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

	def http_request(self, request):

		data = request.get_data()
		if type(data) == dict:

			files, vars = [], []
#			try:
			for(key, value) in data.iteritems():
				if is_array( value ):
					files.append((key, value))
				else:
					vars.append((key, value))
#			except TypeError:
#				systype, value, traceback = sys.exc_info()
#				raise TypeError, "not a valid non-string sequence or mapping object", traceback

			if len(files) == 0:
				data = urllib.urlencode(vars, doseq)
			else:
				boundary, data = self.multipart_encode( vars, files )
				contenttype = 'multipart/form-data; boundary=%s' % boundary
				request.add_unredirected_header('Content-Type', contenttype)
				data = data.getvalue()

			request.add_data( data )
		return request

	def multipart_encode(vars, files, boundary = None, buffer = None):

		if boundary is None:
			boundary = mimetools.choose_boundary()

		buffer = StringIO()

		for(key, value) in vars:
			buffer.write( '--{0}\r\nContent-Disposition: form-data; name="{1}"\r\n\r\n{2}\r\n'.format(
				boundary, key, value ) )

		for(key,  lt) in files:
			filename, fd = lt[0], lt[1].handler
			fd.seek(0)
			contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream' #.encode("utf8") or 'application/octet-stream'
			buffer.write( '--{0}\r\nContent-Disposition: form-data; name="{1}"; filename="{2}"\r\nContent-Type: {3}\r\n\r\n{4}\r\n'.format(
						boundary, key, filename,contenttype, fd.read() ) )

		buffer.write( '--{0}--\r\n\r\n'.format( boundary ) )
		return boundary, buffer

	multipart_encode = Callable(multipart_encode)
	https_request = http_request



# HTTPS

def match_hostname(cert, hostname):
	if not cert:
		raise ValueError("empty or no certificate")
	dnsnames = []
	san = cert.get('subjectAltName', ())
	for key, value in san:
		if key == 'DNS':
			if _dnsname_to_pat(value).match(hostname):
				return
			dnsnames.append(value)
	if not dnsnames:
		for sub in cert.get('subject', ()):
			for key, value in sub:
				if key == 'commonName':
					if _dnsname_to_pat(value).match(hostname):
						return
					dnsnames.append(value)
	if len(dnsnames) > 1:
		raise CertificateError("hostname %r "
			"doesn't match either of %s"
			% (hostname, ', '.join(map(repr, dnsnames))))
	elif len(dnsnames) == 1:
		raise CertificateError("hostname %r "
			"doesn't match %r"
			% (hostname, dnsnames[0]))
	else:
		raise CertificateError("no appropriate commonName or "
			"subjectAltName fields were found")


def _dnsname_to_pat(dn):
	pats = []
	for frag in dn.split(r'.'):
		if frag == '*':
			pats.append('[^.]+')
		else:
			frag = re.escape(frag)
			pats.append(frag.replace(r'\*', '[^.]*'))
	return re.compile(r'\A' + r'\.'.join(pats) + r'\Z', re.IGNORECASE)





class HTTPSConnection( httplib.HTTPSConnection ):

	def __init__( self, host, **kwargs ):
		for param in ssl_params:
			self.__dict__[ param ] = kwargs.pop( param )

		self.checker = match_hostname
		httplib.HTTPSConnection.__init__(self, host, **kwargs)


	def connect( self ):
		args = [ ( self.host, self.port ), self.timeout ]
		if hasattr( self, 'source_address' ):
			args.append( self.source_address )

		sock = socket.create_connection( *args )

		if getattr( self, '_tunnel_host', None ):
			self.sock = sock
			self._tunnel()

		kwargs = {}
		self.sock = ssl.wrap_socket( sock,
										  **{ param : self.__dict__[ param ] for param in ssl_params }
									)

		if self.checker is not None:
			try:
				self.checker( self.sock.getpeercert(), self.host )
			except CertificateError:
				self.sock.shutdown( socket.SHUT_RDWR )
				self.sock.close()
				raise



class HTTPSHandler( urllib2.HTTPSHandler ):

	def __init__( self, *args, **kwargs ):
		urllib2.HTTPSHandler.__init__( self )
		for param in ssl_params:
			self.__dict__[ param ] = kwargs.pop( param )
		self.checker = match_hostname


	def https_open( self, req ):
		return self.do_open( self.getConnection, req )


	def getConnection( self, host, **kwargs ):
		d.update( { param : self.__dict__[ param ] for param in ssl_params } )
		return HTTPSConnection( host, **d )





EXCEPTIONS = (
	v_InvalidURLError,
	v_URLError,
	v_CertificateError,
	v_SocketError
)

import sys
current_module = sys.modules[__name__]
environment = tuple( (  (cls.__name__.lower(), error( cls ) ) for cls in EXCEPTIONS ) ) + \
( ( "v_urllib", 	current_module ), )
