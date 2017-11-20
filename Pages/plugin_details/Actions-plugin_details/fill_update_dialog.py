from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_plugins import Plugins
	plugin_id = request.shared_variables["plugin_id"]
	if plugin_id:
		plugin = Plugins.get_by_id(plugin_id)

		self.dialog_update_plugin.text_description.action( "setText", [ "Plugin to update - %s" % ( plugin.name ) ] )
		self.dialog_update_plugin.form.formtext_pluginid.action( "setValue", [ plugin.id ])


main()
