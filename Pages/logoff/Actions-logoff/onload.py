from class_license import License
import ProAdmin
import localization
lang = localization.get_lang()
try:
	#License().confirmed = ''
	if not License().confirmed:
		response.redirect("/license.vdom")
	self.dialog_information.text_caption.value = lang.get("logoff_caption","You have been logged off")
	self.dialog_information.text_message.value = lang.get("logoff_message","You will be redirected to the login page in few seconds")

	ProAdmin.logoff()

	back_url = request.arguments.get( 'back_url', '' )
	if back_url:
		session[ 'back_url' ] = back_url
except Exception, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["unknown_error"]
	self.growl.active = "1"
