import re

import ProAdmin
import Appinmail

from VEE_utils import AutoCast, encodeUTF8
from VEE_std_lib import base_object
from vscript import generic, version



class v_acl_api(generic):
	@AutoCast
	def v_registereac(self, eac_guid=None):
		return Appinmail.acl.register_eac(eac_guid)

	@AutoCast
	def v_deleteeac(self, eac_guid):
		return Appinmail.acl.delete_eac(eac_guid)

	@AutoCast
	def v_check(self, eac_guid, user_guid, rights=None):
		return Appinmail.acl.check(eac_guid, user_guid, rights)

	@AutoCast
	def v_add(self, eac_guid, users_ids, rights):
		return Appinmail.acl.add(eac_guid, users_ids, rights)

	@AutoCast
	def v_delete(self, eac_guid, users_ids, rights=None):
		return Appinmail.acl.delete(eac_guid, users_ids, rights)




class v_users_api(generic):
	@AutoCast
	def v_createbyemail(self, emails):
		return Appinmail.users.create_by_email(emails)

	@AutoCast
	def v_getbyguid(self, args):
		return Appinmail.users.get_by_guid(args)

	@AutoCast
	def v_getbyemail(self, args):
		return Appinmail.users.get_by_email(args)

	@AutoCast
	def v_getbylogin(self, args):
		return Appinmail.users.get_by_login(args)

	@AutoCast
	def v_getbypisid(self, args):
		return Appinmail.users.get_by_pisid(args)

	@AutoCast
	def v_resolve(self, args):
		return Appinmail.users.resolve(args)




class v_utils_api(generic):
	@AutoCast
	def v_currenthost(self):
		host = request.headers.get('host')
		return re.sub(r'\-\d+\.', '.', host)  # remove port number: {app_name}-pis{pis_id}-{port_number}.domain

	@AutoCast
	def v_parseemails(self, args, key='toemail'):
		email = args.get(key)
		res = email.split(',') if email else []

		pattern = re.compile(r'{0}\[(.*)\]'.format(key))
		mm = map(pattern.match, args.keys())
		mm = filter(None, mm)

		return res + [m.group(1) for m in mm]

	@AutoCast
	def v_getvaluesbykey(self, data, key):
		if not isinstance(data, list):
			return data[key]
		return map(lambda x: x[key], data)






class v_appinmail(generic):
	def __init__(self):
		self.v_acl = v_acl_api()
		self.v_users = v_users_api()
		self.v_utils = v_utils_api()

	@AutoCast
	def v_login(self, username, password):
		return Appinmail.login(username, password)

	@AutoCast
	def v_currentuser(self):
		return Appinmail.current_user()

#		user = ProAdmin.current_user()
#
#		user_info = {
#			'guid' 				 : user.appinmail_guid,
#			'first_name' 		 : user.first_name,
#			'last_name' 		 : user.last_name,
#			'email' 			 : user.notification_email,
#			'login' 			 : user.email,
#		}
#
#		return user_info


	@AutoCast
	def v_ping(self):
		return Appinmail.ping()

	@AutoCast
	def v_createshorturl(self, url):
		return Appinmail.create_short_url(url)


#	@AutoCast
#	def v_getuser(self, args):
#		return self.api.get_appinmail_user(args)

#	@AutoCast
#	def v_createaccesstoken(self, args):
#		return self.api.create_access_token(args)




environment = (
	('v_appinmail', v_appinmail()),
)
