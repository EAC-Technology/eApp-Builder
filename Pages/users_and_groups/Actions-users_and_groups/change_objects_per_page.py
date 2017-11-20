from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	from widget_user_and_group_datatable import WidgetUserAndGroupDatatable

	args = request.arguments

	try:	per_page = int( args.get( "itemValue", 10 ) )
	except: per_page = 10
	if per_page not in [ 10, 20, 50, 100 ]: per_page = 10

	current_tab = request.shared_variables[ "currentTab" ]
	headername = request.shared_variables[ "headername" ]
	asc = request.shared_variables[ "sort_up" ]
	from_group = request.shared_variables[ "from_group_guid" ]

	widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab, from_group	)
	widgetUGDatatable.set_objects_per_page( per_page )
	if headername and asc is not None: widgetUGDatatable.sort_by( headername, asc )

	widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )

	response.shared_variables[ "pagenumber" ] = \
	response.shared_variables[ "selectedRows" ] = None
	response.shared_variables[ "per_page" ] = per_page

	self.cont.dt_main.action( "selectNone", [ "" ] )



main()
