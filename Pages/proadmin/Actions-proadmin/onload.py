from proadmin_utils import Utils
import localization

lang = localization.get_lang()

class SilenException( Exception ):
	pass



try:
	# process ping command
	if 'ping' in request.arguments:
		response.write( Utils.ping(), True )
		raise SilenException()

	# check admin rights
	if not Utils.is_admin():
		self.login_dialog.show = '1'
	else:
		self.login_dialog.show = '0'
		self.dialog_selection.show = '1'


except SilenException:
	pass


text = {
	"system_login_title"	: [ self.login_dialog.login_form.text_system_login ],
	"system_account"		: [ self.login_dialog.login_form.login_label ],
	"password"				: [ self.login_dialog.login_form.password_label ],
	"login_btn"				: [ self.login_dialog.login_form.submit_button ],
	"users_container_label"	: [ self.dialog_selection.btn_cont_2.btn_users_groups ],

}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]