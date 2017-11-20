import ProAdmin
import json
import localization

GROUP_MAX_LENGTH = 30
USER_NAME_MAX_LENGTH = 23
USER_LOGIN_MAX_LENGTH = 18
MAX_LENGTH_STRING_END = "..."


class WidgetUserGroupDialogDatatable(object):

	def __init__( self, search_obj_type, obj ):

		self.search_obj_type 	= search_obj_type
		self.obj				= obj
		self.selected_rows		= []
		self.get_data 			= None

	def set_data( self ):

		if self.search_obj_type == "user":
			self.get_data = ProAdmin.application().get_users
		else:
			self.get_data = ProAdmin.application().get_groups

	def set_selected_rows( self ):

		if self.obj:
			if self.search_obj_type == "user":
				for obj in self.obj.get_users(): self.selected_rows.append( obj.guid )
			else:
				for obj in self.obj.get_groups(): self.selected_rows.append( obj.guid )

	def render( self, datatable, error_text ):

		lang = localization.get_lang()

		header = []
		get_row = None

		if self.search_obj_type == "user":

			h_email = "<span id='email' class='ug_datatable_title'>%s</span>" % (lang.get( 'login_column_header' ))
			h_fullname = "<span id='fullname' class='ug_datatable_title'>%s</span>" % (lang.get( 'fullname_column_header' ))

			header 		= [
				"id",
				h_fullname,
				h_email
			]

			get_row = lambda user: [ 	user.name[:USER_NAME_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( user.name ) > USER_NAME_MAX_LENGTH else user.name,
										user.email[:USER_LOGIN_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( user.email ) > USER_LOGIN_MAX_LENGTH else user.email
									]


		else:

			h_groupname = "<span id='groupname' class='ug_datatable_title'>%s</span>" % (lang.get( 'groupname_column_header' ))
			header = ["id",h_groupname]

			get_row = get_row = lambda group: [ group.name[:GROUP_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( group.name ) > GROUP_MAX_LENGTH else group.name ]





		self.selected_rows = list( set( self.selected_rows ) )

		data = []
		append = data.append
		for obj in self.get_data(): append( [ obj.guid ] + get_row( obj ) )
		data.sort(key=lambda x: x[1].lower())

		if data:
			datatable.key = "id"
			datatable.hiddenfields = json.dumps( [ "id" ] )
			datatable.header = json.dumps( header )
			datatable.data	= json.dumps( data )
			datatable.selectedrows = json.dumps( self.selected_rows )
			datatable.visible = "1"
			error_text.action( "hide", [ "" ] )
		else:
			error_text.action( "show", [ "" ] )
			datatable.action( "hide", [ "" ] )


	def apply_changes_to_object( self, obj, rows ):

		obj_data = []
		get_data = remove_data = add_data = None

		if self.search_obj_type == "user":
			get_data = ProAdmin.application().get_users
			remove_data = obj.remove_user
			add_data = obj.add_user
			obj_data = obj.get_users()

		else:
			get_data = ProAdmin.application().get_groups
			remove_data = obj.remove_group
			add_data = obj.add_group
			obj_data = obj.get_groups()

		for o in obj_data:
			if o.guid not in rows:
				remove_data( o )
			else:
				rows.remove( o.guid )


		for guid in rows:
			search = get_data( guid = guid )
			if search: add_data( search[0] )
