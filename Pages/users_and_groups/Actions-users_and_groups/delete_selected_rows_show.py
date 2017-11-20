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

		from widget_user_and_group_delete_dialog import WidgetUserAndGroupDeleteDialog
		widget = WidgetUserAndGroupDeleteDialog(
							selectedRows,
							request.shared_variables[ "currentTab" ]
					)

		widget.render(	 self.dialog_delete_user_group,
						 self.dialog_delete_user_group.hpt_result )


main()
