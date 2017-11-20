from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	plugin_id = request.shared_variables["plugin_id"]
	self.action("goTo", ["/plugin_details?plugin_id=" + str(plugin_id) + "&op=export"])


main()
