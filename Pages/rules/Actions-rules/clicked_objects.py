from widget_acl_rules import WidgetAclRules
from widget_acl_subjects import WidgetAclSubjects
import ProAdmin
from vdom_trace import Trace
import managers
import localization


lang = localization.get_lang()

try:

	#tree click
	object_guid = request.arguments["key"]

	if object_guid:

		app = ProAdmin.application()

		acl_object = ProAdmin.application().get_by_guid(object_guid)
		if not acl_object:
			raise Exception("Can't find object with this guid '%s'" % str(object_guid))
#		WidgetAclObjects = session["WidgetAclObjects"]
#		WidgetAclObjects.render(self.cnt_acls.cnt_tree.app_structure)
		w_AclSubjects = WidgetAclSubjects()
		w_AclSubjects.set_application(app)
		w_AclSubjects.set_acl_object(acl_object)
		w_AclSubjects.render(
			dt_subjects  = self.cnt_acls.cnt_subjects.dt_subjects
		)

		w_AclRules = WidgetAclRules()
		w_AclRules.set_application(app)
		w_AclRules.set_acl_object(acl_object)
		w_AclRules.render(
			dt_rules = self.cnt_acls.cnt_rules.dt_rules
		)

		session["w_AclSubjects"] = w_AclSubjects
		session["w_AclRules"] 	 = w_AclRules

except Exception:
	self.growl.action("show",[ lang["error"], lang["unknown_error"]])

#except Exception, ex:
#	for key in session.keys():
#		del session[key]
#	session[ "error" ] = unicode("Server encountered an error. Please, contact with your administrator or check the information log.")
#	managers.log_manager.info_bug(
#		u"ProAdmin error: %s" % Trace.exception_trace(5),
#		u"ProAdmin %s" % self.name
#	)
#	self.action("goTo",["/login"])
