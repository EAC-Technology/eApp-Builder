import ProAdmin
from widget_proadmin_users import WidgetProAdminUsers
from proadmin_utils import Utils
import localization

lang = localization.get_lang()

if not Utils.is_admin():
	response.redirect("/proadmin.vdom")

current_user = ProAdmin.current_user()
if current_user:
	self.text_greating.visible = "1"
	self.bar.visible = "1"
	self.text_greating.value = lang["greating_title"] % current_user.get_name()
	self.button_logout.visible = "1"
	self.button_logout.hint = lang["logout_hint"]
else:
	self.text_greating.visible = "0"
	self.bar.visible = "0"
	self.button_logout.visible = "0"


proadmin_users_widget = WidgetProAdminUsers().render(self.datatable_users, self.pager)

text = {
	"user_not_logged_in"			: [ self.text_not_logged ],
	"user_management"				: [ self.page_title ]
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]
