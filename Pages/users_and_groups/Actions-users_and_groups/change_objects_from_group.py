from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	from widget_user_and_group_datatable import WidgetUserAndGroupDatatable

	args = request.arguments

	from_group = args.get( "itemValue" )

	current_tab = request.shared_variables[ "currentTab" ]
	headername = request.shared_variables[ "headername" ]
	asc = request.shared_variables[ "sort_up" ]
	per_page = request.shared_variables[ "per_page" ]

	widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab, from_group	)
	if per_page: widgetUGDatatable.set_objects_per_page( per_page )
	if headername and asc is not None: widgetUGDatatable.sort_by( headername, asc )

	widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )

	response.shared_variables[ "from_group_guid" ] = from_group
	response.shared_variables[ "pagenumber" ] = \
	response.shared_variables[ "selectedRows" ] = None

	self.cont.dt_main.action( "selectNone", [ "" ] )



main()
