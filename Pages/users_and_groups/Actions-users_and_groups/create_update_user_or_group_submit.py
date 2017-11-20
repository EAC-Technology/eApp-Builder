from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme

@authenticated
@administrator
@local_scheme
@error_handler
def main():

	import ProAdmin
	import localization
	import re
	from cgi import escape


	class SilentException( Exception ):
		pass

	class IllegalCharactersInPhoneError( Exception ):
		def __init__( self ):
			Exception.__init__( self, 'Phone contains illegal characters' )


	args = request.arguments

	obj_type = request.shared_variables[ "obj_type" ]
	obj_guid = request.shared_variables[ "obj_guid" ]

	reopen = 0

	lang = localization.get_lang()

	try:

		created_obj = None
		if obj_type == "user":

			last_name 		= escape( args.get( 'ln_input', 		"" ).strip() )
			first_name 		= escape( args.get( 'fn_input', 		"" ).strip() )
			login 			= escape( args.get( 'login_input', 		"" ).strip() )
			password 		= escape( args.get( 'password_input', 	"" ).strip() )
			notif_email 	= escape( args.get( 'email_input', 		"" ).strip() )
			cell_phone 		= escape( args.get( 'phone_input', 		"" ).strip() )
			keywords 		= escape( args.get( 'keywords_input', 	"" ).strip() )

			reopen 	 = args.get( "continue_input", 0 )
			try: reopen = int( reopen )
			except: reopen = 0

			country_index	 = args.get( 'country_input', 	-1 )
			try: country_index = int( country_index )
			except: country_index = -1

			if 	not login \
				or not password \
				or not first_name \
				or not last_name \
				or not notif_email \
				or not cell_phone \
				or country_index == -1:

				self.growl.action("show", [	lang[	"error_title"	], lang[	"fill_all_fields_with_star_error"	]	]	)
				self.dialog_user.user_form.action( "show", [ "" ] )
				self.dialog_user.groups_cont.action( "hide", [ "" ] )
				self.dialog_user.info_btn.action( "show", [ "" ] )
				self.dialog_user.groups_btn.action( "hide", [ "" ] )
				self.dialog_user.user_form.login_input.action( "setFocus", [ "" ] )
				raise SilentException

			else:

				from widget_user_group_dialog import country_list
				country = "" if country_index >= len( country_list ) else country_list[ country_index ]

				user = None
				if obj_guid:
					users = ProAdmin.application().get_users( guid = obj_guid )
					if users: user =  users[ 0 ]
					else:
						self.growl.action("show", [ lang[	"error_title"	], lang[ "user_doesnt_exist_error" ] ] )
						raise SilentException


				users = ProAdmin.application().get_users( email = login )
				if users:
					raise_error = False
					if not user: raise_error = True
					elif user.guid != users[0].guid: raise_error = True

					if raise_error:
						self.growl.action("show", [ lang[	"error_title"	], lang[ "user_login_already_exist_error" ] ] )
						raise SilentException

				if not user: user = ProAdmin.application().create_user( login )

				user.email = login

				if password not in [ "", "********" ]:
					user.password = password
				else:
					if obj_guid and password:
						pass
					else:
						self.growl.action(	"show",
							[ 	lang[ "error_title"	],
								lang[ "user_password_is_empty_error" ]
							])
						raise SilentException


				user.first_name = first_name
				user.last_name = last_name

				g = re.match(r'[a-zA-Z\d.\-\_]+@[a-zA-Z\d.\-\_]+',notif_email)
				if not g:
					self.growl.action("show", [ lang[	"error_title"	], lang[ "user_email_is_incorrect_error" ] ] )
					raise SilentException

				user.notification_email = notif_email

				for c in cell_phone:
					if c not in "0123456789-, +": raise IllegalCharactersInPhoneError

				user.cell_phone = cell_phone
				user.country = country
				user.keywords = [ k.strip() for k in keywords.split(",") ] if keywords else []
				user.save()

				created_obj = user

				if obj_guid or reopen == 0:
					self.dialog_user.action( "hide", [ "" ] )

				else:
					self.dialog_user.edit_user_text.action( "hide", [ "" ] )
					self.dialog_user.new_user_text.action( "show", [ "" ] )
					self.dialog_user.continue_btn.action( "show", [ "" ] )
					self.dialog_user.create_btn.action( "show", [ "" ] )
					self.dialog_user.save_btn.action( "hide", [ "" ] )
					self.dialog_user.groups_btn.action( "show", [ "" ] )
					self.dialog_user.info_btn.action( "hide", [ "" ] )
					self.dialog_user.user_form.action( "show", [ "" ] )
					self.dialog_user.groups_cont.action( "hide", [ "" ] )
					self.dialog_user.user_form.cont.fn_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.cont.ln_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.login_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.password_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.visible_password_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.cont.email_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.cont.phone_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.keywords_input.action( "setValue",	[ "" ]  )
					self.dialog_user.user_form.continue_input.action( "setValue", [ "0" ] )


		elif obj_type == "group":

			name = escape( args.get( "gn_input", 	"" ).strip() )
			if not name:
				self.growl.action("show",[ lang[	"error_title"	], lang[ "fill_group_name_field" ] ] )
				raise SilentException
			else:
				group = None
				if obj_guid:
					groups = ProAdmin.application().get_groups( guid = obj_guid )
					if groups: group = groups[ 0 ]
					else:
						self.growl.action("show", [ lang[	"error_title"	], lang[ "group_doesnt_exist_error" ] ] )
						raise SilentException


				groups = ProAdmin.application().get_groups( name = name )
				if groups:
					raise_error = False
					if not group: raise_error = True
					elif group.guid != groups[0].guid: raise_error = True

					if raise_error:
						self.growl.action("show", [ lang[	"error_title"	], lang[ "group_name_already_exists" ] ] )
						raise SilentException

				if not group: group = ProAdmin.application().create_group( name )



				group.name = name
				group.save()

				created_obj = group

				self.dialog_group.action( "hide", [ "" ] )


		selected_rows = request.shared_variables[ "selectedObjects" ]

		from widget_user_group_dialog_datatable import WidgetUserGroupDialogDatatable
		widget = WidgetUserGroupDialogDatatable( "user" if obj_type == "group" else "group", None )
		widget.apply_changes_to_object( created_obj, selected_rows )


		response.shared_variables[ "selectedRows" ] = None
		self.cont.dt_main.action( "selectNone", [ "" ] )

		if obj_type == "group":
			import widget_user_and_group_dd_group
			widget_user_and_group_dd_group.render( self.form.obj_from_group )
			self.form.obj_from_group.visible = "0"


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

		if reopen == 0:
			response.shared_variables[ "selectedObjects" ] = \
			response.shared_variables[ "displayedObjects" ] = \
			response.shared_variables[ "obj_guid" ] = \
			response.shared_variables[ "obj_type" ] = None



	except SilentException:
		pass

	except IllegalCharactersInPhoneError:
		self.growl.action( 'show', [ lang[	"error_title"	], lang[ "user_phone_illegal_characters" ] ] )

	except ProAdmin.SubjectsLimitationError:
		error_text = lang.get( 'subjects_limitation_error', 'Users limit exceeded' )
		self.growl.action( 'show', [ lang[	"error_title"	], error_text ] )


main()
