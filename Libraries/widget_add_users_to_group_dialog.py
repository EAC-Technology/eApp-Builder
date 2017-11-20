import ProAdmin
import json
from io import StringIO
from collections import OrderedDict
import localization


class WidgetAddUsersToGroupDialog(object):

	def __init__(self,list ):
		self.__list = list 	# list of ID's (GUID)


	def render(self, dialog, formlist_groups, list_users, new_group_name ):

		users, groups = ProAdmin.application().get_users(),\
						ProAdmin.application().get_groups()

		lang = localization.get_lang()

		data_dict = OrderedDict()
		new_group_name.action( "setValue", [ "" ] )
		if not groups:
			formlist_groups.selectedvalue = "new"
			new_group_name.action( "show", [ "" ] )
		else:
			new_group_name.action( "hide", [ "" ] )
			for group in groups[0:-1]:
				data_dict[ group.guid ] = group.name
			data_dict[ groups[-1].guid ] = "%s<option value='0' disabled='disabled'>_______________________</option>" % groups[-1].name
			formlist_groups.selectedvalue = groups[0].guid

		data_dict[ "new" ]	= lang[ "create_new_group_text" ]
		formlist_groups.value = json.dumps( data_dict )

		template = 	u"<div class='acl_container_user'><b>{0}</b> </div>"
		list_users.data = json.dumps( { user.guid : template.format( user.name ) for user in users if user.guid in self.__list } )

		dialog.action( "show", [ "" ] )


	def add_users_to_group( self, group ):
		for user in ProAdmin.application().get_users():
			if user.guid in self.__list:
				group.add_user( user )

		group.save()


