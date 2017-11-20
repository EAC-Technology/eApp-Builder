from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	res_name = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")
	plugin_id = request.shared_variables["plugin_id"]

	if res_name:
		if cell_name == "Delete":
			response.shared_variables["res_name"] = res_name
			self.dialog_delete_resource.action("show", [])


main()
