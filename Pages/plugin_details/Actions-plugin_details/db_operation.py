from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	db_name = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")
	plugin_id = request.shared_variables["plugin_id"]

	if db_name:
		if cell_name == "Export":
			self.action("goTo", ["/plugin_details?plugin_id=" + str(plugin_id) + "&db=" + str(db_name) + "&op=export_db"])
		elif cell_name == "Import":
			self.dialog_update_db.form_db.formtext_old_db_name.action("setValue", [db_name] )
			self.dialog_update_db.action("show", [])
		elif cell_name == "Delete":
			response.shared_variables["db_name"] = db_name
			self.dialog_delete_db.action("show", [])


main()
