from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	macros_id = request.arguments.get("keyField", "")
	cell_name = request.arguments.get("headerData", "")

	if macros_id:
		if cell_name == "Picture":
			self.dialog_uploader.form_uploader.formtext_macro_id.action("setValue", [macros_id] )
			self.dialog_uploader.action("show", [])
		elif cell_name == "Edit_info":
			response.shared_variables["macro_id"] = macros_id
			self.dialog_create_macro.form_macro.formtext_id.action("setValue", [macros_id] )
			self.dialog_create_macro.action("show", [])
		elif cell_name == "Edit_source":
			self.action("goTo",["/macros_source?id="+macros_id])
		elif cell_name == "Delete":
			response.shared_variables["macro_id"] = macros_id
			self.dialog_delete_macro.action("show", [])


main()
