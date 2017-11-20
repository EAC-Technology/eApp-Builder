from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_macro import Macros
	from widget_plugins import WidgetPlugins
	from widget_macro import WidgetMacros
	from class_plugins import Plugins

	plugin_id = request.shared_variables["plugin_id"]
	plugin = Plugins.get_by_id(plugin_id)

	macros = Macros()
	macros.name 		= "config"
	macros.class_name	= ""
	macros.timer_guid 	= ""
	macros.is_button_macros = "1"
	macros.on_board 	= "1"
	macros.description 	= "config macro"
	macros.plugin_guid = plugin.guid
	macros.save()

	plugin = Plugins.get_by_id(plugin_id)
	macros = plugin.get_macros()

	widget_macros = WidgetMacros()
	widget_macros.set_data(macros)
	widget_macros.render(self.datatable_macros)

	self.button_create_config.visible = "0"
	self.button_config.visible = "1"


main()
