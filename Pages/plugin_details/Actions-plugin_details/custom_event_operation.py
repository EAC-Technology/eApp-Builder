from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	custom_event_id = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")

	if custom_event_id:
		if cell_name == "Edit":
			response.shared_variables["custom_event_id"] = custom_event_id
			self.dialog_add_custom_event.action("show", [])
		elif cell_name == "Delete":
			response.shared_variables["custom_event_id"] = custom_event_id
			self.dialog_delete_custom_event.action("show", [])


main()
