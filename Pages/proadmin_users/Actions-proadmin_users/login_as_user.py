import ProAdmin
import localization

lang = localization.get_lang()

guid = request.arguments.get("keyField", )
if guid:
	user = ProAdmin.application().get_subject( guid )
	ProAdmin.set_user( user )

	self.text_greating.visible = "1"
	self.bar.visible = "1"
	self.text_greating.value = lang["greating_title"] % user.name
	self.button_logout.visible = "1"
	self.button_logout.hint = lang["logout_hint"]