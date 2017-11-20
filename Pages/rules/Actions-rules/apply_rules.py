import json
from vdom_trace import Trace
import managers

#try:
if True:
	keys = session.get("rules_keysList",None)

	w_AclSubjects 	= session["w_AclSubjects"]
	w_AclRules 		= session["w_AclRules"]

	acl_object 	= w_AclSubjects.get_acl_object()
	subject		= w_AclRules.get_selected_subject()

	for rule in acl_object.rules(subject=subject):
		rule.delete() if rule.subject.guid == subject.guid else None

	for rule_key in keys:
		acl_object.add_rule(subject=subject, access=rule_key)

	acl_object.save()

	w_AclSubjects.render(dt_subjects = self.cnt_acls.cnt_subjects.dt_subjects)

#except Exception, ex:
#	for key in session.keys():
#		del session[key]
#	session[ "error" ] = unicode("Server encountered an error. Please, contact with your administrator or check the information log.")
#	managers.log_manager.info_bug(
#		u"ProAdmin error: %s" % Trace.exception_trace(5),
#		u"ProAdmin %s" % self.name
#	)
#	self.action("goTo",["/login"])
