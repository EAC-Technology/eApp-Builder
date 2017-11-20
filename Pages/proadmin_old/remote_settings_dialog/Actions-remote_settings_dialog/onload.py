from proadmin_remote_settings import RemoteSettings
from proadmin_utils import Utils

class SilentException( Exception ):
	pass

try:
	# there are no remote settings in ProAdmin application
	if Utils.is_proadmin():
		raise SilentException()

	# check user rights
	if not Utils.is_admin():
		self.remotesettings_form.visible = '0'
		raise SilentException()

	# setup form fields
	try:
		remote = RemoteSettings.get_remote_settings()
	except:
		remote = None

	if remote:
		self.remotesettings_form.server.value = remote.server
		self.remotesettings_form.login.value = remote.login
		self.remotesettings_form.password.value = '*'*8

except SilentException:
	pass