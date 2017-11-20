import ProAdmin
from io import StringIO

NAME_MAX_LENGTH = 23
MAX_LENGTH_STRING_END = "..."

class WidgetUserAndGroupDeleteDialog(object):

	def __init__(self,list, current_tab ):
		self.__list = list 	# list of ID's (GUID)
		self.__subjects = None
		self.__current_tab = current_tab


	def set_subjects( self ):

		self.__subjects = 	ProAdmin.application().get_users() \
							if self.__current_tab == "users" else\
							ProAdmin.application().get_groups()

	def delete_subjects(self):

		self.set_subjects()
		for subject in self.__subjects: # should be initialized during render()
			if subject.guid in self.__list:
				self.__list.remove( subject.guid )
				subject.delete()

	def render(self,dialog, html):
		result_str = StringIO()
		self.set_subjects()
		template = 	u"<div class='acl_container_user'><b>%(name)s</b> </div>" \
					if self.__current_tab == "users" else\
					u"<div class='acl_container_group'><b>%(name)s</b> </div>"


		for subject in self.__subjects:
			if subject.guid in self.__list:
				result_str.write( template % {
						'name'	: subject.name[:NAME_MAX_LENGTH]+MAX_LENGTH_STRING_END if len( subject.name ) > NAME_MAX_LENGTH else subject.name
					})

		html.action( "setHTML", [ result_str.getvalue() ] )
		result_str.close()

		dialog.action( "show", [ "" ] )
