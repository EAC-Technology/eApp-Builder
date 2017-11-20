import ProAdmin
from class_remote_settings import RemoteSettings
import localization
lang = localization.get_lang()

try:

	if RemoteSettings.get_remote_setting():
		RemoteSettings.delete()
		ProAdmin.logoff()
		ProAdmin.unregister_default_scheme()
		ProAdmin.scheme()
		self.action("goTo",["/proadmin_management"])

except Exception, ex:
	self.growl.action( 'show', [ lang["error_title"], str(ex) ] )