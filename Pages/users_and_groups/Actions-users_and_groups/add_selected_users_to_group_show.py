from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	import json

	selectedRows = request.shared_variables[ "selectedRows" ]
	selectedRows = [] if not selectedRows else selectedRows

	if not selectedRows:
		import localization
		lang = localization.get_lang()
		self.growl.action( "show", [ lang[ "warning_title" ], lang[ "select_objects_error" ] ] )

	else:

		from widget_add_users_to_group_dialog import WidgetAddUsersToGroupDialog
		widget = WidgetAddUsersToGroupDialog(
							selectedRows
					)

		widget.render(	 self.dialog_add_to_group,
						 self.dialog_add_to_group.form_add_to_group.formlist_groups,
						 self.dialog_add_to_group.form_add_to_group.cont.list_users,
						 self.dialog_add_to_group.form_add_to_group.new_group_name
						)


main()
