from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_plugins import Plugins
	from class_macro import Macros
	from VEE_resources import create_plugin_dir


	def invoke_dispather( macros ):

		from VEE_vmacro_dispatcher import InvokeDispatcher
		from VEE_std_lib import v_currentpage

		invoke_disp = InvokeDispatcher()
		invoke_disp.page 		= self
		invoke_disp.growl 		= self.growl
		invoke_disp.xmldialog 	= self.xmldialog
		invoke_disp.macros 		= macros

		current_page = v_currentpage()
		current_page.page_name = self.name

		invoke_disp.current_page = current_page
		invoke_disp.run()


	plugin_id = session["plugin_id"] = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")

	if plugin_id:
		plugin = Plugins.get_by_id(plugin_id)

		if cell_name and plugin:

			if cell_name == "Update":
				self.dialog_update_plugin.text_description.action( "setText", [ "Plugin to update - %s" % ( plugin.name )] )
				self.dialog_update_plugin.form.formtext_pluginid.action( "setValue", [ plugin.id ])
				self.dialog_update_plugin.action( "show", [ "" ] )

			elif cell_name == "Export":
				self.action("goTo", ["/plugins?op=export"])

			elif cell_name == "Open":
				create_plugin_dir(plugin.guid)
				self.action("goTo", ["/plugin_details?id=%s"%plugin_id])

			elif cell_name == "Delete":
				session["plugin_id"] = plugin_id
				self.dialog_uninstall.action("show", [])

			elif cell_name == "MD5":
				self.dialog_md5.text_md5.action("setText", [plugin.get_md5()])
				self.dialog_md5.action("show", [])

			elif cell_name == "Config":
				from class_macro import Macros
				macros = Macros.get_config_macro( plugin.guid )
				if macros:
					invoke_dispather( macros )


main()
