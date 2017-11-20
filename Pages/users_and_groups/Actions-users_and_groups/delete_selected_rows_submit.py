from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():


	import localization
	lang = localization.get_lang()

	selectedRows = request.shared_variables[ "selectedRows" ]
	selectedRows = [] if not selectedRows else selectedRows

	if not selectedRows: self.growl.action( "show", [ lang[ "warning_title" ], lang[ "select_objects_error" ] ] )
	else:

		from widget_user_and_group_delete_dialog import WidgetUserAndGroupDeleteDialog
		widget = WidgetUserAndGroupDeleteDialog(
							selectedRows,
							request.shared_variables[ "currentTab" ]
					)

		widget.delete_subjects()

		from widget_user_and_group_datatable import WidgetUserAndGroupDatatable
		current_tab = request.shared_variables[ "currentTab" ]
		headername = request.shared_variables[ "headername" ]
		asc = request.shared_variables[ "sort_up" ]
		per_page = request.shared_variables[ "per_page" ]
		from_group = request.shared_variables[ "from_group_guid" ]

		widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab, from_group	)
		if per_page: widgetUGDatatable.set_objects_per_page( per_page )
		if headername and asc is not None: widgetUGDatatable.sort_by( headername, asc )

		widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )

		response.shared_variables[ "pagenumber" ] = \
		response.shared_variables[ "selectedRows" ] = None
		self.cont.dt_main.action( "selectNone", [ "" ] )
		self.dialog_delete_user_group.action( "hide", [ "" ] )


		if request.shared_variables[ "currentTab" ] == "groups":
			import widget_user_and_group_dd_group
			widget_user_and_group_dd_group.render( self.form.obj_from_group )

main()
