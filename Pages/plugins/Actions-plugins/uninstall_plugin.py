from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_plugins import Plugins
	from widget_plugins import WidgetPlugins
	from VEE_resources import delete_plugin_dir

	if "plugin_id" in session and session["plugin_id"]:
		plugin = Plugins.get_by_id(session.get("plugin_id"))
		delete_plugin_dir(plugin.guid)
		plugin.delete()

		widget_plugins = WidgetPlugins()
		plugins_obj = Plugins.get_all()
		widget_plugins.set_data(plugins_obj)
		widget_plugins.render(self.datatable_plugin)

		self.dialog_uninstall.action("hide", [])


main()
