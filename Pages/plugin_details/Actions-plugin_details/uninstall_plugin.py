from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_plugins import Plugins
	from VEE_resources import delete_plugin_dir

	plugin_id = request.shared_variables["plugin_id"]

	if plugin_id:
		plugin = Plugins.get_by_id(plugin_id)
		delete_plugin_dir(plugin.guid)
		plugin.delete()

		self.dialog_uninstall.action("hide", [])
		self.action("goTo", ["/plugins.vdom"])

	response.shared_variables["plugin_id"]


main()
