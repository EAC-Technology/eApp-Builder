from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from widget_resource import WidgetResource
	from class_plugins import Plugins
	from VEE_resources import ResourceFolderManager

	plugin_id = request.shared_variables["plugin_id"]
	res_name = request.shared_variables["res_name"]
	if plugin_id and res_name:
		plugin = Plugins.get_by_id(int(plugin_id))
		ResourceFolderManager(plugin.guid).delete_res(res_name)

		widget_resource = WidgetResource()
		widget_resource.set_data(ResourceFolderManager(plugin.guid).resourcelist, plugin.guid)
		widget_resource.render(self.datatable_resource)


	self.dialog_delete_resource.action("hide", [])
	response.shared_variables["res_name"] = ""


main()
