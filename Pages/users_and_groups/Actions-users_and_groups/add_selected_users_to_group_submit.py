from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	import json
	import localization
	lang = localization.get_lang()

	selectedRows = request.shared_variables[ "selectedRows" ]
	selectedRows = [] if not selectedRows else selectedRows

	if not selectedRows: self.growl.action( "show", [ lang[ "warning_title" ], lang[ "select_objects_error" ] ] )
	else:

		import ProAdmin
		import cgi

		args = request.arguments

		group_id = args.get( "formlist_groups" )
		group = error = None

		if group_id == "new":
			name = args.get( "new_group_name", "" ).strip()
			if not name: error = "fill_group_name_field"
			elif ProAdmin.application().get_groups( name = name ): error = "group_name_already_exists"
			else:
				group = ProAdmin.application().create_group( cgi.escape( name ) )
				group.save()
		else:
			groups = ProAdmin.application().get_groups( guid = group_id )
			if groups: group = groups[0]
			else:	error = "group_doesnt_exist"


		if error:
			self.growl.action( "show", [ lang[ "error_title" ], lang[ error ] ] )

		else:
			from widget_add_users_to_group_dialog import WidgetAddUsersToGroupDialog
			widget = WidgetAddUsersToGroupDialog(
								selectedRows
						)

			widget.add_users_to_group( group )
			self.dialog_add_to_group.action( "hide", [ ] )

			response.shared_variables[ "selectedRows" ] = None
			self.cont.dt_main.action( "selectNone", [ "" ] )

			import widget_user_and_group_dd_group
			widget_user_and_group_dd_group.render( self.form.obj_from_group )


			from widget_user_and_group_datatable import WidgetUserAndGroupDatatable
			current_tab = request.shared_variables[ "currentTab" ]
			headername = request.shared_variables[ "headername" ]
			asc = request.shared_variables[ "sort_up" ]
			per_page = request.shared_variables[ "per_page" ]
			page = request.shared_variables[ "pagenumber" ]
			from_group = request.shared_variables[ "from_group_guid" ]

			widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab, from_group	)
			if page is not None: widgetUGDatatable.set_page( page )
			if per_page: widgetUGDatatable.set_objects_per_page( per_page )
			if headername and asc is not None: widgetUGDatatable.sort_by( headername, asc )

			widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )


main()
