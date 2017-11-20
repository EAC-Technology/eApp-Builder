import json
import zlib
import base64

from vdom_remote_api import VDOMService


class AppinmailAPIError(Exception): pass

class AppinmailClient(object):
	APP_ID = 'f706ee35-6bc3-4aa9-9b68-c182025e5dd3'
	API_ID = '9d29fd1a-ae9b-4b92-8c2f-72c15d18dcf6'

	_instance = None

	class API(object):
		USER = 'appinmail_api'
		PASSWORD_HASH = '2ab4ac3348b06e078442eb5f2e7b4a85'

		def __init__(self, host):
			self.service = VDOMService.connect(host, self.USER, self.PASSWORD_HASH, AppinmailClient.APP_ID)

		def __call__(self, method, args=None):
			try:
				return self.service.call(AppinmailClient.API_ID, method, args)
			except:
				self.service.open_session()
			return self.service.call(AppinmailClient.API_ID, method, args)

	def __init__(self, host):
		if '://' in host:
			host = host.split('://', 1)[1]

		self.host = host
		self._api = None

	@property
	def api(self):
		if self._api is None:
			self._api = self.API(self.host)
		return self._api

	def call(self, method, args=None):
		return self.api(method, args)

	def json_call(self, method, args=None):
		args = args or ''
		args = json.dumps(args)

		resp = self.call(method, args)

		try:
			status, res = json.loads(resp)
			if status == 'error':
				raise AppinmailAPIError(res)
			return res

		except (ValueError, TypeError):
			return resp

	def __getattr__(self, key):
		try:
			return object.__getattr__(self, key)
		except AttributeError:
			pass

		return lambda *args: self.json_call(key, *args)


	@classmethod
	def default(self, host=None):
		if self._instance is None:
			self._instance = AppinmailClient(host)
		return self._instance

	@classmethod
	def reset(self):
		self._instance = None





class AppinmailSSO(object):
	@classmethod
	def session(self):
		if 'appinmail_sso_data' not in session:
			session['appinmail_sso_data'] = {}
		return session['appinmail_sso_data']

	@classmethod
	def _serialize(self, data):
		jdata = json.dumps(data)
		zdata = zlib.compress(jdata)
		bdata = base64.urlsafe_b64encode(zdata)
		return bdata

	@classmethod
	def _deserialize(self, bdata):
		if isinstance(bdata, unicode):
			bdata = bdata.encode('utf8')
		zdata = base64.urlsafe_b64decode(bdata)
		jdata = zlib.decompress(zdata)
		data = json.loads(jdata)
		return data

	@classmethod
	def current_url(self):
		protocol = request.protocol.name.lower()
		host = request.headers.get('host')
		query = request.environment.get('REQUEST_URI')
		return '{}://{}/{}'.format(protocol, host, query.lstrip('/'))

	@classmethod
	def sso_host(self):
		return self.session().get('sso_host')

	@classmethod
	def sso_request(self, action):
		host = self.sso_host().rstrip('/')
		action = action.lstrip('/')

		args = {'continue_url' : self.current_url()}
		url = '{}/{}?sso={}'.format(host, action, self._serialize(args))

		response.redirect(url)


	@classmethod
	def current_user(self):
		return self.session().get('current_user')

	@classmethod
	def access_token(self):
		return self.session().get('access_token')



	@classmethod
	def auth_by_token(self):
		token = request.arguments.get('auth_token')
		if not token: return False

		user_info = AppinmailClient.default(self.sso_host()).auth_token(token)
		if user_info:
			self.session()['current_user'] = user_info
			self.session()['access_token'] = user_info.get('access_token')
			return True

		return False



	@classmethod
	def authorize(self, host):
		self.session()['sso_host'] = host

		if self.auth_by_token():
			return

		self.sso_request('/login')


	@classmethod
	def logoff(self):
		if 'appinmail_sso_data' in session:
			del session['appinmail_sso_data']

