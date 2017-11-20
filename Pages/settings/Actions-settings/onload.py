from class_acl_user import ACLUser
from class_license import License
from class_errors import AccessDeniedError, AuthorisationError, RemoteSchemeProtection
from utils.card_connect import get_system_attribute
from config import proshare_config
import localization


class UserNotAdmin( Exception ):
	pass

#Starter Mode: plugins are not available
#On the dev server attr_id = 159
#On the production server attr_id = 162
lang = localization.get_lang()
#try:
#	server_type = proshare_config["server_type"]
#	if server_type == "dev":
#		attr_id = "159"
#	elif server_type == "production":
#		attr_id = "162"
#	else:
#		self.growl.title = "Warning"
#		self.growl.text = 'Application not well configured. Plugins management is not available.'
#		self.growl.active = "1"
#
#	starter_flag = get_system_attribute( attr_id )
#
#	if starter_flag == "0":
#		self.btn_cont_5.visible = "1"
#	elif starter_flag == "1":
#		self.btn_cont_5.visible = "0"
#	else:
#		self.btn_cont_5.visible = "0"
#		self.growl.title = "Warning"
#		self.growl.text = 'Application not well configured. Plugins management is not available.'
#		self.growl.active = "1"
#except Exception, ex:
#	self.growl.title = lang["error"]
#	self.growl.text = lang["unknown_error"]
#	self.growl.active = "1"

try:
	user = ACLUser.current()
	if not user.is_admin():
		raise UserNotAdmin()

except AuthorisationError, ex:
	session[ "error" ] = unicode(ex)
	response.redirect("/logoff")

except AccessDeniedError, ex:
	response.redirect( '/home' )

except Exception, ex:
	response.redirect( '/' )



from widget_localization import LocalizationWidget
localization = LocalizationWidget()
localization.add_controls( 'settings_page_title',			self )
localization.add_controls( 'settings_rules_btn',			self.btn_cont_2.btn_rules )
localization.add_controls( 'settings_users_groups_btn',		self.btn_cont_3.btn_users_groups )
localization.add_controls( 'settings_remote_control_btn',	self.btn_cont_4.btn_remote )
localization.render()
