from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	from widget_user_and_group_datatable import WidgetUserAndGroupDatatable

	headername = request.arguments["headername"]
	current_tab = request.shared_variables[ "currentTab" ]
	per_page = request.shared_variables[ "per_page" ]
	from_group = request.shared_variables[ "from_group_guid" ]
	page =  request.shared_variables[ "pagenumber" ]

	widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab, from_group	)

	asc = True if headername.find( "sorted_down" ) == -1 else False
	sorted = False

	if current_tab == "users":
		if headername.find( "email" ) > -1:
			headername = "email"
			sorted = True

		elif headername.find( "fullname" ) > -1:
			headername = "fullname"
			sorted = True

	elif current_tab == "groups":
		if headername.find( "groupname" ) > -1:
			headername = "groupname"
			sorted = True

	if sorted:
		response.shared_variables[ "headername" ] = headername
		response.shared_variables[ "sort_up" ] = asc

		if per_page: widgetUGDatatable.set_objects_per_page( per_page )
		if page is not None: widgetUGDatatable.set_page( page )

		widgetUGDatatable.sort_by( headername, asc )
		widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )

		response.shared_variables[ "selectedRows" ] = None
		self.cont.dt_main.action( "selectNone", [ "" ] )


main()
