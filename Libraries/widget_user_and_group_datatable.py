import ProAdmin
import json
import localization

GROUP_MAX_LENGTH = 60
USER_NAME_MAX_LENGTH = 50
USER_LOGIN_MAX_LENGTH = 30
USER_GROUPS_MAX_LENGTH = 35
MAX_LENGTH_STRING_END = "..."

class WidgetUserAndGroupDatatable:

	def __init__(self, current_tab, from_group_guid = None ):

		self.__current_tab 	= current_tab
		self.__page = 0
		self.users = self.groups = None
		self.__from_group_guid 	 = from_group_guid

		if self.__current_tab == "users":

			if self.__from_group_guid and self.__from_group_guid != "all":
				groups = ProAdmin.application().get_groups( guid = self.__from_group_guid )
				if groups:
					self.users = groups[0].get_users()
				else:
					self.users = []
			else:
				self.users = ProAdmin.application().get_users()

		else:
			self.groups = ProAdmin.application().get_groups()

		self.__is_user_name_sorted 	=	\
		self.__is_user_email_sorted = 	\
		self.__is_group_name_sorted = False
		self.__sort_up				= True
		self.__per_page				= 10


	def sort_by( self, field_name, asc ):

		if field_name == "email": self.sort_by_user_email( asc )
		elif field_name == "fullname": self.sort_by_user_name( asc )
		elif field_name == "groupname": self.sort_by_group_name( asc )

	def sort_by_user_email( self, asc ):
		self.__is_user_email_sorted = True
		self.users.sort(key=lambda x: x.email.lower())
		if not asc:	self.users = self.users[::-1]
		self.__sort_up = asc

	def sort_by_group_name( self, asc ):
		self.__is_group_name_sorted  = True
		self.groups.sort(key=lambda x: x.name.lower())
		if not asc:	self.groups = self.groups[::-1]
		self.__sort_up = asc

	def sort_by_user_name( self, asc ):
		self.__is_user_name_sorted = True
		self.users.sort(key=lambda x: x.name.lower())
		if not asc:	self.users = self.users[::-1]
		self.__sort_up = asc

	def set_page(self,page):
		self.__page = page - 1

	def set_objects_per_page( self, count ):
		self.__per_page = count



	#after
	def render( self, datatable, pager = None, error_text = None ):

		lang = localization.get_lang()

		pages_count = 0
		data 		= []
		header 		= []
		objects 	= None
		get_row 	= None

		edit_template = u"""<div class='ug_subject_edit' title='%s %s'></div>""" % (
							lang["dialog_edit_btn"],
							"%s"
						)

		err_text = ""
		if self.__current_tab == "users": # users

			objects = self.users
			err_text = "no_users_text"

			def get_groups( user ):
				result, l, endl = [], 0, None
				for group in user.get_groups():
					result.append( group.name )
					l += len( group.name )
					if l > USER_GROUPS_MAX_LENGTH:
						endl = MAX_LENGTH_STRING_END
						break
				return ( ", ".join( result )[ :USER_GROUPS_MAX_LENGTH ] + endl ) if endl else  ", ".join( result )

			get_row = lambda user: [ 	user.email[:USER_LOGIN_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( user.email ) > USER_LOGIN_MAX_LENGTH else user.email ,
										user.name[:USER_NAME_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( user.name ) > USER_NAME_MAX_LENGTH else user.name,
										get_groups( user )
									]


			h_email 	= "<span id='email' class='ug_datatable_title'>%s</span>" % (lang.get( 'login_column_header' ))
			h_fullname 	= "<span id='fullname' class='ug_datatable_title'>%s</span>" % (lang.get( 'fullname_column_header' ))
			h_groups	= "<span id='groups' class='ug_datatable_title'>%s</span>" % (lang.get( 'group_column_header' ))

			# adding 'sort' arrow if needed
			if self.__is_user_email_sorted:
				if self.__sort_up:		h_email += "&nbsp;<span class='ug_header_sorted_down'></span>"
				else:						h_email += "&nbsp;<span class='ug_header_sorted_up'></span>"

			elif self.__is_user_name_sorted:
				if self.__sort_up:	 	h_fullname += "&nbsp;<span class='ug_header_sorted_down'></span>"
				else:						h_fullname += "&nbsp;<span class='ug_header_sorted_up'></span>"

			header 		= [
				"id",
				"edit",
				h_email,
				h_fullname,
				h_groups
			]

		else: # groups

			objects = self.groups
			get_users = lambda group: len( group.get_users() )
			get_row = lambda group: [ group.name[:GROUP_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( group.name ) > GROUP_MAX_LENGTH else group.name, get_users( group ) ]
			h_groupname = "<span id='groupname' class='ug_datatable_title'>%s</span>" % (lang.get( 'groupname_column_header' ))
			h_user_count = "<span id='user_count' class='ug_datatable_title'>%s</span>" % (lang.get( 'users_count_column_header' ))

			if self.__is_group_name_sorted:
				if self.__sort_up:		h_groupname += "&nbsp;<span class='ug_header_sorted_down'></span>"
				else:						h_groupname += "&nbsp;<span class='ug_header_sorted_up'></span>"

			header = ["id","edit",h_groupname, h_user_count ]



		count 	= len( objects ) 										# users count
		left 	= self.__page * self.__per_page										# from 	- index
		right 	= left + self.__per_page if left + self.__per_page <= count else count			# to 	- index
		pages_count = 	str( count/self.__per_page + 1 )\
						if count % self.__per_page > 0 	\
						else str( count/ self.__per_page )# number of pages

		for obj in objects[left:right]:
			data.append([
				obj.guid,
				edit_template % obj.name ] + get_row( obj ) )


		datatable.key 		= "id"
		datatable.hiddenfields = json.dumps(["id"])
		datatable.header 	= json.dumps(header)
		datatable.data 		= json.dumps(data)

		if data:
			pager.pagescount 	= pages_count
			pager.currentpage 	= self.__page+1
			pager.top = str( 237  + 38 * len(data ) + 100 )
			datatable.visible   = pager.visible = "1"
			error_text.action( "hide", [ "" ] )
		else:
			datatable.action( "hide", [ "" ] )
			pager.action( "hide", [ "" ] )
			if err_text:
				error_text.action( "show", [ "" ] )
				error_text.action( "setText", [ lang.get( err_text ) ] )
			else:
				error_text.action( "hide", [ "" ] )



