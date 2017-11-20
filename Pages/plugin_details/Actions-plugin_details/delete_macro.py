from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_macro import Macros
	from widget_macro import WidgetMacros
	from class_plugins import Plugins

	macros_id = request.shared_variables["macro_id"]
	plugin_id = request.shared_variables["plugin_id"]
	if macros_id:
		macros = Macros.get_by_id(macros_id)
		macros.delete()

	plugin = Plugins.get_by_id(plugin_id)
	macros = plugin.get_macros()
	config_is_exist = False
	for m in macros:
		if m.name == "config":
			config_is_exist = True

	if config_is_exist == True:
		self.button_config.visible = "1"
		self.button_create_config.visible = "0"
	else:
		self.button_config.visible = "0"
		self.button_create_config.visible = "1"

	plugin = Plugins.get_by_id(plugin_id)
	macros = plugin.get_macros()

	widget_macros = WidgetMacros()
	widget_macros.set_data(macros)
	widget_macros.render(self.datatable_macros)

	self.dialog_delete_macro.action("hide", [])
	response.shared_variables["macro_id"] = ""


main()
