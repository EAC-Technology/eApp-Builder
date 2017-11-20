from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	header = request.arguments["headerData"]

	if header == "edit":

		import ProAdmin
		import localization

		lang = localization.get_lang()

		current_tab = request.shared_variables[ "currentTab" ]
		guid = request.arguments["keyField"]
		obj = obj_type = search_obj_type = datatable = error_text = None

		if current_tab == "users":

			obj_type = "user"
			search_obj_type = "group"
			count_text = self.dialog_user.groups_cont.groups_count
			datatable = self.dialog_user.groups_cont.cont.datatable_groups
			error_text = self.dialog_user.groups_cont.cont.error_text
			throbber_image = self.dialog_user.groups_cont.cont.throbber_image

			users = ProAdmin.application().get_users(guid = guid)
			obj = user = users[0] if users else None

			if user:


				from widget_user_group_dialog import country_list
				index = -1
				if user.country:
					try: index = country_list.index( user.country )
					except: pass

				self.dialog_user.edit_user_text.action( "show", [ "" ] )
				self.dialog_user.new_user_text.action( "hide", [ "" ] )
				self.dialog_user.continue_btn.action( "hide", [ "" ] )
				self.dialog_user.create_btn.action( "hide", [ "" ] )
				self.dialog_user.save_btn.action( "show", [ "" ] )
				self.dialog_user.groups_btn.action( "show", [ "" ] )
				self.dialog_user.info_btn.action( "hide", [ "" ] )
				self.dialog_user.user_form.action( "show", [ "" ] )
				self.dialog_user.groups_cont.action( "hide", [ "" ] )
				self.dialog_user.user_form.password_input.action( "show", [ "" ] )
				self.dialog_user.user_form.visible_password_input.action( "hide", [ "" ] )

				self.dialog_user.user_form.cont.fn_input.action(
							"setValue",
							[ user.first_name if user.first_name else "" ]  )

				self.dialog_user.user_form.cont.ln_input.action(
							"setValue",
							[ user.last_name if user.last_name else "" ]  )

				self.dialog_user.user_form.login_input.action(
							"setValue",
							[ user.email ]  )

				self.dialog_user.user_form.password_input.action(
							"setValue",
							[ "********" ]  )

				self.dialog_user.user_form.visible_password_input.action(
							"setValue",
							[ "" ]  )

				self.dialog_user.user_form.cont.email_input.action(
							"setValue",
							[ user.notification_email if user.notification_email else "" ]  )

				self.dialog_user.user_form.cont.phone_input.action(
							"setValue",
							[ user.cell_phone if user.cell_phone else "" ]  )

				self.dialog_user.user_form.cont.country_input.action(
							"selectItem",
							[ index ]  )

				self.dialog_user.user_form.keywords_input.action(
							"setValue",
							[ ", ".join( user.keywords ) if user.keywords else "" ]  )

				self.dialog_user.user_form.continue_input.action( "setValue", [ "0" ] )

				self.dialog_user.action( "show", [ "" ] )


			else:
				self.growl.action("show", [ lang[	"error_title"	], lang[ "user_doesnt_exist_error" ] ] )
				return


		else:
			obj_type = "group"
			search_obj_type = "user"
			count_text = self.dialog_group.cont.users_count
			datatable = self.dialog_group.cont.cont.datatable_users
			error_text = self.dialog_group.cont.cont.error_text
			throbber_image = self.dialog_group.cont.cont.throbber_image

			groups = ProAdmin.application().get_groups(guid = guid)
			obj  = group = groups[0] if groups else None

			if group:
				self.dialog_group.edit_group_text.action( "show", [ "" ] )
				self.dialog_group.new_group_text.action( "hide", [ "" ] )
				self.dialog_group.create_btn.action( "hide", [ "" ] )
				self.dialog_group.save_btn.action( "show", [ "" ] )

				self.dialog_group.group_form.gn_input.action(
							"setValue",
					[ group.name if group.name else "" ] )

				self.dialog_group.cont.show_all_btn.action( "hide", [ "" ] )
				self.dialog_group.cont.search_form.searchfield.action( "setValue", [ "" ] )

				self.dialog_group.action( "show", [ "" ] )

			else:
				self.growl.action("show", [ lang[	"error_title"	], lang[ "group_doesnt_exist_error" ] ] )
				return



		if obj:

			from widget_user_group_dialog_datatable import WidgetUserGroupDialogDatatable
			widget = WidgetUserGroupDialogDatatable( search_obj_type, obj  )
			widget.set_data()
			widget.set_selected_rows()
			widget.render( datatable, error_text )

			count = len( widget.selected_rows )
			response.shared_variables[ "selectedObjects" ] = widget.selected_rows
			response.shared_variables[ "displayedObjects" ] = []
			response.shared_variables[ "obj_guid" ] = guid
			response.shared_variables[ "obj_type" ] = obj_type

			count_text.action( "setText", [ count ] )
			throbber_image.action( "hide", [ "" ] )

		else:
			response.shared_variables[ "selectedObjects" ] = \
			response.shared_variables[ "displayedObjects" ] = \
			response.shared_variables[ "obj_guid" ] = \
			response.shared_variables[ "obj_type" ] = None


main()
