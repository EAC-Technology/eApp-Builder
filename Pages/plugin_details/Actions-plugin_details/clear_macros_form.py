from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():
	self.dialog_create_macro.form_macro.formtext_name.value = ""
	self.dialog_create_macro.form_macro.formtextarea_description.value = ""
	self.dialog_create_macro.form_macro.formtext_id.value = ""


main()
