from class_license import License
import localization

lang = localization.get_lang()
eng_license = """This software and documentation are the property of VDOM Box International. It is forbidden to translate, decompile, modify, adapt and correct. You may not remove or modify the license information and transmit it to others. The rental and lending of the software are prohibited. You can not use this software on other hardware that comes with it. The author alone is authorized to perform these operations.
If you do one of the above, your rights are automatically terminated and the author may have recourse to justice.
You are allowed to possess for the purpose of backup only copies of the XML file representing the application on other storage media than those included in the hardware running the application. You are not allowed to make copies of paper documentation.
You may install and use the software on one device running the application server VDOM (usually a VDOM Box). The license of this software is associated with a unique user ID stored on the smart card fitted to the VDOM Box, you do not use the license for this software to another user with a unique identifier different.
License transfer. To transfer the license of the software on another single user, it must first be removed from the smart card allows the previous user, this transfer can be done by the distributor of this license.
Using this software, you agree to abide by copyright, and to ensure that others respect them themselves.
This software is protected in France by the laws on intellectual property and abroad by international conventions on copyright (Berne Convention).
Violation of any of the rights of the author of the software is an infringement punishable in France by Article L335-2 of the Code of intellectua property.
The software is provided as is without warranty. The author can not be held liable for damages of any kind whatsoever suffered by the user or third parties arising directly or indirectly from its use, including loss of data, or any financial loss resulting from its use or inability to use, and this even if the author has been advised of the possibility of such damages. In any case, the responsibility of the author may not exceed the amount paid to acquire the license.
If the proposed software is presented as an update, you must already be licensed before the same software to benefit. A full update or replace the license and the previous version of the software. The update and the original license must be regarded as a single product. You are not authorized to sell or give separately."""

#if License().confirmed and False:
if License().confirmed and False:
	response.redirect("/login")
else:
	if session.get("from_license_page") and session["from_license_page"] == "1":
		self.dialog.hypertext_lisence.visible = "0"
		self.dialog.form_selector.visible = "1"
		self.dialog.button_agree.visible = "0"
		self.dialog.button_disagree.visible = "0"
		session["from_license_page"] = "0"
	else:
		self.dialog.text1.visible = "0"
		self.dialog.hypertext_lisence.htmlcode = lang.get("license", eng_license).format(application.name)

#	self.growl.title = lang["error"]
#	self.growl.text = localization.current_language()
#	self.growl.active = "1"
text = {
	"agree_button"				: [ self.dialog.button_agree ],
	"disagree_button"			: [ self.dialog.button_disagree ],
	"close_button"				: [ self.dialog_disagree.button_close ],
	"disagree_warning"			: [ self.dialog_disagree.hypertext_disagree ],
	"select_operation_mode"		: [ self.dialog.form_selector.text1 ],
	"standalone_mode"			: [ self.dialog.form_selector.formradiogroup_selector.formradiobutton_local ],
	"proadmin_mode"				: [ self.dialog.form_selector.formradiogroup_selector.formradiobutton_remote ],
	"proadmin_page_warning"		: [ self.dialog.form_remote.text_title ],
	"go_button"					: [ self.dialog.form_remote.btn_remote_settings ],
	"password_title"			: [ self.dialog.form_local.text_title ],
	"password_field"			: [ self.dialog.form_local.text_password ],
	"confirm_password_field"	: [ self.dialog.form_local.text_confirmation ],
	"apply_password"			: [ self.dialog.form_local.formbutton_apply ],
}
for k, v in text.items():
	for element in v:
		if 'htmlcode' in dir( element ):
			element.htmlcode = lang[k]
		elif 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]
