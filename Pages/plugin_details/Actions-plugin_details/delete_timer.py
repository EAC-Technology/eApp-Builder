from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_timer import Timer
	from widget_plugins import WidgetPlugins
	from widget_timer import WidgetTimer
	from class_plugins import Plugins
	plugin_id = request.shared_variables["plugin_id"]
	timer_id = request.shared_variables["timer_id"]
	if timer_id:
		timer = Timer.get_by_id(timer_id)
		timer.delete()

	plugin = Plugins.get_by_id(plugin_id)
	timer = plugin.get_timer()

	widget_timer = WidgetTimer()
	widget_timer.set_data(timer)
	widget_timer.render(self.datatable_timer)

	self.dialog_delete_timer.action("hide", [])
	response.shared_variables["timer_id"]


main()
