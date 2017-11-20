import ProAdmin
import json
import localization

GROUP_MAX_LENGTH = 30
USER_NAME_MAX_LENGTH = 23
USER_LOGIN_MAX_LENGTH = 18
MAX_LENGTH_STRING_END = "..."

class WidgetSearchUserGroupDialog(object):

	def __init__( self, obj_type ):

		self.obj_type = obj_type	#* ONLY INT
		self.objects = []

	def set_objects( self ):

		if self.obj_type == "user":
			self.objects = ProAdmin.application().get_users()
		else:
			self.objects = ProAdmin.application().get_groups()



	def search( self, search_query ):

		search_query = search_query.lower()

		search_func = None
		if self.obj_type == "user":

			search_func = lambda user: True if  (
				user.email.lower().find( search_query ) >= 0 or
				user.name.lower().find( search_query ) >= 0 ) else False

		else:
			search_func = lambda group: True if group.name.lower().find( search_query ) >= 0 else False

		self.objects = [ obj for obj in self.objects if search_func( obj ) ]


	search_result = property( lambda x: x.objects )
