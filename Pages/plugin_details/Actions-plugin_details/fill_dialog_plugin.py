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

		#self.dialog_create.action("setTitle", ["Edit plugin"])
		self.dialog_create.form_update.formtext_id.value = plugin_id
		self.dialog_create.form_update.formtext_name.value = plugin.name
		self.dialog_create.form_update.formtext_author.value = plugin.author
		self.dialog_create.form_update.formtextarea_description.value = plugin.description
		self.dialog_create.form_update.formtext_version.value = plugin.version
		self.dialog_create.form_update.hpt.htmlcode = "<img src='/get_image?id=%s'/>"%plugin.picture if plugin.picture else ""


main()
