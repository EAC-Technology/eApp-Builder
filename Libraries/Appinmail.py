from vdom_debug import *

from md5 import md5
from appinmail_sso_client import AppinmailClient, Config




_apiconnection = None

def appinmail_api():
	global _apiconnection

	if _apiconnection is None:
		import ProMail
		host = Config.get('host') or ProMail.cloud_domain('admin.appinmail.io')
		_apiconnection = AppinmailClient(host)

	return _apiconnection







def ping():
	try:
		return appinmail_api().ping() == '1'
	except:
		return False


def login(username, password):
	import ProAdmin

	proadmin_user = ProAdmin.current_user()
	if not proadmin_user: return None

	try:
		user = appinmail_api().remote_login({'user_login' : username, 'password_md5' : md5(password).hexdigest()})
		if not user: return None

		proadmin_user.appinmail_guid = user.get('guid')
		return user

	except:
		pass

	return None


def current_user():
	import ProAdmin
	user = ProAdmin.current_user()

	if not user:
		return None

	if not hasattr(user, 'appinmail_guid'):
		return None

	return users.get_by_guid(user.appinmail_guid)


def create_short_url(url):
	return appinmail_api().create_short_url({'url' : url})




class auth(object):
	@classmethod
	def is_valid_access_token(self, token):
		return appinmail_api().auth_is_valid_access_token(token)



class acl(object):
	@classmethod
	def register_eac(self, eac_guid=None):
		user = current_user()
		user_guid = user.get('guid')

		data = {'user_guid' : user_guid}
		if eac_guid:
			data['eac_guid'] = eac_guid

		return appinmail_api().acl_register_eac(data)

	@classmethod
	def delete_eac(self, eac_guid):
		return appinmail_api().acl_delete_eac({'eac_guid' : eac_guid})

	@classmethod
	def check(self, eac_guid, users_ids, rights=None):
		return appinmail_api().acl_check({'eac_guid' : eac_guid, 'user_guid' : users_ids, 'rights' : rights})

	@classmethod
	def add(self, eac_guid, users_ids, rights):
		return appinmail_api().acl_add({'eac_guid' : eac_guid, 'user_guid' : users_ids, 'rights' : rights})

	@classmethod
	def delete(self, eac_guid, users_ids, rights=None):
		return appinmail_api().acl_delete({'eac_guid' : eac_guid, 'user_guid' : users_ids, 'rights' : rights})




class users(object):
	@classmethod
	def create_by_email(self, emails):
		return appinmail_api().users_create({'email' : emails})

	@classmethod
	def get_by_guid(self, args):
		return appinmail_api().users_get({'guid' : args})

	@classmethod
	def get_by_email(self, args):
		return appinmail_api().users_get({'email' : args})

	@classmethod
	def get_by_login(self, args):
		return appinmail_api().users_get({'login' : args})

	@classmethod
	def get_by_pisid(self, args):
		return appinmail_api().users_get({'pis_id' : args})

	@classmethod
	def resolve(self, args):
		return appinmail_api().users_get({'resolve' : args})



