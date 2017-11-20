from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_timer import Timer
	from widget_timer import WidgetTimer
	from class_plugins import Plugins

	name = request.arguments.get("formtext_name", "")
	period = request.arguments.get("formtext_period", "")
	id = request.arguments.get("formtext_id", "")
	period_list = period.split(":")

	plugin_id = request.shared_variables["plugin_id"]
	plugin = Plugins.get_by_id(plugin_id)

	timer = Timer.get_by_id(id) if id else Timer()
	timer.name = name
	timer.period = period
	timer.plugin_guid = plugin.guid
	timer.save()

	timer_list = plugin.get_timer()
	widget_timer = WidgetTimer()
	widget_timer.set_data(timer_list)
	widget_timer.render(self.datatable_timer)
	self.dialog_add_timer.action("hide", [])


main()
