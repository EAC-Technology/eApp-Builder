from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	active_tab = "groups" if request.arguments.get("Name") == "cont_group" else "users"

	response.shared_variables[ "currentTab" ] = active_tab
	response.shared_variables[ "selectedRows" ] = \
	response.shared_variables[ "headername" ] = \
	response.shared_variables[ "sort_up" 	] = \
	response.shared_variables[ "pagenumber" ] = \
	response.shared_variables[ "obj_type" 	] = \
	response.shared_variables[ "obj_guid" 	] = \
	response.shared_variables[ "from_group_guid" ] = \
	response.shared_variables[ "per_page" ] = None


	from widget_user_and_group_datatable import WidgetUserAndGroupDatatable
	widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab = active_tab )
	widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )


	if active_tab == "groups":
		self.btn_add_to_group.action( "hide", [ "" ] )
		self.btn_create_user.action( "hide", [ "" ] )
		self.btn_create_group.action( "show", [ "" ] )
		self.form.obj_from_group.action( "hide", [ "" ] )

	else:
		self.btn_add_to_group.action( "show", [ "" ] )
		self.btn_create_user.action( "show", [ "" ] )
		self.btn_create_group.action( "hide", [ "" ] )
		self.form.obj_from_group.action( "show", [ "" ] )

main()
