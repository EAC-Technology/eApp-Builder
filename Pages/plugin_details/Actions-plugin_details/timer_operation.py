from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	timer_id = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")

	if timer_id:
		if cell_name == "Edit":
			response.shared_variables["timer_id"] = timer_id
			self.dialog_add_timer.action("show", [])
		elif cell_name == "Delete":
			response.shared_variables["timer_id"] = timer_id
			self.dialog_delete_timer.action("show", [])


main()
