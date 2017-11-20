from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_custom_event import CustomEvent
	from widget_plugins import WidgetPlugins
	from widget_custom_event import WidgetCustomEvent
	from class_plugins import Plugins
	plugin_id = request.shared_variables["plugin_id"]
	custom_event_id = request.shared_variables["custom_event_id"]
	if custom_event_id:
		custom_event = CustomEvent.get_by_id(custom_event_id)
		custom_event.delete()

	plugin = Plugins.get_by_id(plugin_id)
	custom_event_list = plugin.get_custom_event()

	widget_custom_event = WidgetCustomEvent()
	widget_custom_event.set_data(custom_event_list)
	widget_custom_event.render(self.datatable_custom_event)

	self.dialog_delete_custom_event.action("hide", [])
	response.shared_variables["custom_event_id"] = ""


main()
