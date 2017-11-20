from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	#search_obj_type = "group" if request.shared_variables[ "obj_type" ] == "user" else "user"
	search_obj_type = "user"
	datatable = self.dialog_group.cont.cont.datatable_users
	error_text = self.dialog_group.cont.cont.error_text
	throbber_image = self.dialog_group.cont.cont.throbber_image

	searchfield = request.arguments.get( "searchfield", "" )
	selected_objects = request.shared_variables[ "selectedObjects" ]

	from widget_user_group_dialog_datatable import WidgetUserGroupDialogDatatable
	widgetUGDatatable = WidgetUserGroupDialogDatatable( search_obj_type, None )
	widgetUGDatatable.selected_rows = selected_objects

	if searchfield:
		from widget_search_user_group_dialog import WidgetSearchUserGroupDialog
		widget = WidgetSearchUserGroupDialog( search_obj_type )
		widget.set_objects()
		widget.search( searchfield )
		result = widget.search_result

		self.dialog_group.cont.show_all_btn.action( "show" , [ "" ] )
		response.shared_variables[ "displayedObjects" ] = [ o.guid for o in result ]
		widgetUGDatatable.get_data = lambda: result
	else:
		response.shared_variables[ "displayedObjects" ] = [ ]
		widgetUGDatatable.set_data()
		self.dialog_group.cont.show_all_btn.action( "hide", [ "" ] )

	widgetUGDatatable.render( datatable, error_text )

	throbber_image.action( "hide", [ "" ] )

main()
