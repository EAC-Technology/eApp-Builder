import json

from vdom_remote_api import VDOMService
from appinmail_sso_utils import Utils, Request, Url

from appinmail_config import Config

#class Config(object):
#	_instance = None
#
#	FILENAME = 'appinmail_sso.json'
#
#	@classmethod
#	def read(self):
#		if not application.storage.exists(self.FILENAME):
#			return None
#		return application.storage.readall(self.FILENAME)
#
#	@classmethod
#	def write(self, data):
#		application.storage.write(self.FILENAME, data)
#
#	@classmethod
#	def load(self):
#		try:
#			return json.loads(self.read())
#		except:
#			return None
#
#	@classmethod
#	def flush(self, data):
#		self.write(json.dumps(data))
#
#
#	@classmethod
#	def get(self, key=None, default=None):
#		if self._instance is None:
#			self._instance = self.load()
#
#		if self._instance is None:
#			return None
#
#		return self._instance.get(key, default) if key else self._instance
#
#	@classmethod
#	def get_config(self, key=None, default=None):
#		return self.get(key, default)
#
#	@classmethod
#	def set(self, key, value):
#		if self._instance is None:
#			self._instance = {}
#
#		self._instance[key] = value
#
#	@classmethod
#	def save(self, data=None):
#		data = data or self._instance
#		if not data: return
#
#		self.flush(data)
#		self._instance = data
#
#	@classmethod
#	def delete(self):
#		self.write('null')
#		self._instance = None
#
#	@classmethod
#	def create_test_config(self):
#		Config.save({u'api_host': u'admin.appinmail.pw', 'sso_host' : 'admin.appinmail.pw'})
#



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

	def __init__(self, host=None):
		self.host = host or Config.get('api_host') or Config.get('host') or 'https://admin.appinmail.io'
		self._api = None

	@property
	def api(self):
		if self._api is None:
			self._api = self.API(self.host)
		return self._api

	def call(self, method, args=None):
		return self.api(method, args)

	def json_call(self, method, args=None):
#		if method == 'auth_token' : raise Exception(1)
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
	def default(self):
		if self._instance is None:
			self._instance = AppinmailClient()
		return self._instance

	@classmethod
	def reset(self):
		self._instance = None



def create_proadmin_appinmail_user(user, appinmail_guid=None):
	class ProAdminAppinmailUser(user.__class__):
		def __init__(self, proadmin_user, appinmail_guid=None):
			self.proadmin_user = proadmin_user
			self.appinmail_guid = appinmail_guid

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

	return ProAdminAppinmailUser(user, appinmail_guid)



class SSOClient(object):
	@classmethod
	def is_appinmail_sso(self):
		return Config.get('host') is not None and Config.get('active')


	@classmethod
	def current_protocol(self):
		return Request.protocol()

	@classmethod
	def check_url_protocol(self, url):
		return Url.check_protocol(url)

	@classmethod
	def current_url(self):
		return Url.check_protocol(Request.current_url(), 'https')



	@classmethod
	def sso_url(self, action):
		args = {'continue_url' : self.current_url()}
		host = Config.get('host')

		url = Url.join(host, action)
		url = Url.update_query(url, {'sso' : Utils.serialize(args)})
		return Url.check_protocol(url, 'https')

	@classmethod
	def sso_redirect(self, url):
		response.redirect(url)




	@classmethod
	def sso_request(self, a):
		pass






	@classmethod
	def get_auth_token(self):
		return request.arguments.get('auth_token')

	@classmethod
	def get_proadmin_user(self):
		import ProAdmin
		return ProAdmin.current_user()

	@classmethod
	def set_proadmin_user(self, user_info, save=True):
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
		if save: user.save()

		ProAdmin.application().add_rule(subject=user, access='a')

		user = create_proadmin_appinmail_user(user, appinmail_guid=user_info.get('guid'))
		ProAdmin.set_user(user)
		session['access_token'] = user_info.get('access_token')


	@classmethod
	def login_auth_token(self, auth_token_key, redirect=True):
		appinmail = AppinmailClient.default()
		user_info = appinmail.auth_token(auth_token_key)

		if user_info:
			self.set_proadmin_user(user_info)
			return True

		return False


	@classmethod
	def success_login(self):
		back_url = request.arguments.get('back_url') or '/home'
		response.redirect(back_url)


	@classmethod
	def login(self):
		if not self.is_appinmail_sso():
			return

		if self.get_proadmin_user():
			return self.success_login()

		# sso_host = request.arguments.get('sso_host')
		# if sso_host:
		# 	sso_host = Utils.deserialize(sso_host)
		# 	if Config.get('host') != sso_host:
		# 		Config.set('host', 'sso_host')
		# 		Config.save()

		auth_token = self.get_auth_token()

		if auth_token and self.login_auth_token(auth_token):
			return self.success_login()

		url = self.sso_url('/login')
		self.sso_redirect(url)

	@classmethod
	def sso_logoff_complete(self):
		status = request.arguments.get('status')
		return bool(status)

	@classmethod
	def logoff(self):
		if not self.is_appinmail_sso():
			return

		import ProAdmin
		ProAdmin.logoff()

		url = self.sso_url('/logoff')
		self.sso_redirect(url)





SSO = SSOClient




def test_promail_clean():
	for db_name in application.databases.get_list().values():
		db = getattr(application.databases, db_name, None)
		if not db: continue

		for table_name in db.get_list():
			db.commit('delete from {0}'.format(table_name))

	from prosuite_app_cleaner import ApplicationCleaner
	cleaner = ApplicationCleaner()
	cleaner.clean_storage = True
	cleaner.clean_vee_engine = True

#	import ProAdmin
#	ProAdmin.scheme().connection.recreate()

	from promail_orm import Mailbox

	mailboxes = list(Mailbox.select())
	for m in mailboxes:
		m.remove()

	response.write('<pre>promail clean - done</pre>')




















