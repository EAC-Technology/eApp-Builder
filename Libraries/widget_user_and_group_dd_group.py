import ProAdmin, json, localization
from collections import OrderedDict

def render( dropdown, selected = None ):
	lang = localization.get_lang()
	groups = ProAdmin.application().get_groups()
	data_dict = OrderedDict()

	for group in groups[0:-1]:	data_dict[ group.guid ] = group.name
	data_dict[ groups[-1].guid ] = "%s<option value='0' disabled='disabled'>_______________________</option>" % groups[-1].name
	data_dict[ "all" ] = lang.get( "dd_all_users", "All users" )

	dropdown.selectedvalue = selected if selected else "all"
	dropdown.value = json.dumps( data_dict )
#
