from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from widget_plugin_db import WidgetPluginDB
	from class_plugins import Plugins
	from VEE_sqlite3 import DatabaseManager

	plugin_id = request.shared_variables["plugin_id"]
	db_name = request.shared_variables["db_name"]

	if plugin_id and db_name:
		plugin = Plugins.get_by_id(int(plugin_id))
		DatabaseManager(plugin.guid).delete_db(db_name)

		widget_db = WidgetPluginDB()
		widget_db.set_data(DatabaseManager(plugin.guid).databaselist)
		widget_db.render(self.datatable_db)

	self.dialog_delete_db.action("hide", [])
	response.shared_variables["db_name"] = ""


main()
