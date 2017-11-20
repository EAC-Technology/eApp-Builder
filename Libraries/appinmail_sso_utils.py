import json
import base64
import zlib
import urlparse, urllib
import threading



class Local(object):
	_local = threading.local()

	@classmethod
	def get(self, key, default=None):
		return getattr(self._local, key, default)

	@classmethod
	def set(self, key, value):
		self._local.__setattr__(key, value)


def thread_local_cache(clsname=None):
	def decorator(func):
		key = func.__name__
		if clsname: key = str(clsname) + '_' + key

		def wrapper(*args, **kwargs):
			import threading
			value = Local.get(key)
			if value is None:
				value = func(*args, **kwargs)
				Local.set(key, value)
			return value

		return wrapper

	return decorator




class Utils(object):
	@classmethod
	def serialize(self, data):
		jdata = json.dumps(data)
		zdata = zlib.compress(jdata)
		bdata = base64.urlsafe_b64encode(zdata)
		return bdata

	@classmethod
	def deserialize(self, bdata):
		if isinstance(bdata, unicode):
			bdata = bdata.encode('utf8')
		zdata = base64.urlsafe_b64decode(bdata)
		jdata = zlib.decompress(zdata)
		data = json.loads(jdata)
		return data

	@classmethod
	def update_url_query(self, urlstring, data):
		return Url.update_query(urlstring, data)




class Cookies(object):
	@classmethod
	def get(self, name):
		c = response.cookies.get(name)
		return c.value if c else None

	@classmethod
	def set(self, name, value, params={}):
		response.cookies[name] = value

		for key in params.keys():
			v = params[key]
			del params[key]
			params[key.lower()] = v

		if 'max-age' not in params:
			params['max-age'] = 7 * 24 * 3600 * 1000 # 7 days

		for k,v in params.iteritems():
			response.cookies[name][k] = v

	@classmethod
	def delete(self, name):
		response.cookies[name] = ''
		response.cookies[name]['max-age'] = 0




class Request(object):
	@classmethod
	def protocol(self):
		return request.protocol.name.lower()
#		return 'https' if request.environment['SERVER_PORT'] == '443' else 'http'

	@classmethod
	def host(self):
		return request.headers.get('host')

	@classmethod
	def domain(self):
		return '.'.join(self.host().split('.')[1:])

	@classmethod
	def page(self):
		return ''.join(self.query().split('?', 1)[0])

	@classmethod
	def query(self):
		return request.environment.get('REQUEST_URI')

	@classmethod
	def url_parts(self):
		return {
			'protocol' 	: self.protocol(),
			'host' 		: self.host().rstrip('/'),
			'query' 	: self.query().lstrip('/')
		}

	@classmethod
	def current_url(self):
		return '{protocol}://{host}/{query}'.format(**self.url_parts())

	@classmethod
	def get(self, key=None, default=None):
		if key is None:
			data = dict([(k, request.arguments.get(k)) for k in request.arguments])
			return data
		return request.arguments.get(key, default)


	@classmethod
	def remote_ip(self):
		pass


	@classmethod
	def is_e2vdom(self):
		return request.render_type == 'e2vdom'

	@classmethod
	def is_soap(self):
		return request.environment['SCRIPT_NAME'] == '/SOAP'

	@classmethod
	def is_http(self):
		return not self.is_e2vdom() and not self.is_soap()






class Url(object):
	@classmethod
	def current(self):
		return Request.current_url()

	@classmethod
	def join(self, *args):
		args = map(lambda x: x.strip('/'), args)
		return '/'.join(args)

	@classmethod
	def check_protocol(self, url, protocol=None):
		if '://' not in url[:8]:
			protocol = protocol or Request.protocol()
			return protocol + '://' + url

		if not protocol:
			return url

		parts = url.split('://')
		parts[0] = protocol
		return '://'.join(parts)

	@classmethod
	def update_query(self, urlstring, data):
		u = urlparse.urlparse(urlstring)
		query_data = urlparse.parse_qs(u.query)

		delete_args = [k for k,v in data.iteritems() if v is None]
		for key in delete_args:
			del data[key]
			if key in query_data:
				del query_data[key]

		query_data.update(data)
		query_tuples = []

		for key,values in query_data.iteritems():
			if not isinstance(values, list):
				values = [values]

			for value in values:
				query_tuples.append((key, value))

		query = urllib.urlencode(query_tuples)

		u = list(u)
		u[4] = query
		return urlparse.urlunparse(u)

	@classmethod
	def for_page(self, page, args=None):
		parts = Request.url_parts()
		parts['query'] = page.lstrip('/')

		url = '{protocol}://{host}/{query}'.format(**parts)
		if not args: return url

		if isinstance(args, basestring):
			return url + '?' + args.lstrip('?')

		return self.update_query(url, args)



class AppinmailProAdmin(object):
	@classmethod
	def appinmail_user_wrapper(proadmin_user, appinmail_guid=None):
		class ProAdminAppinmailUser(proadmin_user.__class__):
			def __init__(self, proadmin_user, appinmail_guid=None):
				self.proadmin_user = proadmin_user
				self.appinmail_guid = appinmail_guid
				self.access_token = None

			def __getattr__(self, key):
				try:
					return object.__getattr__(self, key)
				except AttributeError:
					pass

				return object.__getattribute__(self.proadmin_user, key)

			def check_password(self, password):
				from md5 import md5

				args = {
					'user_guid' : self.appinmail_guid or self.guid,
					'password_md5' : md5(password).hexdigest()
				}

				appinmail = AppinmailClient.default()
				return appinmail.check_password(args)

		return ProAdminAppinmailUser(proadmin_user, appinmail_guid)

	@classmethod
	def add_application_rule(self, user, right):
		import ProAdmin
		ProAdmin.application().add_rule(user, access=right)

	@classmethod
	def sudo(self, user):
		self.add_application_rule(user, 'a')

	@classmethod
	def current_user(self):
		import ProAdmin
		return ProAdmin.current_user()

	@classmethod
	def create_user(self, user_info):
		import ProAdmin

		users = ProAdmin.application().get_users(email=user_info.get('login'))
		if not users:
			user = ProAdmin.application().create_user(user_info.get('login'))
			user.guid = user_info.get('guid')
		else:
			user = users[0]

		user.notification_email = user_info.get('email')
		user.first_name = user_info.get('first_name')
		user.last_name = user_info.get('last_name')

		user = self.appinmail_user_wrapper(user, appinmail_guid=user_info.get('guid'))
		user.access_token = user_info.get('access_token')

		return user


#		if save: user.save()
#
#		ProAdmin.application().add_rule(subject=user, access='a')
#
#		user = self.create_proadmin_appinmail_user(user, appinmail_guid=user_info.get('guid'))
#		ProAdmin.set_user(user)
#		session['access_token'] = user_info.get('access_token')


	@classmethod
	def set_user(self, user):
		import ProAdmin
		ProAdmin.set_user(user)
		session['access_token'] = user.access_token


