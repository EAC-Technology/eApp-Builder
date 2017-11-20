import re

import ProAdmin
import Appinmail
from models import Application

from VEE_utils import AutoCast, encodeUTF8
from VEE_std_lib import base_object
from vscript import generic, version


class v_application(generic):

	@AutoCast
	def v_getnamebyguid(self, app_guid=None):
		app = Application.get(guid=app_guid)
		return "<not_found>" if not app else app.name


class v_workspace(generic):
	pass


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
