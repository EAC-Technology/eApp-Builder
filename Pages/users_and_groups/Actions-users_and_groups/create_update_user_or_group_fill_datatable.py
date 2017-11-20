from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	obj_type = request.shared_variables[ "obj_type" ]
	count_text = datatable = error_text = search_obj_type = None

	if obj_type == "user":
		search_obj_type = "group"
		count_text = self.dialog_user.groups_cont.groups_count
		datatable = self.dialog_user.groups_cont.cont.datatable_groups
		error_text = self.dialog_user.groups_cont.cont.error_text
		throbber_image = self.dialog_user.groups_cont.cont.throbber_image
	else:
		search_obj_type = "user"
		count_text = self.dialog_group.cont.users_count
		datatable = self.dialog_group.cont.cont.datatable_users
		error_text = self.dialog_group.cont.cont.error_text
		throbber_image = self.dialog_group.cont.cont.throbber_image


	from widget_user_group_dialog_datatable import WidgetUserGroupDialogDatatable
	widget = WidgetUserGroupDialogDatatable( search_obj_type, None  )
	widget.set_data()
	widget.set_selected_rows()
	widget.render( datatable, error_text )

	response.shared_variables[ "selectedObjects" ] = widget.selected_rows
	response.shared_variables[ "displayedObjects" ] = []
	response.shared_variables[ "obj_guid" ] = None
	response.shared_variables[ "obj_type" ] = obj_type

	count_text.action( "setText", [ "0" ] )
	throbber_image.action( "hide", [ "" ] )

main()
