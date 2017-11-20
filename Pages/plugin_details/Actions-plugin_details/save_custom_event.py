from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_custom_event import CustomEvent
	from widget_custom_event import WidgetCustomEvent
	from class_plugins import Plugins

	name = request.arguments.get("formtext_name", "")
	id = request.arguments.get("formtext_id", "")
	plugin_id = request.shared_variables["plugin_id"]
	plugin = Plugins.get_by_id(plugin_id)
	if name:
		custom_event = CustomEvent.get_by_id(id) if id else CustomEvent()
		custom_event.name = name
		custom_event.plugin_guid = plugin.guid
		custom_event.save()
	else:
		self.growl.action("show", ["Error", "Fill custom event name"])



	custom_event_list = plugin.get_custom_event()
	widget_custom_event = WidgetCustomEvent()
	widget_custom_event.set_data(custom_event_list)
	widget_custom_event.render(self.datatable_custom_event)
	self.dialog_add_custom_event.action("hide", [])


main()
