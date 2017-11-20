import ProAdmin
import json
from io import StringIO
import localization


class WidgetAclRules(object):

	def __init__(self):

		# input data
		self.__application 		= None
		self.__acl_object 		= None
		self.__subject			= None
		self.__access_types 	= None

	def set_application(self, app):
		self.__application = app

	def get_application(self):
		return self.__application

	def set_acl_object(self, acl_object):
		self.__acl_object = acl_object

	def get_acl_object(self):
		return self.__acl_object

	def set_app_guid(self, app_guid):
		self.__application = DB_Application.get_by_guid(app_guid)
		if not self.__application:
			raise Exception("Widget error: Can't find object with this guid '%s'" % str(app_guid))

	def set_object_guid(self, object_guid):
		self.__acl_object = ProAdmin.application().get_by_guid(object_guid)
		if not self.__acl_object:
			raise Exception("Widget error: Can't find object with this guid '%s'" % str(object_guid))

	def set_subject(self, subject_guid):
		subjects = ProAdmin.application().get_users() + ProAdmin.application().get_groups()
		rules 	= self.__acl_object.rules()
		selected_subject = None
		for subj in subjects:
			if subj.guid == subject_guid:
				selected_subject = subj
				break;
		if not selected_subject:
			raise Exception("No such subject: %s"%subject_guid)

		self.__subject = selected_subject

	def get_acl_object(self):
		if not self.__acl_object:
			raise Exception("Widget error: attribute '%s' is not defined" % "aclobject")

		return self.__acl_object

	def get_selected_subject(self):
		return self.__subject

	def render(self,
			dt_rules		# subject rules datatable
		):

		if not self.__subject: # no data provided (app, object, subject)
			dt_rules.showheader 	= "0"
			dt_rules.data 			= json.dumps([])
			dt_rules.title			= ""
			return
		lang = localization.get_lang()
		result_rules_header 	= ["access", u'<span title="f">{0}</span>'.format(lang.get("Full", "Full"))]
		result_rules_hidden		= ["access"]
		result_rules_key		= "access"
		result_rules_data		= []
		selected_rules		 	= []

		# OBJECT_TYPES (need for getting ACCESS_TYPES )
		object_types = ProAdmin.scheme().get_aclobjecttypes()

		for type in object_types:
			if type.name == self.__acl_object.type:
				self.__access_types = type.access_types
				break;

		if not self.__access_types:
			raise Exception("This object type '%s' is not registered" % self.__acl_object.type)

		for access_key, access_value in self.__access_types.items():
			result_rules_data.append([access_key, u'<span title="{0}">{1}</span>'.format(access_key, lang.get( access_key, access_value )) ] )

		if self.__subject:
			rules 		= self.__acl_object.rules()
			selected_rules = [rule.access for rule in rules if rule.subject == self.__subject]

		dt_rules.showheader 	= "1"
		dt_rules.title 			= ""
		dt_rules.selectionmode 	= "1" # multi
		dt_rules.hiddenfields 	= json.dumps(result_rules_hidden)
		dt_rules.key			= result_rules_key
		dt_rules.header 		= json.dumps(result_rules_header)
		dt_rules.data 			= json.dumps(result_rules_data)
		dt_rules.selectedrows 	= json.dumps(selected_rules)

	def clear_render(self,
		dt_rules		# subject rules datatable
	):
		dt_rules.showheader 		= "0"
		dt_rules.selectionmode 	= "1" # multi
		dt_rules.data 			= json.dumps([])

	def EmptyValue(value):
		raise Exception("Widget error: attribute '%s' is not defined" % str(value))


	def style(self):
		return """
#%(id)s caption
{

}

#%(id)s table.table
{
	border-collapse:collapse;
	border: none;
	height: 0;

}

#%(id)s .thead
{
	font-size:12px;
	text-align:left;
	padding:0 8px;
	line-height: 16px;
}

#%(id)s .thead:hover
{
	color: #BD202F;
	background: #fafafa !important;
}

#%(id)s .th-cell
{
	border: none;
	padding-left:6px;
	font-size:12px;
}

#%(id)s th.th-cell-0, #%(id)s td.cell-0 input
{
	width: 18px;
	margin: 2px;
}

#%(id)s table.table td.cell
{
	border: none;
	padding-left:6px;
	text-align:left;

}


#%(id)s table.table td.cell:hover
{
	color: #BD202F;
}

#%(id)s tr.even
{

}

#%(id)s .row
{

}

#%(id)s .row:hover
{
	background: #fafafa !important;
}

#%(id)s .row_selected
{
	background:#f2f2f2!important;
	color: #BD202F;
}

		"""
