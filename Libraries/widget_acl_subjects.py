import ProAdmin
import json
from io import StringIO
import localization


class WidgetAclSubjects(object):

	def __init__(self):

		# input data
		self.__application 		= None
		self.__acl_object 		= None
		self.__subject 			= None
		self.__access_types 	= None

	def set_application(self, app):
		self.__application = app

	def get_application(self):
		return self.__application

	def set_acl_object(self, acl_object):
		self.__acl_object = acl_object

	def get_acl_object(self):
		return self.__acl_object

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

	def get_selected_subject(self):
		return self.__subject

	def render(self,	dt_subjects	= None, ): # subjects datatable

		# SUBJECTS
		if not self.__application: 	self.EmptyValue("app_guid")
		if not self.__acl_object: 	self.EmptyValue("object_guid")

		result_uag_header 	= ["guid", "name","arrow"]
		result_uag_hidden	= ["guid"]
		result_uag_key		= "guid"
		result_uag_data		= []
		selected_subjects 	= []

		subjects 	= ProAdmin.application().get_groups() + ProAdmin.application().get_users()
		rules 		= self.__acl_object.rules()

		object_types = ProAdmin.scheme().get_aclobjecttypes()

		for type in object_types:
			if type.name == self.__acl_object.type:
				self.__access_types = type.access_types
				break;

		if not self.__access_types:
			raise Exception("This object type '%s' is not registered" % self.__acl_object.type)

		lang = localization.get_lang()
		# fill subjects (groups and users)
		for subject in subjects:
			subject_rules = [rule.access for rule in rules if rule.subject == subject]
			#subject_rules = [self.__access_types[subj_rule] for subj_rule in subject_rules if subj_rule in self.__access_types]
			subject_rules = [lang[subj_rule] for subj_rule in subject_rules if subj_rule in self.__access_types]
			rights_str = ", ".join(subject_rules)

			if hasattr(subject, "email"):
				# user
				subject_str = "<div class='acl_container_user'>%(name)s (%(rights)s) </div>" % {
					'name'	: subject.name,
					'rights': rights_str
				}
			else:
				# group
				subject_str = "<div class='acl_container_group'><b>%(name)s</b> (%(rights)s)</div>" % {
					'name'	: subject.name,
					'rights': rights_str
				}

			result_uag_data.append([subject.guid, subject_str, ""])

		if self.__subject:
			selected_subjects = [self.__subject.guid]

		dt_subjects.showheader 		= "0"
		dt_subjects.title 			= ""
		dt_subjects.selectionmode	= "0" # single
		dt_subjects.hiddenfields 	= json.dumps(result_uag_hidden)
		dt_subjects.key				= result_uag_key
		dt_subjects.header 			= json.dumps(result_uag_header)
		dt_subjects.data 			= json.dumps(result_uag_data)
		dt_subjects.selectedrows 	= json.dumps(selected_subjects)
#		dt_subjects.title			= "<b>%s <span class='small_guid'>(%s)</span></b>" % (
#			self.__acl_object.name,
#			self.__acl_object.guid,
#		)

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
}

#%(id)s .th-cell
{
	border: none;

	font-size:12px;
}

#%(id)s table.table td.cell-1
{
	padding-left: 10px !important;
}

#%(id)s table.table td.cell
{
	border: none;
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

#%(id)s .row_selected td.cell-2
{
	background: url(/7f0a5366-8baa-4fa1-9ce7-42d77fd20de6.png) left no-repeat;
}



		"""





