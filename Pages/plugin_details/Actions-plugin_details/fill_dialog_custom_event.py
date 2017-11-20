from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_custom_event import CustomEvent

	custom_event_id = request.shared_variables["custom_event_id"]

	if custom_event_id:
		self.dialog_add_custom_event.form_add_custom_event.formtext_id.value = custom_event_id
		custom_event = CustomEvent.get_by_id(custom_event_id)
		self.dialog_add_custom_event.form_add_custom_event.formtext_name.value = custom_event.name
	else:
		self.dialog_add_custom_event.form_add_custom_event.formtext_id.value = ""
		self.dialog_add_custom_event.form_add_custom_event.formtext_name.value = ""


main()
